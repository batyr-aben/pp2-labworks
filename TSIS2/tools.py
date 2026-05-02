import pygame
from collections import deque


def draw_shape(surface, shape, color, start, end, width):
    if start is None or end is None:
        return

    x1, y1 = start[:2]
    x2, y2 = end[:2]

    left = min(x1, x2)
    top = min(y1, y2)
    w = abs(x2 - x1)
    h = abs(y2 - y1)

    if shape == "line":
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), width)

    elif shape == "rectangle":
        pygame.draw.rect(surface, color, (left, top, w, h), width)

    elif shape == "circle":
        radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
        pygame.draw.circle(surface, color, (x1, y1), radius, width)

    elif shape == "square":
        size = min(w, h)
        pygame.draw.rect(surface, color, (left, top, size, size), width)

    elif shape == "right_triangle":
        points = [(x1, y2), (x1, y1), (x2, y2)]
        pygame.draw.polygon(surface, color, points, width)

    elif shape == "equilateral_triangle":
        points = [(x1, y2), ((x1 + x2) // 2, y1), (x2, y2)]
        pygame.draw.polygon(surface, color, points, width)

    elif shape == "rhombus":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
        pygame.draw.polygon(surface, color, points, width)


def flood_fill(surface, start, fill_color):
    w, h = surface.get_size()
    x, y = start[:2]

    if not (0 <= x < w and 0 <= y < h):
        return

    target_color = surface.get_at((x, y))
    fill_color = pygame.Color(*fill_color)

    if target_color == fill_color:
        return

    q = deque()
    q.append((x, y))

    while q:
        px, py = q.popleft()

        if px < 0 or px >= w or py < 0 or py >= h:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), fill_color)

        q.append((px + 1, py))
        q.append((px - 1, py))
        q.append((px, py + 1))
        q.append((px, py - 1))
