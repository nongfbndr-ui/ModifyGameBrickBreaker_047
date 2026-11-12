import pygame
import random
import math

# ============================================================
# INISIALISASI PYGAME
# ============================================================
pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker Deluxe")

clock = pygame.time.Clock()

# ============================================================
# WARNA
# ============================================================
BLACK = (8, 10, 25)
DARK_BLUE = (15, 20, 45)
WHITE = (255, 255, 255)
GRAY = (170, 170, 180)
RED = (255, 70, 70)
GREEN = (60, 220, 120)
BLUE = (60, 150, 255)
YELLOW = (255, 220, 70)
PURPLE = (180, 80, 255)
ORANGE = (255, 140, 50)
CYAN = (50, 230, 230)

BRICK_COLORS = [
    RED,
    ORANGE,
    YELLOW,
    GREEN,
    BLUE,
    PURPLE,
    CYAN
]

# ============================================================
# FONT
# ============================================================
small_font = pygame.font.SysFont("arial", 20)
medium_font = pygame.font.SysFont("arial", 30, bold=True)
large_font = pygame.font.SysFont("arial", 55, bold=True)
title_font = pygame.font.SysFont("arial", 65, bold=True)


# ============================================================
# FUNGSI MENAMPILKAN TEKS DI TENGAH
# ============================================================
def draw_center_text(text, font, color, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(text_surface, text_rect)


# ============================================================
# CLASS PADDLE
# ============================================================
class Paddle:
    def __init__(self):
        self.width = 120
        self.height = 18
        self.speed = 9

        self.rect = pygame.Rect(
            WIDTH // 2 - self.width // 2,
            HEIGHT - 60,
            self.width,
            self.height
        )

        self.color = WHITE

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        # Mencegah paddle keluar layar
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def reset(self):
        self.rect.centerx = WIDTH // 2
        self.rect.y = HEIGHT - 60

    def draw(self):
        # Bayangan paddle
        shadow_rect = self.rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4

        pygame.draw.rect(
            screen,
            (40, 40, 60),
            shadow_rect,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            self.color,
            self.rect,
            border_radius=8
        )

        # Bagian tengah paddle
        center_rect = pygame.Rect(
            self.rect.centerx - 20,
            self.rect.y,
            40,
            self.rect.height
        )

        pygame.draw.rect(
            screen,
            CYAN,
            center_rect,
            border_radius=8
        )


