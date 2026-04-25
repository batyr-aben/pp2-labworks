

import pygame
import random
import sys

pygame.init()


SCREEN_W, SCREEN_H = 400, 600
FPS = 60


ROAD_LEFT = 60
ROAD_RIGHT = 340


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (90, 90, 90)
YELLOW = (255, 215, 0)
RED = (210, 30, 30)
BLUE = (30, 90, 210)
GREEN = (0, 180, 0)


screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Racer (Simplified)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)


CAR_W, CAR_H = 38, 68

def random_lane_x():
    
    lane = random.randint(0, 2)  
    lane_width = (ROAD_RIGHT - ROAD_LEFT) // 3  
    return ROAD_LEFT + lane * lane_width + (lane_width - CAR_W) // 2


player_x = SCREEN_W // 2 - CAR_W // 2
player_y = SCREEN_H - 110
player_speed = 5

def draw_player():
    pygame.draw.rect(screen, BLUE, (player_x, player_y, CAR_W, CAR_H), border_radius=6)
    pygame.draw.rect(screen, WHITE, (player_x + 5, player_y + 8, CAR_W - 10, 18))
    pygame.draw.rect(screen, WHITE, (player_x + 5, player_y + CAR_H - 22, CAR_W - 10, 12))

def get_player_rect():
    return pygame.Rect(player_x + 4, player_y + 4, CAR_W - 8, CAR_H - 8)


enemies = []
enemy_timer = 0

def spawn_enemy(speed):
    enemy = {
        'x': random_lane_x(),
        'y': -CAR_H,
        'speed': speed,
        'color': random.choice([RED, (180, 90, 0), (140, 0, 140)])
    }
    enemies.append(enemy)

def update_enemies(speed):
    global score, game_over
    for enemy in enemies[:]: 
        enemy['y'] += enemy['speed']
        
       
        if enemy['y'] > SCREEN_H:
            enemies.remove(enemy)
            score += 1  
            continue
        
        enemy_rect = pygame.Rect(enemy['x'] + 4, enemy['y'] + 4, CAR_W - 8, CAR_H - 8)
        if enemy_rect.colliderect(get_player_rect()):
            game_over = True

def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, enemy['color'], (enemy['x'], enemy['y'], CAR_W, CAR_H), border_radius=6)
        pygame.draw.rect(screen, WHITE, (enemy['x'] + 5, enemy['y'] + CAR_H - 22, CAR_W - 10, 12))


coins = []
coin_timer = 0
coin_count = 0

def spawn_coin(speed):
    coin_radius = 11
    coin = {
        'x': random.randint(ROAD_LEFT + coin_radius + 2, ROAD_RIGHT - coin_radius - 2),
        'y': -coin_radius,
        'speed': speed,
        'radius': coin_radius
    }
    coins.append(coin)

def update_coins():
    global coin_count
    for coin in coins[:]:
        coin['y'] += coin['speed']
        
        if coin['y'] - coin['radius'] > SCREEN_H:
            coins.remove(coin)
            continue
        
     
        coin_rect = pygame.Rect(coin['x'] - coin['radius'], coin['y'] - coin['radius'], 
                                coin['radius'] * 2, coin['radius'] * 2)
        if coin_rect.colliderect(get_player_rect()):
            coins.remove(coin)
            coin_count += 1

def draw_coins():
    for coin in coins:
        pygame.draw.circle(screen, YELLOW, (coin['x'], coin['y']), coin['radius'])
        text = font.render("$", True, (200, 160, 0))
        screen.blit(text, (coin['x'] - 5, coin['y'] - 8))


road_offset = 0
road_speed = 5
LINE_H = 55
LINE_GAP = 35
SEGMENT = LINE_H + LINE_GAP

def update_road():
    global road_offset
    road_offset = (road_offset + road_speed) % SEGMENT

def draw_road():
    
    screen.fill(GREEN)
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, SCREEN_H))
    
    
    pygame.draw.rect(screen, WHITE, (ROAD_LEFT - 4, 0, 4, SCREEN_H))
    pygame.draw.rect(screen, WHITE, (ROAD_RIGHT, 0, 4, SCREEN_H))
    
   
    lane_width = (ROAD_RIGHT - ROAD_LEFT) // 3
    for lane in range(1, 3):  
        x = ROAD_LEFT + lane_width * lane - 2
        y = road_offset - SEGMENT
        while y < SCREEN_H:
            pygame.draw.rect(screen, WHITE, (x, y, 4, LINE_H))
            y += SEGMENT


def draw_hud():
    score_text = font.render(f"Score: {score}", True, WHITE)
    coin_text = font.render(f"Coins: {coin_count}", True, YELLOW)
    screen.blit(score_text, (10, 8))
    screen.blit(coin_text, (SCREEN_W - coin_text.get_width() - 10, 8))

def draw_game_over():
    
    overlay = pygame.Surface((SCREEN_W, SCREEN_H))
    overlay.set_alpha(160)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    
    texts = [
        ("GAME OVER", RED, 48),
        (f"Score: {score}", WHITE, 22),
        (f"Coins: {coin_count}", YELLOW, 22),
        ("Press R to restart, Q to quit", WHITE, 18)
    ]
    
    y = 200
    for text, color, size in texts:
        f = pygame.font.SysFont("Arial", size, bold=(size > 22))
        rendered = f.render(text, True, color)
        screen.blit(rendered, (SCREEN_W//2 - rendered.get_width()//2, y))
        y += rendered.get_height() + 15


score = 0
base_speed = 4
game_over = False


running = True
while running:
    clock.tick(FPS)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:  
                
                enemies.clear()
                coins.clear()
                score = 0
                coin_count = 0
                game_over = False
                player_x = SCREEN_W // 2 - CAR_W // 2
                road_offset = 0
                enemy_timer = 0
                coin_timer = 0
            if event.key == pygame.K_q:  
                pygame.quit()
                sys.exit()
    
    if not game_over:
       
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > ROAD_LEFT:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x + CAR_W < ROAD_RIGHT:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y + CAR_H < SCREEN_H:
            player_y += player_speed
        
        
        current_speed = base_speed + score // 5
        road_speed = 5 + score // 8
        
        
        update_road()
        
       
        enemy_timer += 1
        if enemy_timer >= random.randint(55, 80):
            spawn_enemy(current_speed)
            enemy_timer = 0
        
        
        coin_timer += 1
        if coin_timer >= random.randint(90, 180):
            spawn_coin(current_speed)
            coin_timer = 0
        
        
        update_enemies(current_speed)
        update_coins()
    

    draw_road()
    draw_enemies()
    draw_coins()
    draw_player()
    draw_hud()
    
    if game_over:
        draw_game_over()
    
    pygame.display.flip()
