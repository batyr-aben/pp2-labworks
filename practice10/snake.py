import pygame
import random

pygame.init()


CELL = 20
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)


BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class SnakeGame:
    def __init__(self):
        self.reset()
    
    def reset(self):
        
        self.snake = [(WIDTH//2//CELL, HEIGHT//2//CELL)]
        for i in range(1, 3):
            self.snake.append((self.snake[0][0]-i, self.snake[0][1]))
        
        self.direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.create_food()
    
    def create_food(self):
        while True:
            x = random.randint(0, WIDTH//CELL - 1)
            y = random.randint(0, HEIGHT//CELL - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
    
    def move(self):
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        
        if (new_head[0] < 0 or new_head[0] >= WIDTH//CELL or
            new_head[1] < 0 or new_head[1] >= HEIGHT//CELL):
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        
        if new_head == self.food:
            self.score += 10
            self.create_food()
        else:
            self.snake.pop()
        
        
        if new_head in self.snake[1:]:
            self.game_over = True
    
    def draw(self):
        screen.fill(BLACK)
        
       
        for i, (x, y) in enumerate(self.snake):
            pygame.draw.rect(screen, GREEN, (x*CELL, y*CELL, CELL-2, CELL-2))
        
       
        pygame.draw.rect(screen, RED, (self.food[0]*CELL, self.food[1]*CELL, CELL-2, CELL-2))
        
    
        text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(text, (10, 10))
        
        if self.game_over:
            game_over_text = font.render("GAME OVER! Press SPACE", True, WHITE)
            screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2))

def main():
    game = SnakeGame()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game.game_over and event.key == pygame.K_SPACE:
                    game.reset()
                elif not game.game_over:
                    if event.key == pygame.K_UP and game.direction != (0, 1):
                        game.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and game.direction != (0, -1):
                        game.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and game.direction != (1, 0):
                        game.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and game.direction != (-1, 0):
                        game.direction = (1, 0)
        
        if not game.game_over:
            game.move()
        
        game.draw()
        pygame.display.flip()
        clock.tick(8)  
    
    pygame.quit()

if __name__ == "__main__":
    main()
