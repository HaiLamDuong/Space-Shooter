# Space Shooter

A classic top-down space shooter game built with Pygame. Navigate your spaceship, avoid meteors, and blast them into space dust!

[](https://github.com/user-attachments/assets/b065f419-db6b-4fc0-90a3-b7473e64c4bb)

## Quick Start

1. Install requirements:
    ```bash
    pip install -r requirements.txt
    ```
2. Run the game:
    ```bash
    python src/main.py
    ```

## Features

- **Endless Gameplay:** Survive as long as you can against an endless barrage of meteors.
- **Dynamic Physics:** Meteors have randomized speeds, rotations, and directions.
- **Classic Controls:** Smooth spaceship movement and responsive shooting mechanics.
- **Score Tracking:** Survive longer to increase your score.

## How to Play

### Controls

| Action      | Key     |
| ----------- | ------- |
| Move Up     | `W`     |
| Move Left   | `A`     |
| Move Down   | `S`     |
| Move Right  | `D`     |
| Shoot Laser | `SPACE` |

### Objective

- **Dodge:** Avoid colliding with meteors at all costs. One hit and it's game over!
- **Shoot:** Use your lasers to destroy meteors before they reach you.
- **Survive:** Your score increases the longer you stay alive.

## Requirements

- Python 3.x
- `pygame-ce==2.5.6`
- `PyTMX==3.32`
