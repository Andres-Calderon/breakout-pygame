import math
import random
from enum import Enum, auto

import pygame

from config import (
    BALL_RADIUS,
    BALL_SPEED,
    BRICK_COLS,
    BRICK_HEIGHT,
    BRICK_PADDING,
    BRICK_ROWS,
    BRICK_TOP_OFFSET,
    BRICK_WIDTH,
    COLORS,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
    PADDLE_WIDTH,
    PADDLE_Y_OFFSET,
    POWERUP_FALL_SPEED,
    POWERUP_SIZE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class PowerUpType(Enum):
    MULTIBALL = auto()
    EXPAND = auto()
    LIFE = auto()
    SLOW = auto()
    SPEED = auto()


POWERUP_LABELS = {
    PowerUpType.MULTIBALL: "3x",
    PowerUpType.EXPAND: "W",
    PowerUpType.LIFE: "+1",
    PowerUpType.SLOW: "S",
    PowerUpType.SPEED: "F",
}


class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.rect = pygame.Rect(
            (SCREEN_WIDTH - self.width) // 2,
            SCREEN_HEIGHT - PADDLE_Y_OFFSET,
            self.width,
            self.height,
        )
        self.speed = PADDLE_SPEED

    def reset(self):
        self.rect.centerx = SCREEN_WIDTH // 2
        self.reset_modifiers()

    def reset_modifiers(self):
        center = self.rect.center
        self.width = PADDLE_WIDTH
        self.speed = PADDLE_SPEED
        self.rect.width = self.width
        self.rect.height = self.height
        self.rect.center = center

    def set_width(self, width: int):
        center = self.rect.center
        self.width = width
        self.rect.width = width
        self.rect.center = center

    def move(self, direction: int):
        self.rect.x += direction * self.speed
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)

    def set_center_x(self, x: int):
        self.rect.centerx = max(self.width // 2, min(SCREEN_WIDTH - self.width // 2, x))

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, COLORS["paddle"], self.rect, border_radius=6)


class Ball:
    def __init__(self):
        self.radius = BALL_RADIUS
        self.speed = BALL_SPEED
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.velocity = pygame.Vector2(0, 0)
        self.stuck = True

    def reset(self, paddle: Paddle):
        self.rect.center = paddle.rect.center
        self.rect.bottom = paddle.rect.top - 2
        self.velocity.update(0, 0)
        self.stuck = True

    def launch(self, angle_degrees: float = -70):
        if not self.stuck:
            return
        self.stuck = False
        angle = math.radians(angle_degrees)
        self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * self.speed

    def update(self, paddle: Paddle):
        if self.stuck:
            self.rect.centerx = paddle.rect.centerx
            self.rect.bottom = paddle.rect.top - 2
            return

        self.rect.x += int(self.velocity.x)
        self.rect.y += int(self.velocity.y)

        if self.rect.left <= 0:
            self.rect.left = 0
            self.velocity.x *= -1
        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.velocity.x *= -1

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity.y *= -1

    def bounce_off_paddle(self, paddle: Paddle):
        offset = (self.rect.centerx - paddle.rect.centerx) / (paddle.width / 2)
        offset = max(-1.0, min(1.0, offset))
        angle = math.radians(-60 - 30 * offset)
        self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * self.speed

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, COLORS["ball"], self.rect.center, self.radius)


class Brick:
    def __init__(self, x: int, y: int, color: tuple[int, int, int], points: int):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color
        self.points = points
        self.alive = True

    def draw(self, surface: pygame.Surface):
        if not self.alive:
            return
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)
        pygame.draw.rect(surface, (255, 255, 255, 40), self.rect, 1, border_radius=4)


def create_bricks() -> list[Brick]:
    total_width = BRICK_COLS * BRICK_WIDTH + (BRICK_COLS - 1) * BRICK_PADDING
    start_x = (SCREEN_WIDTH - total_width) // 2
    bricks: list[Brick] = []

    for row in range(BRICK_ROWS):
        color = COLORS["bricks"][row % len(COLORS["bricks"])]
        points = (BRICK_ROWS - row) * 10
        y = BRICK_TOP_OFFSET + row * (BRICK_HEIGHT + BRICK_PADDING)
        for col in range(BRICK_COLS):
            x = start_x + col * (BRICK_WIDTH + BRICK_PADDING)
            bricks.append(Brick(x, y, color, points))

    return bricks


class PowerUp:
    COLOR_KEYS = {
        PowerUpType.MULTIBALL: "multiball",
        PowerUpType.EXPAND: "expand",
        PowerUpType.LIFE: "life",
        PowerUpType.SLOW: "slow",
        PowerUpType.SPEED: "speed",
    }

    def __init__(self, x: int, y: int, kind: PowerUpType):
        self.kind = kind
        self.rect = pygame.Rect(0, 0, POWERUP_SIZE * 2, POWERUP_SIZE * 2)
        self.rect.center = (x, y)
        self.speed = POWERUP_FALL_SPEED

    @classmethod
    def random_at(cls, x: int, y: int) -> "PowerUp":
        return cls(x, y, random.choice(list(PowerUpType)))

    def update(self):
        self.rect.y += self.speed

    def is_off_screen(self) -> bool:
        return self.rect.top > SCREEN_HEIGHT

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        color_key = self.COLOR_KEYS[self.kind]
        color = COLORS["powerups"][color_key]
        pygame.draw.circle(surface, color, self.rect.center, POWERUP_SIZE)
        pygame.draw.circle(surface, (255, 255, 255), self.rect.center, POWERUP_SIZE, 2)
        label = font.render(POWERUP_LABELS[self.kind], True, (20, 20, 30))
        surface.blit(label, label.get_rect(center=self.rect.center))
