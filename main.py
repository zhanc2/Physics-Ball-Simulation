import pygame
from ball_simulation import BallSimulation

pygame.init()
pygame.font.init()
pygame.display.init()

x, y = 1300, 1000
screen = pygame.display.set_mode((x, y))

dt = 0
clock = pygame.time.Clock()

ball_simulation = BallSimulation(1300, 1000, -500)

new_font = pygame.font.SysFont("Arial", 30)

running = True

while running:
    screen.fill((255, 255, 255))
    dt = clock.tick(120)

    # e = new_font.render("ball x: "+str(ball_simulation.ball.x + 25), False, (0, 0, 0))
    # f = new_font.render("ball y: " + str(ball_simulation.ball.y + 25), False, (0, 0, 0))
    a = new_font.render("x vel: " + str(ball_simulation.ball.x_vel), False, (0, 0, 0))
    b = new_font.render("y vel: " + str(ball_simulation.ball.y_vel), False, (0, 0, 0))

    events = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()
    mouse_move = pygame.mouse.get_rel()
    mouse_pressed = pygame.mouse.get_pressed()

    ball_simulation.display_rect_blocks(screen)
    ball_simulation.display_triangle_blocks(screen)
    ball_simulation.do_ball(dt, screen, mouse_pos, mouse_move, mouse_pressed, events)

    # screen.blit(e, (20, 20))
    # screen.blit(f, (20, 50))
    screen.blit(a, (20, 20))
    screen.blit(b, (20, 50))

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
