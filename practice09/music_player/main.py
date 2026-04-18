import pygame
from player import MusicPlayer

def main():
    
    pygame.init()
    pygame.mixer.init()
    
    
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")
    
    
    player = MusicPlayer()
    
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
       
        player.draw_ui(screen)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.previous_track()
                elif event.key == pygame.K_q:
                    running = False
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
