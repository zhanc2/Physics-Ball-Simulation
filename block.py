import math

import pygame


class Block:
    def __init__(self, x: int, y: int, color: tuple):
        self.x = x
        self.y = y
        self.color = color


class Rectangle(Block):
    def __init__(self, x: int, y: int, color: tuple, x_size: int, y_size: int):
        super(Rectangle, self).__init__(x, y, color)
        self.x_size = x_size
        self.y_size = y_size
        self.rect = pygame.Rect(x, y, x_size, y_size)

    def display(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)


class Triangle(Block):
    def __init__(self, x: int, y: int, color: tuple, pt2: tuple, pt3: tuple, right: bool,
                 slanted_edge: tuple, facing: int):
        super(Triangle, self).__init__(x, y, color)
        self.facing = facing
        self.slanted_edge = slanted_edge
        self.right = right
        self.pt1 = [x, y]
        self.pt2 = pt2
        self.pt3 = pt3
        self.pts = [self.pt1, self.pt2, self.pt3]
        furthest_left = min(x, min(pt2[0], pt3[0]))
        furthest_right = max(x, max(pt2[0], pt3[0]))
        furthest_up = min(y, min(pt2[1], pt3[1]))
        furthest_down = max(y, max(pt2[1], pt3[1]))
        self.rect = pygame.Rect(furthest_left, furthest_up, furthest_right-furthest_left, furthest_down-furthest_up)
        self.hypotenuse = math.sqrt((self.pts[slanted_edge[0]][0]-self.pts[slanted_edge[1]][0])**2 +
                                    (self.pts[slanted_edge[0]][1]-self.pts[slanted_edge[1]][1])**2)
        self.vertical_edge = furthest_down - furthest_up
        self.horizontal_edge = furthest_right - furthest_left

    def display(self, screen: pygame.Surface):
        pygame.draw.polygon(screen, self.color, (self.pt1, self.pt2, self.pt3))


class CurvedRamp(Block):
    def __init__(self, x: int, y: int, color: tuple, pt1: tuple, pt2: tuple, curve_radius: int):
        super(CurvedRamp, self).__init__(x, y, color)
        self.pt1 = pt1
        self.pt2 = pt2
        self.curve_radius = curve_radius
