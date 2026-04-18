import pygame



BALL_RADIUS = 25
BALL_COLOR = (255, 0, 0)  
MOVE_DISTANCE = 20

def draw_ball(screen, x, y):
    
    pygame.draw.circle(screen, BALL_COLOR, (x, y), BALL_RADIUS)

def move_up(x, y, screen_height):
    
    new_y = y - MOVE_DISTANCE
    if new_y - BALL_RADIUS >= 0:  
        return x, new_y
    return x, y

def move_down(x, y, screen_height):
    
    new_y = y + MOVE_DISTANCE
    if new_y + BALL_RADIUS <= screen_height:  
        return x, new_y
    return x, y

def move_left(x, y):
    
    new_x = x - MOVE_DISTANCE
    if new_x - BALL_RADIUS >= 0: 
        return new_x, y
    return x, y

def move_right(x, y, screen_width):
   
    new_x = x + MOVE_DISTANCE
    if new_x + BALL_RADIUS <= screen_width:  
        return new_x, y
    return x, y
