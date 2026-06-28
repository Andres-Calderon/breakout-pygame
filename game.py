import math
import random
from enum import Enum, auto

import pygame

from config import (
    BALL_SPEED,
    COLORS,
    LIVES,
    PADDLE_SPEED,
    PADDLE_WIDTH,
    POWERUP_DROP_CHANCE,
    POWERUP_DURATION_MS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from entities import Ball, Brick, Paddle, PowerUp, PowerUpType, create_bricks
from platform_utils import is_mobile, setup_window


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    WIN = auto()


class BreakoutGame:
    def __init__(self):
        self.mobile = is_mobile()

        if not pygame.get_init():
            pygame.init()
        pygame.display.set_caption("Breakout - Pygame")
        self.screen = setup_window()
        self.clock = pygame.time.Clock()
        font_name = None if self.mobile else "consolas"
        self.font_large = pygame.font.SysFont(font_name, 48, bold=True)
        self.font_medium = pygame.font.SysFont(font_name, 28)
        self.font_small = pygame.font.SysFont(font_name, 22)
        self.font_powerup = pygame.font.SysFont(font_name, 14, bold=True)

        self.state = GameState.MENU
        self.paddle = Paddle()
        self.balls: list[Ball] = []
        self.bricks: list[Brick] = []
        self.powerups: list[PowerUp] = []
        self.score = 0
        self.lives = LIVES
        self.level = 1
        self.base_ball_speed = BALL_SPEED
        self.active_effects: dict[str, int] = {}

    def reset_round(self):
        self.paddle.reset()
        self.balls = [Ball()]
        self.balls[0].speed = self.base_ball_speed
        self.balls[0].reset(self.paddle)
        self.bricks = create_bricks()
        self.powerups.clear()
        self.clear_timed_effects()

    def start_new_game(self):
        self.score = 0
        self.lives = LIVES
        self.level = 1
        self.base_ball_speed = BALL_SPEED
        self.reset_round()
        self.state = GameState.PLAYING

    def next_level(self):
        self.level += 1
        self.base_ball_speed += 0.4
        self.reset_round()

    def clear_timed_effects(self):
        self.active_effects.clear()
        self.paddle.reset_modifiers()
        for ball in self.balls:
            ball.speed = self.base_ball_speed
            if not ball.stuck and ball.velocity.length() > 0:
                ball.velocity = ball.velocity.normalize() * ball.speed

    def has_stuck_ball(self) -> bool:
        return any(ball.stuck for ball in self.balls)

    def launch_balls(self):
        angles = [-75, -70, -65]
        stuck_balls = [ball for ball in self.balls if ball.stuck]
        for index, ball in enumerate(stuck_balls):
            ball.launch(angles[index % len(angles)])

    def spawn_multiball(self):
        for _ in range(2):
            ball = Ball()
            ball.speed = self.base_ball_speed
            ball.stuck = False
            ball.rect.center = self.paddle.rect.center
            ball.rect.bottom = self.paddle.rect.top - 2
            angle = random.uniform(-120, -60)
            ball.velocity = pygame.Vector2(math.cos(math.radians(angle)), math.sin(math.radians(angle)))
            ball.velocity = ball.velocity.normalize() * ball.speed
            self.balls.append(ball)

    def apply_powerup(self, kind: PowerUpType):
        now = pygame.time.get_ticks()

        if kind == PowerUpType.MULTIBALL:
            self.spawn_multiball()
        elif kind == PowerUpType.EXPAND:
            self.paddle.set_width(int(PADDLE_WIDTH * 1.7))
            self.active_effects["expand"] = now + POWERUP_DURATION_MS
        elif kind == PowerUpType.LIFE:
            self.lives += 1
        elif kind == PowerUpType.SLOW:
            slow_speed = max(2.5, self.base_ball_speed * 0.55)
            for ball in self.balls:
                ball.speed = slow_speed
                if not ball.stuck and ball.velocity.length() > 0:
                    ball.velocity = ball.velocity.normalize() * slow_speed
            self.active_effects["slow"] = now + POWERUP_DURATION_MS
        elif kind == PowerUpType.SPEED:
            self.paddle.speed = int(PADDLE_SPEED * 1.9)
            self.active_effects["speed"] = now + POWERUP_DURATION_MS

    def update_timed_effects(self):
        now = pygame.time.get_ticks()

        if "expand" in self.active_effects and now >= self.active_effects["expand"]:
            self.paddle.set_width(PADDLE_WIDTH)
            del self.active_effects["expand"]

        if "slow" in self.active_effects and now >= self.active_effects["slow"]:
            for ball in self.balls:
                ball.speed = self.base_ball_speed
                if not ball.stuck and ball.velocity.length() > 0:
                    ball.velocity = ball.velocity.normalize() * self.base_ball_speed
            del self.active_effects["slow"]

        if "speed" in self.active_effects and now >= self.active_effects["speed"]:
            self.paddle.speed = PADDLE_SPEED
            del self.active_effects["speed"]

    def maybe_drop_powerup(self, brick: Brick):
        if random.random() < POWERUP_DROP_CHANCE:
            self.powerups.append(PowerUp.random_at(brick.rect.centerx, brick.rect.centery))

    def handle_ball_brick_collision(self, ball: Ball, brick: Brick):
        brick.alive = False
        self.score += brick.points
        self.maybe_drop_powerup(brick)

        overlap_left = ball.rect.right - brick.rect.left
        overlap_right = brick.rect.right - ball.rect.left
        overlap_top = ball.rect.bottom - brick.rect.top
        overlap_bottom = brick.rect.bottom - ball.rect.top
        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        if min_overlap == overlap_left or min_overlap == overlap_right:
            ball.velocity.x *= -1
        else:
            ball.velocity.y *= -1

    def handle_collisions(self):
        for ball in self.balls:
            if ball.stuck:
                continue

            if ball.rect.colliderect(self.paddle.rect) and ball.velocity.y > 0:
                ball.bounce_off_paddle(self.paddle)

            for brick in self.bricks:
                if brick.alive and ball.rect.colliderect(brick.rect):
                    self.handle_ball_brick_collision(ball, brick)
                    break

    def update_powerups(self):
        for powerup in self.powerups:
            powerup.update()

        for powerup in self.powerups[:]:
            if powerup.rect.colliderect(self.paddle.rect):
                self.apply_powerup(powerup.kind)
                self.powerups.remove(powerup)
            elif powerup.is_off_screen():
                self.powerups.remove(powerup)

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.state = GameState.GAME_OVER
            return

        self.balls = [Ball()]
        self.balls[0].speed = self.base_ball_speed
        self.balls[0].reset(self.paddle)
        self.powerups.clear()
        self.clear_timed_effects()

    def finger_to_x(self, finger_x: float) -> int:
        return int(finger_x * SCREEN_WIDTH)

    def handle_tap(self):
        if self.state == GameState.MENU:
            self.start_new_game()
        elif self.state == GameState.PLAYING:
            self.launch_balls()
        elif self.state in (GameState.GAME_OVER, GameState.WIN):
            self.start_new_game()

    def handle_touch_position(self, finger_x: float):
        if self.state == GameState.PLAYING:
            self.paddle.set_center_x(self.finger_to_x(finger_x))

    def update(self):
        if self.state != GameState.PLAYING:
            return

        keys = pygame.key.get_pressed()
        direction = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(
            keys[pygame.K_LEFT] or keys[pygame.K_a]
        )
        self.paddle.move(direction)

        mouse_x, _ = pygame.mouse.get_pos()
        if not self.mobile and pygame.mouse.get_pressed()[0]:
            self.paddle.set_center_x(mouse_x)

        if self.mobile and pygame.mouse.get_pressed()[0]:
            self.paddle.set_center_x(mouse_x)

        for ball in self.balls:
            ball.update(self.paddle)

        self.handle_collisions()
        self.update_powerups()
        self.update_timed_effects()

        self.balls = [ball for ball in self.balls if ball.rect.top <= SCREEN_HEIGHT]
        if not self.balls:
            self.lose_life()

        if all(not brick.alive for brick in self.bricks):
            if self.level >= 3:
                self.state = GameState.WIN
            else:
                self.next_level()

    def draw_hud(self):
        score_text = self.font_small.render(f"Puntos: {self.score}", True, COLORS["text"])
        lives_text = self.font_small.render(f"Vidas: {self.lives}", True, COLORS["text"])
        level_text = self.font_small.render(f"Nivel: {self.level}", True, COLORS["text"])
        self.screen.blit(score_text, (20, 16))
        self.screen.blit(lives_text, (SCREEN_WIDTH // 2 - lives_text.get_width() // 2, 16))
        self.screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 20, 16))

        if self.active_effects:
            effect_names = []
            if "expand" in self.active_effects:
                effect_names.append("Barra+")
            if "slow" in self.active_effects:
                effect_names.append("Lento")
            if "speed" in self.active_effects:
                effect_names.append("Rapido")
            effects_text = self.font_small.render(" | ".join(effect_names), True, (180, 220, 255))
            self.screen.blit(effects_text, (20, 42))

    def draw_playfield(self):
        for brick in self.bricks:
            brick.draw(self.screen)
        for powerup in self.powerups:
            powerup.draw(self.screen, self.font_powerup)
        self.paddle.draw(self.screen)
        for ball in self.balls:
            ball.draw(self.screen)
        self.draw_hud()
        if self.has_stuck_ball():
            hint_text = "Toca para lanzar" if self.mobile else "ESPACIO para lanzar"
            hint = self.font_small.render(hint_text, True, COLORS["text"])
            self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 90)))

    def draw_centered_text(self, lines: list[str], y_start: int = 220):
        for index, line in enumerate(lines):
            font = self.font_large if index == 0 else self.font_medium
            text = font.render(line, True, COLORS["text"])
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_start + index * 56))
            self.screen.blit(text, rect)

    def draw(self):
        self.screen.fill(COLORS["background"])

        if self.state == GameState.MENU:
            if self.mobile:
                lines = [
                    "BREAKOUT",
                    "Toca para jugar",
                    "Arrastra el dedo para mover la barra",
                    "Destruye ladrillos y recoge mejoras",
                ]
            else:
                lines = [
                    "BREAKOUT",
                    "Presiona ESPACIO para jugar",
                    "Flechas / A-D o mouse",
                    "Destruye ladrillos y recoge mejoras",
                ]
            self.draw_centered_text(lines)
        elif self.state == GameState.PLAYING:
            self.draw_playfield()
        elif self.state == GameState.PAUSED:
            self.draw_playfield()
            self.draw_centered_text(["PAUSA", "P para continuar"], 250)
        elif self.state == GameState.GAME_OVER:
            self.draw_centered_text(
                ["GAME OVER", f"Puntuacion: {self.score}", "ESPACIO para reintentar", "ESC para menu"]
            )
        elif self.state == GameState.WIN:
            self.draw_centered_text(
                ["GANASTE!", f"Puntuacion final: {self.score}", "ESPACIO para jugar de nuevo"]
            )

        pygame.display.flip()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.FINGERDOWN:
            self.handle_touch_position(event.x)
            self.handle_tap()
        elif event.type == pygame.FINGERMOTION:
            self.handle_touch_position(event.x)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.mobile:
                mouse_x, _ = pygame.mouse.get_pos()
                self.paddle.set_center_x(mouse_x)
                self.handle_tap()
            elif self.state == GameState.PLAYING:
                self.launch_balls()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state in (GameState.PLAYING, GameState.PAUSED):
                    self.state = GameState.MENU
                else:
                    return False

            if event.key == pygame.K_SPACE:
                if self.state == GameState.MENU:
                    self.start_new_game()
                elif self.state == GameState.PLAYING:
                    self.launch_balls()
                elif self.state == GameState.GAME_OVER:
                    self.start_new_game()
                elif self.state == GameState.WIN:
                    self.start_new_game()

            if event.key == pygame.K_p and self.state == GameState.PLAYING:
                self.state = GameState.PAUSED
            elif event.key == pygame.K_p and self.state == GameState.PAUSED:
                self.state = GameState.PLAYING

        return True

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if not self.handle_event(event):
                    running = False

            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
