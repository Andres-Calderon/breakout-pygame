SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

PADDLE_WIDTH = 110
PADDLE_HEIGHT = 14
PADDLE_SPEED = 8
PADDLE_Y_OFFSET = 50

BALL_RADIUS = 7
BALL_SPEED = 5

BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 24
BRICK_PADDING = 6
BRICK_TOP_OFFSET = 80

LIVES = 3

POWERUP_DROP_CHANCE = 0.24
POWERUP_FALL_SPEED = 4
POWERUP_SIZE = 14
POWERUP_DURATION_MS = 10_000

COLORS = {
    "background": (15, 15, 35),
    "paddle": (80, 200, 255),
    "ball": (255, 255, 255),
    "text": (240, 240, 255),
    "bricks": [
        (255, 80, 80),
        (255, 140, 60),
        (255, 220, 60),
        (100, 220, 120),
        (80, 160, 255),
    ],
    "powerups": {
        "multiball": (255, 215, 50),
        "expand": (80, 255, 140),
        "life": (255, 100, 150),
        "slow": (100, 220, 255),
        "speed": (255, 150, 60),
    },
}
