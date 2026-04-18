import pygame
import os

class MusicPlayer:
    def __init__(self):
        
        
        self.playlist = [
            "music/track1.wav",
            "music/track2.wav"
        ]
        
        self.current_track = 0
        self.playing = False
        
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        
        
        self.font = pygame.font.Font(None, 36)
    
    def play(self):
       
        try:
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play()
            self.playing = True
        except Exception as e:
            print(f"Ошибка воспроизведения: {e}")
    
    def stop(self):
        
        pygame.mixer.music.stop()
        self.playing = False
    
    def next_track(self):
        
        self.current_track = (self.current_track + 1) % len(self.playlist)
        self.play()
    
    def previous_track(self):
        
        self.current_track = (self.current_track - 1) % len(self.playlist)
        self.play()
    
    def get_current_track_name(self):
       
        return os.path.basename(self.playlist[self.current_track])
    
    def draw_ui(self, screen):
        
        screen.fill(self.BLACK)
        
        
        track_text = self.font.render(
            f"Track: {self.get_current_track_name()}", 
            True, 
            self.WHITE
        )
        screen.blit(track_text, (50, 50))
        
        
        status = "PLAYING" if self.playing else "STOPPED"
        color = self.GREEN if self.playing else self.RED
        status_text = self.font.render(f"Status: {status}", True, color)
        screen.blit(status_text, (50, 100))
        
       
        controls = [
            "P - Play",
            "S - Stop",
            "N - Next track",
            "B - Previous track",
            "Q - Quit"
        ]
        
        y = 200
        for control in controls:
            text = self.font.render(control, True, self.WHITE)
            screen.blit(text, (50, y))
            y += 40
