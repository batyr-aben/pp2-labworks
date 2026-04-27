import pygame
import random
import sys

SCREEN_W, SCREEN_H = 480, 700
FPS               = 60

ROAD_LEFT  = 80
ROAD_RIGHT = 400

WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0)
GREY       = (80,  80,  80)
DARK_GREY  = (50,  50,  50)
YELLOW     = (255, 220, 0)
RED        = (220, 40,  40)
BLUE       = (30,  120, 255)
GREEN      = (50,  200, 80)
ORANGE     = (255, 160, 0)
SILVER     = (192, 192, 192)

COINS_PER_SPEEDUP = 5
SPEEDUP_AMOUNT    = 0.5

COIN_TYPES = [
    {"label": "BRONZE", "value": 1, "colour": (180, 100, 30), "weight": 60},
    {"label": "SILVER", "value": 2, "colour": SILVER,         "weight": 30},
    {"label": "GOLD",   "value": 3, "colour": YELLOW,         "weight": 10},
]

def weighted_choice(items):
    total   = sum(i["weight"] for i in items)
    roll    = random.randint(1, total)
    running = 0
    for item in items:
        running += item["weight"]
        if roll <= running:
            return item
    return items[-1]

class PlayerCar:
    WIDTH  = 40
    HEIGHT = 70

    def __init__(self):
        self.rect  = pygame.Rect(
            (ROAD_LEFT + ROAD_RIGHT) // 2 - self.WIDTH // 2,
            SCREEN_H - self.HEIGHT - 20,
            self.WIDTH, self.HEIGHT
        )
        self.colour = BLUE
        self.speed  = 5

    def update(self, keys):
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > ROAD_LEFT:
            self.rect.x -= int(self.speed)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < ROAD_RIGHT:
            self.rect.x += int(self.speed)

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect, border_radius=6)
        wshield = pygame.Rect(self.rect.x + 5, self.rect.y + 8, self.WIDTH - 10, 18)
        pygame.draw.rect(surface, (180, 220, 255), wshield, border_radius=3)
        for wx, wy in [(self.rect.x - 5, self.rect.y + 8),
                       (self.rect.right - 5, self.rect.y + 8),
                       (self.rect.x - 5, self.rect.bottom - 22),
                       (self.rect.right - 5, self.rect.bottom - 22)]:
            pygame.draw.rect(surface, BLACK, (wx, wy, 10, 14), border_radius=3)

class EnemyCar:
    WIDTH  = 40
    HEIGHT = 70

    def __init__(self, base_speed):
        self.rect = pygame.Rect(
            random.randint(ROAD_LEFT, ROAD_RIGHT - self.WIDTH),
            -self.HEIGHT,
            self.WIDTH, self.HEIGHT
        )
        self.colour = random.choice([RED, GREEN, ORANGE, (150, 50, 200)])
        self.speed  = base_speed + random.uniform(-0.3, 0.3)

    def update(self):
        self.rect.y += self.speed

    def is_off_screen(self):
        return self.rect.top > SCREEN_H

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect, border_radius=6)
        wshield = pygame.Rect(self.rect.x + 5, self.rect.y + 8, self.WIDTH - 10, 18)
        pygame.draw.rect(surface, (255, 230, 180), wshield, border_radius=3)
        for wx, wy in [(self.rect.x - 5, self.rect.y + 8),
                       (self.rect.right - 5, self.rect.y + 8),
                       (self.rect.x - 5, self.rect.bottom - 22),
                       (self.rect.right - 5, self.rect.bottom - 22)]:
            pygame.draw.rect(surface, BLACK, (wx, wy, 10, 14), border_radius=3)

class Coin:
    RADIUS = 12

    def __init__(self, speed):
        self.ctype  = weighted_choice(COIN_TYPES)
        self.colour = self.ctype["colour"]
        self.value  = self.ctype["value"]
        self.label  = self.ctype["label"]
        self.speed  = speed
        self.rect   = pygame.Rect(
            random.randint(ROAD_LEFT + self.RADIUS, ROAD_RIGHT - self.RADIUS),
            -self.RADIUS * 2,
            self.RADIUS * 2, self.RADIUS * 2
        )

    def update(self):
        self.rect.y += self.speed

    def is_off_screen(self):
        return self.rect.top > SCREEN_H

    def draw(self, surface):
        cx = self.rect.centerx
        cy = self.rect.centery
        pygame.draw.circle(surface, self.colour, (cx, cy), self.RADIUS)
        pygame.draw.circle(surface, BLACK, (cx, cy), self.RADIUS, 2)
        font_s = pygame.font.SysFont("arial", 11, bold=True)
        txt    = font_s.render(str(self.value), True, BLACK)
        surface.blit(txt, txt.get_rect(center=(cx, cy)))

class Road:
    STRIPE_W = 8
    STRIPE_H = 40
    GAP      = 30

    def __init__(self):
        self.offset = 0
        self.speed  = 4

    def update(self):
        self.offset = (self.offset + self.speed) % (self.STRIPE_H + self.GAP)

    def draw(self, surface):
        pygame.draw.rect(surface, DARK_GREY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, SCREEN_H))
        pygame.draw.line(surface, YELLOW, (ROAD_LEFT, 0),  (ROAD_LEFT, SCREEN_H),  4)
        pygame.draw.line(surface, YELLOW, (ROAD_RIGHT, 0), (ROAD_RIGHT, SCREEN_H), 4)
        cx = (ROAD_LEFT + ROAD_RIGHT) // 2
        y  = -self.STRIPE_H + self.offset
        while y < SCREEN_H:
            pygame.draw.rect(surface, WHITE, (cx - self.STRIPE_W // 2, y, self.STRIPE_W, self.STRIPE_H))
            y += self.STRIPE_H + self.GAP

class RacerGame:
    ENEMY_BASE_SPEED  = 3.0
    SPAWN_ENEMY_EVERY = 90
    SPAWN_COIN_EVERY  = 60

    def __init__(self):
        pygame.init()
        self.screen  = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Racer – Practice 11")
        self.clock   = pygame.time.Clock()
        self.font    = pygame.font.SysFont("arial", 22, bold=True)
        self.big_font= pygame.font.SysFont("arial", 48, bold=True)
        self.reset()

    def reset(self):
        self.player       = PlayerCar()
        self.road         = Road()
        self.enemies      = []
        self.coins        = []
        self.score        = 0
        self.coins_total  = 0
        self.enemy_speed  = self.ENEMY_BASE_SPEED
        self.frame        = 0
        self.running      = True
        self.game_over    = False
        self.next_speedup = COINS_PER_SPEEDUP

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self._handle_events()
            if not self.game_over:
                self._update()
            self._draw()
        pygame.quit()
        sys.exit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.reset()
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def _update(self):
        self.frame += 1
        keys = pygame.key.get_pressed()

        self.road.update()
        self.player.update(keys)

        if self.frame % self.SPAWN_ENEMY_EVERY == 0:
            self.enemies.append(EnemyCar(self.enemy_speed))

        if self.frame % self.SPAWN_COIN_EVERY == 0:
            self.coins.append(Coin(self.enemy_speed))

        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
            elif self.player.rect.colliderect(enemy.rect):
                self.game_over = True

        for coin in self.coins[:]:
            coin.update()
            if coin.is_off_screen():
                self.coins.remove(coin)
            elif self.player.rect.colliderect(coin.rect):
                self.score       += coin.value
                self.coins_total += 1
                self.coins.remove(coin)

                if self.coins_total >= self.next_speedup:
                    self.enemy_speed  += SPEEDUP_AMOUNT
                    self.road.speed   += SPEEDUP_AMOUNT
                    self.player.speed += 0.3
                    self.next_speedup += COINS_PER_SPEEDUP

    def _draw(self):
        self.screen.fill(GREEN)
        self.road.draw(self.screen)

        for coin in self.coins:
            coin.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.player.draw(self.screen)
        self._draw_hud()

        if self.game_over:
            self._draw_game_over()

        pygame.display.flip()

    def _draw_hud(self):
        hud = pygame.Surface((230, 100), pygame.SRCALPHA)
        hud.fill((0, 0, 0, 140))
        self.screen.blit(hud, (5, 5))

        coins_txt = self.font.render(f"Coins : {self.coins_total}  →  {self.next_speedup}", True, SILVER)
        score_txt = self.font.render(f"Score : {self.score}", True, YELLOW)
        espd_txt  = self.font.render(f"Enemy : {self.enemy_speed:.1f} px/f", True, (255, 100, 100))
        pspd_txt  = self.font.render(f"You   : {self.player.speed:.1f} px/f", True, (100, 200, 255))

        self.screen.blit(coins_txt, (10, 8))
        self.screen.blit(score_txt, (10, 30))
        self.screen.blit(espd_txt,  (10, 52))
        self.screen.blit(pspd_txt,  (10, 74))

        lx, ly = SCREEN_W - 150, SCREEN_H - 80
        for ct in COIN_TYPES:
            pygame.draw.circle(self.screen, ct["colour"], (lx + 10, ly + 8), 8)
            pygame.draw.circle(self.screen, BLACK,        (lx + 10, ly + 8), 8, 1)
            lbl = self.font.render(f"{ct['label']} +{ct['value']}", True, ct["colour"])
            self.screen.blit(lbl, (lx + 24, ly))
            ly += 24

    def _draw_game_over(self):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        go_txt   = self.big_font.render("GAME OVER", True, RED)
        sc_txt   = self.font.render(f"Final Score: {self.score}", True, YELLOW)
        rest_txt = self.font.render("Press  R  to Restart   |   ESC to Quit", True, WHITE)

        self.screen.blit(go_txt,   go_txt.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 50)))
        self.screen.blit(sc_txt,   sc_txt.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 10)))
        self.screen.blit(rest_txt, rest_txt.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 50)))

if __name__ == "__main__":
    game = RacerGame()
    game.run()
