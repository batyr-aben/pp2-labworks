import pygame
import sys
import ball 


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)  
FPS = 60

def main():
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Moving Ball Game")
    clock = pygame.time.Clock()
    
    
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    
    
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball_x, ball_y = ball.move_up(ball_x, ball_y, SCREEN_HEIGHT)
                elif event.key == pygame.K_DOWN:
                    ball_x, ball_y = ball.move_down(ball_x, ball_y, SCREEN_HEIGHT)
                elif event.key == pygame.K_LEFT:
                    ball_x, ball_y = ball.move_left(ball_x, ball_y)
                elif event.key == pygame.K_RIGHT:
                    ball_x, ball_y = ball.move_right(ball_x, ball_y, SCREEN_WIDTH)
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        
        screen.fill(BACKGROUND_COLOR)  
        ball.draw_ball(screen, ball_x, ball_y)  
        pygame.display.flip()  
        
        
        clock.tick(FPS)
    

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
