import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

enemy = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemy.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(0.6)
    enemyY_change.append(0)

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
background = pygame.image.load('space.jpg')
mixer.music.load('Background.wav')
mixer.music.play(-1)
background = pygame.transform.scale(background, (800, 600))
pygame.display.set_icon(icon)
guns = pygame.image.load('guns.png')

bullet = pygame.image.load('bullet.png')
playerX = 368
playerY = 480
playerX_change = 0

bulletX = 0
bulletY = 480
bulletY_change = 1.6
bullet_state = "ready"

score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 600
textY = 32

over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (220, 300))


def show_score(x, y):
    score_value = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))


def player(x, y):
    screen.blit(guns, (x, y))


def enemies(x, y, i):
    screen.blit(enemy[i], (x, y))


def firebullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 20, y + 10))


def collide(x1, y1, x2, y2):
    distance = math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((155, 100, 55))
    screen.blit(background, (0, 0))

    player(playerX, playerY)
    show_score(textX, textY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 0.5
            if event.key == pygame.K_RIGHT:
                playerX_change += 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('Shot.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    firebullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736
    for i in range(num_enemies):
        if enemyY[i] > 420:
            for j in range(num_enemies):
                enemyY[j] = 1500
            game_over()
            mixer.music.stop()
            Over_Sound = mixer.Sound('Game over.wav')
            Over_Sound.play()
            break
        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]
        enemyY_change[i] = 0
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = (-1) * (enemyX_change[i])
            enemyY_change[i] += 50
        if enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] = (-1) * (enemyX_change[i])
            enemyY_change[i] += 50
        collision = collide(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            enemy_Sound = mixer.Sound('Hit.wav')
            enemy_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 200)
        enemies(enemyX[i], enemyY[i], i)

    if (bullet_state == "fire"):
        firebullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY < 0:
        bullet_state = "ready"
        bulletY = 480

    pygame.display.update()
