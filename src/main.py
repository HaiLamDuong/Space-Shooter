import os
from random import randint, uniform

import pygame

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

# General setup
pygame.init()

# Caption
pygame.display.set_caption("Space shooter")

# Surfaces
displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Imports
starSurf = pygame.image.load(os.path.join("images", "star.png")).convert_alpha()
laserSurf = pygame.image.load(os.path.join("images", "laser.png")).convert_alpha()
meteorSurf = pygame.image.load(os.path.join("images", "meteor.png")).convert_alpha()
explosionSurfs = [
    pygame.image.load(os.path.join("images", "explosion", f"{i}.png")).convert_alpha()
    for i in range(21)
]


font = pygame.font.Font(os.path.join("images", "Oxanium-Bold.ttf"), 40)

laserSound = pygame.mixer.Sound(os.path.join("audio", "laser.wav"))
laserSound.set_volume(0.2)
explosionSound = pygame.mixer.Sound(os.path.join("audio", "explosion.wav"))
explosionSound.set_volume(0.2)
damageSound = pygame.mixer.Sound(os.path.join("audio", "damage.ogg"))
damageSound.set_volume(0.2)
gameMusic = pygame.mixer.Sound(os.path.join("audio", "game_music.wav"))
gameMusic.set_volume(0.1)
gameMusic.play(-1)

# Groups
allSprites = pygame.sprite.Group()
meteorSprites = pygame.sprite.Group()
laserSprites = pygame.sprite.Group()

# Custom events
meteorEvent = pygame.event.custom_type()
pygame.time.set_timer(meteorEvent, 500)

# System
running = True
clock = pygame.time.Clock()


# Sprites
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(
            os.path.join("images", "player.png")
        ).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 400

        # Cooldown
        self.canShoot = True
        self.laserShootTime = 0
        self.coolDownDuration = 400

    def laserTimer(self):
        if (
            not self.canShoot
            and pygame.time.get_ticks() - self.laserShootTime >= self.coolDownDuration
        ):
            self.canShoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )
        self.rect.center += self.direction * self.speed * dt

        recentKeys = pygame.key.get_just_pressed()
        if recentKeys[pygame.K_SPACE] and self.canShoot:
            Laser(laserSurf, self.rect.midtop, (allSprites, laserSprites))
            laserSound.play()
            self.canShoot = False
            self.laserShootTime = pygame.time.get_ticks()
        self.laserTimer()


class Star(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)


class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.speed = 400

    def update(self, dt):
        self.rect.centery -= self.speed * dt
        if self.rect.bottom < 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.originalSurf = surf
        self.image = self.originalSurf
        self.rect = self.image.get_frect(center=pos)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 600)
        self.lifeTime = 3000
        self.creationTime = pygame.time.get_ticks()
        self.rotationSpeed = randint(20, 50)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.creationTime > self.lifeTime:
            self.kill()
        self.rotation += self.rotationSpeed * dt
        self.image = pygame.transform.rotozoom(self.originalSurf, self.rotation, 1)
        self.rect = self.image.get_frect(center=self.rect.center)


class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, surfs, pos, groups):
        super().__init__(groups)
        self.surfs = surfs
        self.currentIndex = 0
        self.image = self.surfs[self.currentIndex]
        self.rect = self.image.get_frect(center=pos)

    def update(self, dt):
        self.currentIndex += 20 * dt
        if self.currentIndex >= len(self.surfs):
            self.kill()
        else:
            self.image = self.surfs[int(self.currentIndex)]
            self.rect = self.image.get_frect(center=self.rect.center)


def collisions():
    global running
    if pygame.sprite.spritecollide(
        player, meteorSprites, True, pygame.sprite.collide_mask
    ):
        damageSound.play()
        running = False
    for laser in laserSprites:
        collidedSprites = pygame.sprite.spritecollide(laser, meteorSprites, True)
        if collidedSprites:
            laser.kill()
            AnimatedExplosion(explosionSurfs, laser.rect.midtop, allSprites)
            explosionSound.play()


def displayScore():
    textSurf = font.render(str(pygame.time.get_ticks() // 100), True, (240, 240, 240))
    textRect = textSurf.get_frect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    displaySurface.blit(textSurf, textRect)
    pygame.draw.rect(
        displaySurface, (240, 240, 240), textRect.inflate(20, 10).move(0, -8), 5, 10
    )


# Initital objects
[
    Star(starSurf, (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)), allSprites)
    for _ in range(20)
]
player = Player(allSprites)

# Game loop
while running:
    deltaTime = clock.tick() / 1000
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteorEvent:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteorSurf, (x, y), (allSprites, meteorSprites))
    # Update
    allSprites.update(deltaTime)
    collisions()

    # Draw the game
    displaySurface.fill("#3a2e3f")
    displayScore()
    allSprites.draw(displaySurface)

    pygame.display.update()

pygame.quit()
