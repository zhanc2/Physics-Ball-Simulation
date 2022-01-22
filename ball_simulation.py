import pygame
from ball import Ball
from block import Rectangle, Triangle


class BallSimulation:
    def __init__(self, x_bound: int, y_bound: int, upper_bound: int):
        self.ball = Ball(x_bound, y_bound, 0.5, 0.5, 0.96, upper_bound)
        # self.rect_blocks = [Rectangle(1000, 700, (0, 0, 0), 300, 300)]
        self.rect_blocks = []
        self.triangle_blocks = [Triangle(0, 1000, (0, 0, 0), (0, 700), (600, 1000), True, (1, 2), 2), Triangle(700, 1000, (0, 0, 0), (1200, 700), (1200, 1000), True, (0, 1), 1)]
        # self.triangle_blocks = [Triangle(0, 700, (0, 0, 0), (0, 1000), (1000, 1000), True, (0, 2), 2)]

    def do_ball(self, delta_time: int, screen: pygame.Surface, mouse_pos: tuple, mouse_move: tuple,
                mouse_pressed: tuple, events: list[pygame.event]):
        self.ball.move(delta_time)
        self.ball.reset_pos(events)
        self.ball.boundary_physics()
        self.ball.mouse_pick(mouse_pos, mouse_pressed)
        self.ball.mouse_moving(mouse_pos, mouse_move)
        for block in self.rect_blocks:
            self.ball.rect_physics(block.rect)
        for block in self.triangle_blocks:
            self.ball.triangle_physics(block.rect, block.pts, block.facing, block.slanted_edge, block.hypotenuse,
                                       block.vertical_edge, block.horizontal_edge)
        self.ball.display(screen)

    def display_rect_blocks(self, screen: pygame.Surface):
        for block in self.rect_blocks:
            block.display(screen)

    def display_triangle_blocks(self, screen: pygame.Surface):
        for block in self.triangle_blocks:
            block.display(screen)
