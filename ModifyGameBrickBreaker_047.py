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


# ============================================================
# CLASS BRICK
# ============================================================
class Brick:
    def __init__(self, x, y, width, height, health, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = health
        self.max_health = health
        self.color = color

    def hit(self):
        self.health -= 1
        return self.health <= 0

    def draw(self):
        # Bayangan brick
        shadow = self.rect.copy()
        shadow.x += 3
        shadow.y += 3

        pygame.draw.rect(
            screen,
            (20, 20, 35),
            shadow,
            border_radius=5
        )

        # Warna berubah ketika brick rusak
        if self.health == 1 and self.max_health > 1:
            display_color = tuple(
                max(50, value - 80)
                for value in self.color
            )
        else:
            display_color = self.color

        pygame.draw.rect(
            screen,
            display_color,
            self.rect,
            border_radius=5
        )

        pygame.draw.rect(
            screen,
            WHITE,
            self.rect,
            width=2,
            border_radius=5
        )

        # Tampilkan ketahanan brick jika lebih dari satu
        if self.health > 1:
            health_text = small_font.render(
                str(self.health),
                True,
                WHITE
            )

            health_rect = health_text.get_rect(
                center=self.rect.center
            )

            screen.blit(health_text, health_rect)


# ============================================================
# CLASS PARTICLE
# ============================================================
class Particle:
    def __init__(self, x, y, color):
        self.x = float(x)
        self.y = float(y)

        self.dx = random.uniform(-3, 3)
        self.dy = random.uniform(-4, 1)

        self.radius = random.randint(2, 5)
        self.life = random.randint(20, 40)
        self.color = color

    def update(self):
        self.x += self.dx
        self.y += self.dy

        self.dy += 0.15
        self.life -= 1

        return self.life > 0

    def draw(self):
        if self.life > 0:
            pygame.draw.circle(
                screen,
                self.color,
                (int(self.x), int(self.y)),
                self.radius
            )


# ============================================================
# MEMBUAT BACKGROUND BINTANG
# ============================================================
def create_stars():
    stars = []

    for _ in range(100):
        stars.append({
            "x": random.randint(0, WIDTH),
            "y": random.randint(0, HEIGHT),
            "size": random.choice([1, 1, 1, 2]),
            "speed": random.uniform(0.2, 0.8)
        })

    return stars


def update_and_draw_stars(stars):
    for star in stars:
        star["y"] += star["speed"]

        if star["y"] > HEIGHT:
            star["y"] = 0
            star["x"] = random.randint(0, WIDTH)

        pygame.draw.circle(
            screen,
            GRAY,
            (int(star["x"]), int(star["y"])),
            star["size"]
        )


# ============================================================
# MEMBUAT BRICK BERDASARKAN LEVEL
# ============================================================
def create_bricks(level):
    bricks = []

    columns = 10
    rows = 4 + level

    gap = 6
    brick_width = 70
    brick_height = 25

    total_width = columns * brick_width + (columns - 1) * gap
    start_x = (WIDTH - total_width) // 2
    start_y = 80

    for row in range(rows):
        for column in range(columns):
            x = start_x + column * (brick_width + gap)
            y = start_y + row * (brick_height + gap)

            color = BRICK_COLORS[
                row % len(BRICK_COLORS)
            ]

            # Level lebih tinggi menghasilkan brick lebih kuat
            if level == 1:
                health = 1

            elif level == 2:
                health = 2 if row < 2 else 1

            else:
                if row < 2:
                    health = 3
                elif row < 4:
                    health = 2
                else:
                    health = 1

            bricks.append(
                Brick(
                    x,
                    y,
                    brick_width,
                    brick_height,
                    health,
                    color
                )
            )

    return bricks


# ============================================================
# MEMBUAT EFEK PARTIKEL
# ============================================================
def create_particles(particles, x, y, color):
    for _ in range(15):
        particles.append(
            Particle(x, y, color)
        )


# ============================================================
# MENU UTAMA
# ============================================================
def show_menu(stars):
    while True:
        screen.fill(BLACK)
        update_and_draw_stars(stars)

        draw_center_text(
            "BLOCK BREAKER",
            title_font,
            CYAN,
            150
        )

        draw_center_text(
            "DELUXE",
            large_font,
            YELLOW,
            215
        )

        draw_center_text(
            "Tekan SPACE untuk mulai",
            medium_font,
            WHITE,
            330
        )

        draw_center_text(
            "Gerak: Panah kiri/kanan atau A dan D",
            small_font,
            GRAY,
            390
        )

        draw_center_text(
            "P = Pause | ESC = Keluar",
            small_font,
            GRAY,
            425
        )

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

                if event.key == pygame.K_ESCAPE:
                    return False


# ============================================================
# LAYAR PAUSE
# ============================================================
def show_pause():
    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    draw_center_text(
        "PAUSE",
        large_font,
        YELLOW,
        HEIGHT // 2 - 40
    )

    draw_center_text(
        "Tekan P untuk melanjutkan",
        small_font,
        WHITE,
        HEIGHT // 2 + 30
    )

    pygame.display.flip()


# ============================================================
# LAYAR AKHIR
# ============================================================
def show_end_screen(state, score, stars):
    while True:
        screen.fill(BLACK)
        update_and_draw_stars(stars)

        if state == "WIN":
            draw_center_text(
                "KAMU MENANG!",
                large_font,
                GREEN,
                180
            )

            draw_center_text(
                "Semua level berhasil diselesaikan",
                medium_font,
                WHITE,
                250
            )

        else:
            draw_center_text(
                "GAME OVER",
                large_font,
                RED,
                180
            )

            draw_center_text(
                "Nyawamu sudah habis",
                medium_font,
                WHITE,
                250
            )

        draw_center_text(
            f"Skor akhir: {score}",
            medium_font,
            YELLOW,
            315
        )

        draw_center_text(
            "Tekan R untuk bermain lagi",
            small_font,
            WHITE,
            390
        )

        draw_center_text(
            "Tekan ESC untuk keluar",
            small_font,
            GRAY,
            425
        )

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "RESTART"

                if event.key == pygame.K_ESCAPE:
                    return "QUIT"


