import pygame
import sys
from datetime import datetime
from tools import draw_shape, flood_fill

pygame.init()

WIDTH, HEIGHT = 1100, 700
TOOLBAR_HEIGHT = 60
CANVAS_RECT = pygame.Rect(0, TOOLBAR_HEIGHT, WIDTH, HEIGHT - TOOLBAR_HEIGHT)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2 Paint")

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill((255, 255, 255))

font = pygame.font.SysFont(None, 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)

current_color = BLACK
brush_size = 2
tool = "pencil"

drawing = False
start_pos = None
last_pos = None

text_mode = False
text_position = None
text_buffer = ""

color_palette = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 180, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 128, 0),
    (128, 0, 255),
]


def canvas_pos(pos):
    return pos[0], pos[1] - TOOLBAR_HEIGHT


def inside_canvas(pos):
    return CANVAS_RECT.collidepoint(pos)


def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    label = font.render(f"Tool: {tool} | Size: {brush_size}", True, BLACK)
    screen.blit(label, (10, 10))

    for i, color in enumerate(color_palette):
        rect = pygame.Rect(250 + i * 40, 10, 30, 30)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)


def save_canvas():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"paint_{timestamp}.png"
    pygame.image.save(canvas, filename)
    print(f"Saved: {filename}")


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()

            if text_mode:
                if event.key == pygame.K_RETURN:
                    rendered = font.render(text_buffer, True, current_color)
                    canvas.blit(rendered, text_position)
                    text_mode = False
                    text_buffer = ""

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_buffer = ""

                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]

                else:
                    text_buffer += event.unicode

            else:
                if event.key == pygame.K_s and mods & pygame.KMOD_CTRL:
                    save_canvas()

                elif event.key == pygame.K_1:
                    brush_size = 2
                elif event.key == pygame.K_2:
                    brush_size = 5
                elif event.key == pygame.K_3:
                    brush_size = 10

                elif event.key == pygame.K_p:
                    tool = "pencil"
                elif event.key == pygame.K_l:
                    tool = "line"
                elif event.key == pygame.K_r:
                    tool = "rectangle"
                elif event.key == pygame.K_c:
                    tool = "circle"
                elif event.key == pygame.K_q:
                    tool = "square"
                elif event.key == pygame.K_t:
                    tool = "right_triangle"
                elif event.key == pygame.K_e:
                    tool = "equilateral_triangle"
                elif event.key == pygame.K_h:
                    tool = "rhombus"
                elif event.key == pygame.K_f:
                    tool = "fill"
                elif event.key == pygame.K_g:
                    tool = "eraser"
                elif event.key == pygame.K_x:
                    tool = "text"

        if event.type == pygame.MOUSEBUTTONDOWN:
            if inside_canvas(event.pos):
                pos = canvas_pos(event.pos)

                if tool == "fill":
                    flood_fill(canvas, pos, current_color)

                elif tool == "text":
                    text_mode = True
                    text_position = pos
                    text_buffer = ""

                else:
                    drawing = True
                    start_pos = pos
                    last_pos = pos

                    if tool == "pencil":
                        pygame.draw.circle(canvas, current_color, pos, brush_size // 2)

                    elif tool == "eraser":
                        pygame.draw.circle(canvas, WHITE, pos, brush_size)

            else:
                for i, color in enumerate(color_palette):
                    rect = pygame.Rect(250 + i * 40, 10, 30, 30)
                    if rect.collidepoint(event.pos):
                        current_color = color

        if event.type == pygame.MOUSEMOTION:
            if drawing and inside_canvas(event.pos):
                pos = canvas_pos(event.pos)

                if tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, pos, brush_size)
                    last_pos = pos

                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, pos, brush_size * 2)
                    last_pos = pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and inside_canvas(event.pos):
                end_pos = canvas_pos(event.pos)

                if tool in [
                    "line",
                    "rectangle",
                    "circle",
                    "square",
                    "right_triangle",
                    "equilateral_triangle",
                    "rhombus",
                ]:
                    draw_shape(canvas, tool, current_color, start_pos, end_pos, brush_size)

            drawing = False

    screen.fill(WHITE)
    draw_toolbar()

    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    if drawing and tool in [
        "line",
        "rectangle",
        "circle",
        "square",
        "right_triangle",
        "equilateral_triangle",
        "rhombus",
    ]:
        if inside_canvas(pygame.mouse.get_pos()):
            preview = canvas.copy()
            current_pos = canvas_pos(pygame.mouse.get_pos())
            draw_shape(preview, tool, current_color, start_pos, current_pos, brush_size)
            screen.blit(preview, (0, TOOLBAR_HEIGHT))

    if text_mode:
        rendered = font.render(text_buffer, True, current_color)
        screen.blit(rendered, (text_position[0], text_position[1] + TOOLBAR_HEIGHT))

    pygame.display.flip()
    clock.tick(60)
