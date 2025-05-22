import pygame
import random
import sys
import time

pygame.init()

# Ekran ayarları
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basit Savaş Oyunu")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ENEMY_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# Saat
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Oyuncu ayarları
player = pygame.Rect(WIDTH // 2, HEIGHT - 50, 50, 30)
player_speed = 5
bullets = []

# Düşman ayarları
enemies = []
enemy_spawn_time = 1000
enemy_bullet_speed = 5
enemy_fire_rate = 2000
last_enemy_fire = pygame.time.get_ticks()

# Skor ve zaman
score = 0
last_hit_time = pygame.time.get_ticks()
start_time = pygame.time.get_ticks()

# Oyunun durumu
game_over = False
game_won = False

def reset_game():
    global player, bullets, enemies, score, last_hit_time, start_time, enemy_fire_rate, last_enemy_fire, game_over, game_won
    player.x = WIDTH // 2
    bullets = []
    enemies = []
    score = 0
    last_hit_time = pygame.time.get_ticks()
    start_time = pygame.time.get_ticks()
    enemy_fire_rate = 2000
    last_enemy_fire = pygame.time.get_ticks()
    game_over = False
    game_won = False

def create_enemy():
    x = random.randint(0, WIDTH - 40)
    enemy = pygame.Rect(x, 0, 40, 30)
    enemies.append((enemy, random.choice(ENEMY_COLORS)))

def fire_enemy_bullets():
    enemy_bullets = []
    for enemy, _ in enemies:
        bullet = pygame.Rect(enemy.centerx, enemy.bottom, 5, 10)
        enemy_bullets.append(bullet)
    return enemy_bullets

def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

enemy_bullets = []
next_difficulty_increase = pygame.time.get_ticks() + 10000

# Ana oyun döngüsü
running = True
reset_game()

while running:
    screen.fill(BLACK)

    # Etkinlikler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player.x += player_speed
        if keys[pygame.K_SPACE]:
            if len(bullets) < 5:  # spam engelleme
                bullet = pygame.Rect(player.centerx, player.y, 5, 10)
                bullets.append(bullet)

        # Oyuncu mermilerini hareket ettir
        for bullet in bullets[:]:
            bullet.y -= 10
            if bullet.y < 0:
                bullets.remove(bullet)

        # Mermilerle düşmanları kontrol et
        for bullet in bullets[:]:
            for enemy, color in enemies[:]:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove((enemy, color))
                    score += 100
                    break

        # Düşman oluştur
        if random.randint(0, 30) == 0:
            create_enemy()

        # Düşmanları hareket ettir
        for enemy, _ in enemies:
            enemy.y += 2
            if enemy.y > HEIGHT:
                enemies.remove((enemy, _))

        # Düşman ateşi
        now = pygame.time.get_ticks()
        if now - last_enemy_fire > enemy_fire_rate:
            enemy_bullets.extend(fire_enemy_bullets())
            last_enemy_fire = now

        # Zorluk artışı
        if now > next_difficulty_increase:
            enemy_fire_rate = max(500, int(enemy_fire_rate * 0.8))
            next_difficulty_increase = now + 10000

        # Düşman mermilerini hareket ettir
        for bullet in enemy_bullets[:]:
            bullet.y += enemy_bullet_speed
            if bullet.colliderect(player):
                game_over = True
                game_won = False
            if bullet.y > HEIGHT:
                enemy_bullets.remove(bullet)

        # Kazanma durumu
        if now - last_hit_time > 60000:
            game_over = True
            game_won = True

        # Çizim
        pygame.draw.rect(screen, WHITE, player)
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)
        for bullet in enemy_bullets:
            pygame.draw.rect(screen, (255, 255, 0), bullet)
        for enemy, color in enemies:
            pygame.draw.rect(screen, color, enemy)

        draw_text(f"Skor: {score}", 10, HEIGHT - 40)

    else:
        message = "Kazandın!" if game_won else "Kaybettin!"
        draw_text(message, WIDTH // 2 - 80, HEIGHT // 2 - 50)
        draw_text("Tekrar oynamak ister misin? (E/H)", WIDTH // 2 - 200, HEIGHT // 2)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            reset_game()
        elif keys[pygame.K_h]:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()