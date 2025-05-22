import pygame
import random
import sys
import time

pygame.init()

# Ekran boyutu
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basit Araba Oyunu")

# Renkler
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Araba
car_width = 50
car_height = 100
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - car_height - 10
car_speed = 5

# Engel
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 5
obstacles = []

# Zamanlama
start_time = time.time()
last_speed_increase = 0

# Oyun kontrolü
game_over = False
game_win = False
font = pygame.font.SysFont(None, 55)

clock = pygame.time.Clock()

def draw_text(text, color, y_offset=0):
    render = font.render(text, True, color)
    rect = render.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(render, rect)

def spawn_obstacles(num):
    for _ in range(num):
        x = random.randint(0, WIDTH - obstacle_width)
        y = random.randint(-800, -50)
        obstacles.append(pygame.Rect(x, y, obstacle_width, obstacle_height))

spawn_obstacles(3)

while True:
    screen.fill(WHITE)
    elapsed = time.time() - start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over and not game_win:
        # Klavye kontrol
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 0:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < WIDTH - car_width:
            car_x += car_speed

        car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        pygame.draw.rect(screen, BLUE, car_rect)

        # Engelleri güncelle
        for obs in obstacles:
            obs.y += obstacle_speed
            pygame.draw.rect(screen, RED, obs)

            if car_rect.colliderect(obs):
                game_over = True

        # Engelleri yeniden doğur
        obstacles = [obs for obs in obstacles if obs.y < HEIGHT]
        while len(obstacles) < 3 + int(elapsed // 10):  # Hızla birlikte engel sayısı artsın
            spawn_obstacles(1)

        # Zamanla hız artır
        if elapsed >= 10 and last_speed_increase < 1:
            car_speed *= 1.25
            obstacle_speed *= 1.25
            last_speed_increase = 1
        elif elapsed >= 20 and last_speed_increase < 2:
            car_speed *= 1.25
            obstacle_speed *= 1.25
            last_speed_increase = 2
        elif elapsed >= 30 and not game_win:
            game_win = True

    # Kazanma veya kaybetme ekranı
    if game_over:
        draw_text("Kaybettin!", RED)
    elif game_win:
        draw_text("Kazandın!", GREEN)

    pygame.display.flip()
    clock.tick(60)