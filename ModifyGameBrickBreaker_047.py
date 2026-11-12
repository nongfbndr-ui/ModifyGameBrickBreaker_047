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


# ============================================================
# CLASS BALL
# ============================================================
class Ball:
    def __init__(self):
        self.radius = 10
        self.base_speed = 5
        self.speed = self.base_speed

        self.x = float(WIDTH // 2)
        self.y = float(HEIGHT - 100)

        self.dx = random.choice([-1, 1]) * self.speed
        self.dy = -self.speed

        # Rect langsung dibuat agar collision tidak error
        self.rect = pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2
        )

    def update_rect(self):
        self.rect.x = int(self.x - self.radius)
        self.rect.y = int(self.y - self.radius)

    def update(self):
        self.x += self.dx
        self.y += self.dy

        # Tabrakan dinding kiri
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.dx = abs(self.dx)

        # Tabrakan dinding kanan
        if self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius
            self.dx = -abs(self.dx)

        # Tabrakan bagian atas
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.dy = abs(self.dy)

        self.update_rect()

        # Mengembalikan True jika bola jatuh
        return self.y - self.radius > HEIGHT

    def bounce_from_paddle(self, paddle):
        # Pastikan bola sedang bergerak ke bawah
        if self.dy > 0 and self.rect.colliderect(paddle.rect):
            self.y = paddle.rect.top - self.radius

            # Menghitung posisi benturan pada paddle
            distance = self.x - paddle.rect.centerx
            normalized_distance = distance / (paddle.rect.width / 2)

            # Sudut pantulan maksimum 60 derajat
            angle = normalized_distance * math.radians(60)

            current_speed = math.sqrt(
                self.dx ** 2 + self.dy ** 2
            )

            self.dx = current_speed * math.sin(angle)
            self.dy = -abs(current_speed * math.cos(angle))

            self.update_rect()

    def bounce_from_brick(self, brick):
        overlap_left = self.rect.right - brick.rect.left
        overlap_right = brick.rect.right - self.rect.left
        overlap_top = self.rect.bottom - brick.rect.top
        overlap_bottom = brick.rect.bottom - self.rect.top

        minimum_overlap = min(
            overlap_left,
            overlap_right,
            overlap_top,
            overlap_bottom
        )

        # Menentukan sisi brick yang terkena
        if minimum_overlap == overlap_left:
            self.dx = -abs(self.dx)
            self.x = brick.rect.left - self.radius

        elif minimum_overlap == overlap_right:
            self.dx = abs(self.dx)
            self.x = brick.rect.right + self.radius

        elif minimum_overlap == overlap_top:
            self.dy = -abs(self.dy)
            self.y = brick.rect.top - self.radius

        else:
            self.dy = abs(self.dy)
            self.y = brick.rect.bottom + self.radius

        self.update_rect()

    def increase_speed(self, amount=0.25):
        current_speed = math.sqrt(
            self.dx ** 2 + self.dy ** 2
        )

        if current_speed == 0:
            return

        new_speed = min(current_speed + amount, 11)

        self.dx = (self.dx / current_speed) * new_speed
        self.dy = (self.dy / current_speed) * new_speed

    def reset(self, level=1):
        self.x = float(WIDTH // 2)
        self.y = float(HEIGHT - 100)

        self.speed = min(
            self.base_speed + (level - 1) * 0.7,
            9
        )

        self.dx = random.choice([-1, 1]) * self.speed
        self.dy = -self.speed

        self.update_rect()

    def draw(self):
        # Efek cahaya luar
        pygame.draw.circle(
            screen,
            (80, 120, 180),
            (int(self.x), int(self.y)),
            self.radius + 4
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x), int(self.y)),
            self.radius
        )

        # Titik cahaya
        pygame.draw.circle(
            screen,
            CYAN,
            (int(self.x - 3), int(self.y - 3)),
            3
        )


