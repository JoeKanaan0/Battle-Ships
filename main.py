import pygame
import os
pygame.font.init()
from pygame import mixer
pygame.mixer.init()

WIDTH = 900
HEIGHT = 600

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
SCALED_RED = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP = pygame.transform.rotate(SCALED_RED, (90))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
SCALED_YELLOW = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
YELLOW_SPACESHIP = pygame.transform.rotate(SCALED_YELLOW, (270))

SPACE_IMAGE = pygame.image.load(os.path.join("Assets", "space.png"))
SPACE = pygame.transform.scale(SPACE_IMAGE, (900, 600))

mixer.music.load(os.path.join("Assets", 'background.wav'))
mixer.music.play(-1)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.init()

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
            explosion_Sound = mixer.Sound('Assets\explosion.wav')
            explosion_Sound.play()
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)
    
    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            yellow_bullets.remove(bullet) 
            pygame.event.post(pygame.event.Event(RED_HIT))
            explosion_Sound = mixer.Sound('Assets\explosion.wav')
            explosion_Sound.play()
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)

def draw(red, yellow, red_bullets, yellow_bullets, RED, YELLOW, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    WIN.blit((RED_SPACESHIP), (red.x, red.y))
    WIN.blit((YELLOW_SPACESHIP), (yellow.x, yellow.y))
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.draw.rect(WIN, BLACK, BORDER)
    pygame.display.update()

def red_movement(red, keys_pressed):
    if keys_pressed[pygame.K_a] and red.x > 0:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x < BORDER.x - SPACESHIP_HEIGHT:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_s] and red.y < HEIGHT:  # DOWN
        red.y += VEL
    if keys_pressed[pygame.K_w] and red.y - SPACESHIP_WIDTH > 0:  # UP
        red.y -= VEL

def yellow_movement(yellow, keys_pressed):
    if keys_pressed[pygame.K_LEFT] and yellow.x - 10 > BORDER.x:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and yellow.x + SPACESHIP_HEIGHT < WIDTH:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_DOWN]  and yellow.y < HEIGHT:  # DOWN
        yellow.y += VEL
    if keys_pressed[pygame.K_UP] and yellow.y - SPACESHIP_WIDTH > 0:  # UP
        yellow.y -= VEL

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(200, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    running = True
    clock = pygame.time.Clock()

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + SPACESHIP_WIDTH, red.y + SPACESHIP_WIDTH//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    bullet_Sound = mixer.Sound('Assets\laser.wav')
                    bullet_Sound.play()

                elif event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x, yellow.y + SPACESHIP_WIDTH//2 , 10, 5)
                    yellow_bullets.append(bullet)
                    bullet_Sound = mixer.Sound('Assets\laser.wav')
                    bullet_Sound.play()

            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1 
                
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            main()
                
        keys_pressed = pygame.key.get_pressed()
        draw(red, yellow, red_bullets, yellow_bullets, RED, YELLOW, red_health, yellow_health)
        red_movement(red, keys_pressed)
        yellow_movement(yellow, keys_pressed)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

if __name__ == "__main__":
    main()