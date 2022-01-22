import pygame
import math


class Ball:
    def __init__(self, x_bound: int, y_bound: int, bounce: float, gravity: float, friction: float, upper_bound: int):
        self.x_bound = x_bound
        self.y_bound = y_bound
        self.upper_bound = upper_bound
        self.x = 626
        self.y = 625
        self.bounce = bounce
        self.gravity = gravity
        self.x_vel = 0
        self.y_vel = 0
        self.size = 50
        self.held = False
        self.friction = friction
        self.color = (40, 100, 240)
        self.dis = 0
        self.fromRamp = 0

    def display(self, screen: pygame.display):
        pygame.draw.ellipse(screen, self.color, pygame.Rect(self.x, self.y, self.size, self.size))
        pygame.draw.ellipse(screen, (0, 0, 0), pygame.Rect(self.x+self.size/2-2, self.y+self.size/2-2, 4, 4))
        if self.fromRamp:
            self.color = (255, 0, 0)
        else:
            self.color = (0, 0, 0)

    def reset_pos(self, events: list[pygame.event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.x = self.x_bound/2 - self.size/2
                    self.y = self.y_bound/2 - self.size/2
                    self.x_vel = 0
                    self.y_vel = 0
                    return
                if event.key == pygame.K_x:
                    self.x = 200
                    self.y = 500
                    self.x_vel = 30
                    self.y_vel = 30
                    return
                if event.key == pygame.K_y:
                    self.x = 1100
                    self.y = 500
                    self.x_vel = -30
                    self.y_vel = 30
                    return
                if event.key == pygame.K_a:
                    self.x = 400
                    self.y = 200
                    self.x_vel = 0
                    self.y_vel = 0
                    return
                if event.key == pygame.K_d:
                    self.x = 900
                    self.y = 200
                    self.x_vel = 0
                    self.y_vel = 0
                    return
                if event.key == pygame.K_z:
                    self.x = 675
                    self.y = 730
                    self.x_vel = 10
                    self.y_vel = 10
                    return

    def move(self, dt: int):
        if not self.held:
            self.x += self.x_vel * (dt / 15)
            self.y += self.y_vel * (dt / 15)
            if self.fromRamp < 0:
                self.y_vel += self.gravity

    def boundary_physics(self):
        if self.x + self.size > self.x_bound:
            self.x = self.x_bound - self.size
            if abs(self.x_vel) > 5:
                self.x_vel *= -self.bounce
            else:
                self.x_vel = 0
        elif self.x < 0:
            self.x = 0
            if abs(self.x_vel) > 5:
                self.x_vel *= -self.bounce
            else:
                self.x_vel = 0

        if self.y+self.size > self.y_bound:
            self.y = self.y_bound-self.size
            if abs(self.x_vel) < 0.001:
                self.x_vel = 0
            else:
                self.x_vel *= self.friction
            if abs(self.y_vel) > 5:
                self.y_vel *= -self.bounce
            else:
                self.y_vel = 0
        elif self.y < self.upper_bound:
            self.y = self.upper_bound
            if abs(self.x_vel) < 0.001:
                self.x_vel = 0
            else:
                self.x_vel *= self.friction
            if abs(self.y_vel) > 5:
                self.y_vel *= -self.bounce
            else:
                self.y_vel = 0

        # if self.x_vel < 0.5:
        #     self.x_vel = 0

    @staticmethod
    def clamp(num: float, min_value: float, max_value: float) -> float:
        return max(min(num, max_value), min_value)

    @staticmethod
    def area_triangle(pts: list[tuple]) -> float:
        return abs(pts[0][0] * (pts[1][1]-pts[2][1]) + pts[1][0] * (pts[2][1]-pts[0][1]) +
                   pts[2][0] * (pts[0][1]-pts[1][1]))/2

    def check_if_point_in_triangle(self, triangle_pts: list[tuple], pt: tuple) -> bool:
        area_total = self.area_triangle(triangle_pts)

        area1 = self.area_triangle([pt, triangle_pts[1], triangle_pts[2]])
        area2 = self.area_triangle([triangle_pts[0], pt, triangle_pts[2]])
        area3 = self.area_triangle([triangle_pts[0], triangle_pts[1], pt])

        return (area1 + area2 + area3) == area_total

    def find_sector(self, rect: pygame.Rect, point: tuple, shape_type: int) -> int:
        if point[0] > rect[0]:
            if point[0] < rect[0]+rect[2]:
                if point[1] < rect[1]:
                    return 2
                elif point[1] > rect[1]+rect[3]:
                    return 8
                else:
                    if shape_type == 0:
                        if point[0] > rect[0]+rect[2]/2:
                            if point[1] > rect[1]+rect[3]/2:
                                if self.check_if_point_in_triangle([(rect[0]+rect[2]/2, rect[1]+rect[3]/2),
                                                                    (rect[0]+rect[2], rect[1]),
                                                                    (rect[0]+rect[2], rect[1]+rect[3])], point):
                                    return 5
                                else:
                                    return 8
                            else:
                                if self.check_if_point_in_triangle([(rect[0]+rect[2]/2, rect[1]+rect[3]/2),
                                                                    (rect[0]+rect[2], rect[1]),
                                                                    (rect[0]+rect[2], rect[1]+rect[3])], point):
                                    return 5
                                else:
                                    return 2
                        else:
                            if point[1] > rect[1]+rect[3]/2:
                                if self.check_if_point_in_triangle([(rect[0]+rect[2]/2, rect[1]+rect[3]/2),
                                                                    (rect[0], rect[1]),
                                                                    (rect[0], rect[1]+rect[3])], point):
                                    return 4
                                else:
                                    return 8
                            else:
                                if self.check_if_point_in_triangle([(rect[0]+rect[2]/2, rect[1]+rect[3]/2),
                                                                    (rect[0], rect[1]),
                                                                    (rect[0], rect[1]+rect[3])], point):
                                    return 4
                                else:
                                    return 2
                    return 0
            elif point[0] > rect[0]+rect[2]:
                if point[1] < rect[1]:
                    return 3
                elif point[1] > rect[1]:
                    if point[1] < rect[1]+rect[3]:
                        return 5
                    elif point[1] > rect[1]+rect[3]:
                        return 9
                    else:
                        return 0
                else:
                    return 0
            else:
                return 0
        else:
            if point[1] < rect[1]:
                return 1
            elif point[1] > rect[1]:
                if point[1] < rect[1]+rect[3]:
                    return 4
                elif point[1] > rect[1]+rect[3]:
                    return 7
                else:
                    return 0
            else:
                return 0

    @staticmethod
    def get_point_on_circle(point: tuple, circle_center: tuple, radius: float) -> tuple:
        x_diff = circle_center[0] - point[0]
        y_diff = circle_center[1] - point[1]
        hypotenuse = math.sqrt(x_diff**2 + y_diff**2)

        x = (radius/hypotenuse)*x_diff
        y = (radius/hypotenuse)*y_diff

        return circle_center[0]-x, circle_center[1]-y

    def get_closest_corner(self, rect: pygame.Rect) -> bool:
        closest_x = self.clamp(self.x + self.size / 2, rect[0], rect[0] + rect[2])
        closest_y = self.clamp(self.y + self.size / 2, rect[1], rect[1] + rect[3])

        dis_x = self.x + self.size / 2 - closest_x
        dis_y = self.y + self.size / 2 - closest_y

        return (dis_x**2 + dis_y**2) < (self.size/2)**2

    @staticmethod
    def get_position_off_corner(circle_center: tuple, corner_pos: tuple, radius: int) -> tuple:
        x_diff = circle_center[0] - corner_pos[0]
        y_diff = circle_center[1] - corner_pos[1]
        hypotenuse = math.sqrt(x_diff**2 + y_diff**2)

        x_offset = radius * x_diff/hypotenuse
        y_offset = radius * y_diff/hypotenuse

        return corner_pos[0] + x_offset, corner_pos[1] + y_offset

    def rect_physics(self, rect: pygame.Rect):
        if self.get_closest_corner(rect):
            sector = self.find_sector(rect, (self.x+self.size/2, self.y+self.size/2), 0)
            if sector == 2 or sector == 8:
                if sector == 2:
                    self.y = rect[1] - self.size
                else:
                    self.y = rect[1] + rect[3]
                self.x_vel *= self.friction
                if abs(self.y_vel) > 5:
                    self.y_vel *= -self.bounce
                else:
                    self.y_vel = 0
            elif sector == 4 or sector == 5:
                if sector == 4:
                    self.x = rect[0] - self.size
                else:
                    self.x = rect[0] + rect[2]
                self.y_vel *= self.friction
                if abs(self.x_vel) > 5:
                    self.x_vel *= -self.bounce
                else:
                    self.x_vel = 0
            else:
                if sector == 1:
                    closest_corner = (rect[0], rect[1])
                elif sector == 3:
                    closest_corner = (rect[0]+rect[2], rect[1])
                elif sector == 7:
                    closest_corner = (rect[0], rect[1]+rect[3])
                elif sector == 9:
                    closest_corner = (rect[0]+rect[2], rect[1]+rect[3])
                else:
                    return
                new_pos = self.get_position_off_corner((self.x+self.size/2, self.y+self.size/2), closest_corner,
                                                       int(self.size/2))
                self.x = new_pos[0] - self.size/2
                self.y = new_pos[1] - self.size/2
                corner_dis_to_center = ((self.x+self.size/2)-closest_corner[0], (self.y+self.size/2)-closest_corner[1])
                velocity = math.sqrt(self.x_vel**2 + self.y_vel**2)
                self.x_vel = corner_dis_to_center[0] * velocity * self.bounce * 0.05
                self.y_vel = corner_dis_to_center[1] * velocity * self.bounce * 0.05

    def collision_with_line(self, line_equation: list, circle_center: tuple, radius: int) -> bool:
        top_half = (abs((line_equation[0] * circle_center[0]) + (line_equation[1] * circle_center[1]) +
                        line_equation[2]))
        bottom_half = (math.sqrt(line_equation[0]**2 + line_equation[1]**2))
        self.dis = top_half / bottom_half
        if self.dis <= radius:
            return True
        return False

    def get_equation_line(self, pt1: tuple, pt2: tuple) -> list:
        new_point1 = (pt1[0], self.y_bound - pt1[1])
        new_point2 = (pt2[0], self.y_bound - pt2[1])
        a = new_point1[1] - new_point2[1]
        b = new_point2[0] - new_point1[0]
        c = (new_point1[0]-new_point2[0])*new_point1[1] + new_point1[0]*(new_point2[1]-new_point1[1])

        return [a, b, c]

    @staticmethod
    def get_x_y_components_from_ramp(gravity, hypotenuse: float, vertical_edge: float,
                                     horizontal_edge: float, facing: int) -> tuple:
        velocity = gravity * (vertical_edge / hypotenuse)

        x_velocity = velocity * horizontal_edge / hypotenuse
        y_velocity = velocity * vertical_edge / hypotenuse

        if facing == 1:
            x_velocity *= -1

        return x_velocity, y_velocity

    @staticmethod
    def find_circle_point_on_line(circle_center: tuple, equation: list) -> \
            tuple:
        b = equation[1]
        for i in range(len(equation)):
            equation[i] /= b
        equation[0] *= -1
        equation[2] *= -1
        equation.pop(1)

        equation_new = [0, 0]
        equation_new[0] = -1 / equation[0]
        equation_new[1] = circle_center[1] - (equation_new[0] * circle_center[0])

        x = (equation_new[1] - equation[1]) / (equation[0] - equation_new[0])
        y = (equation[0] * x) + equation[1]

        return x, y, equation_new[0]

    @staticmethod
    def find_point_where_circle_should_be_on_ramp(facing: int, radius: int, slope: float, starting_point: tuple) -> \
            tuple:
        slope_hypotenuse = math.sqrt((slope**2)+1)

        x_offset = radius / slope_hypotenuse
        y_offset = radius * (slope / slope_hypotenuse)

        if facing == 1:
            return starting_point[0]-x_offset, starting_point[1]-y_offset
        elif facing == 2:
            return starting_point[0]+x_offset, starting_point[1]+y_offset
        elif facing == 3:
            return starting_point[0]-x_offset, starting_point[1]-y_offset
        elif facing == 4:
            return starting_point[0]+x_offset, starting_point[1]-y_offset

    @staticmethod
    def get_bounce_angle(ramp_points: list[tuple], velocity_x_y: tuple, velocity: float, facing: int,
                         bounce: float) -> tuple:
        slope_mirror = (ramp_points[1][1] - ramp_points[0][1]) / (ramp_points[1][0] - ramp_points[0][0])
        if velocity_x_y[0] == 0:
            new_x_y = 1, abs((slope_mirror**2 - 1) / 2 * slope_mirror)
            hyp = math.sqrt(new_x_y[1]**2 + 1)
            x = (velocity / hyp) * bounce
            y = (velocity * new_x_y[1] / hyp) * bounce
            if facing == 1:
                return -x, -y
            else:
                return x, y
        else:
            slope_original = velocity_x_y[1] / velocity_x_y[0]
            print("vel: ", velocity_x_y)
            if not 1 + 2*slope_mirror*slope_original - slope_mirror**2 == 0:
                slope_new = (slope_mirror**2 * slope_original + 2*slope_mirror - slope_original) / \
                            (1 + 2*slope_mirror*slope_original - slope_mirror**2)
                # print(slope_new)
                hyp = math.sqrt(slope_new ** 2 + 1)
                x = (velocity / hyp) * bounce
                y = (velocity * slope_new / hyp) * bounce

                if facing == 1:
                    return -x, -y
                return x, y
        return 0, 0

    def triangle_physics(self, rect: pygame.Rect, points: list, facing: int, slanted_points: tuple, hypotenuse: float,
                         vertical_edge: float, horizontal_edge: float):
        if self.get_closest_corner(rect):
            sector = self.find_sector(rect, (self.x + self.size / 2, self.y + self.size / 2), 1)
            if not sector == 0:
                if facing == 1:
                    if not 1 <= sector <= 2 and not sector == 4:
                        self.rect_physics(rect)
                        return
                elif facing == 2:
                    if not 2 <= sector <= 3 and not sector == 5:
                        self.rect_physics(rect)
                        return
                elif facing == 3:
                    if not 7 <= sector <= 8 and not sector == 4:
                        self.rect_physics(rect)
                        return
                else:
                    if not 8 <= sector <= 9 and not sector == 5:
                        self.rect_physics(rect)
                        return
            equation = self.get_equation_line(points[slanted_points[0]], points[slanted_points[1]])
            if self.collision_with_line(equation, (self.x + self.size/2, self.y_bound - (self.y + self.size/2)),
                                        int(self.size/2)):
                point_on_line_and_slope = self.find_circle_point_on_line((self.x+self.size/2,
                                                                          1000-(self.y+self.size/2)), equation)
                updated_pos = self.find_point_where_circle_should_be_on_ramp(facing, int(self.size/2),
                                                                             point_on_line_and_slope[2],
                                                                             (point_on_line_and_slope[0],
                                                                              point_on_line_and_slope[1]))
                self.x = updated_pos[0]-self.size/2
                self.y = (1000-updated_pos[1])-self.size/2
                velocity = self.x_vel**2 + self.y_vel**2
                if velocity < 0:
                    bounce_x_y = self.get_bounce_angle([points[slanted_points[0]], points[slanted_points[1]]],
                                                       (self.x_vel, self.y_vel), math.sqrt(velocity), facing,
                                                       self.bounce)
                    if bounce_x_y[1] == 0:
                        e = 0
                    else:
                        q = abs(bounce_x_y[0] / (bounce_x_y[1]))
                        w = abs((points[slanted_points[1]][0] - points[slanted_points[0]][0]) / (points[slanted_points[1]][1] - points[slanted_points[0]][1]))
                        e = q/w
                    if abs(e - 1) < 0.5:
                        print("idk if my math is good", e)
                        x_y_acceleration = self.get_x_y_components_from_ramp(self.gravity, hypotenuse, vertical_edge,
                                                                             horizontal_edge, facing)
                        self.x_vel += x_y_acceleration[0]
                        self.fromRamp = 20
                        return
                    self.x_vel = bounce_x_y[0]
                    self.y_vel = bounce_x_y[1]
                else:
                    if facing == 1 or facing == 2:
                        x_y_acceleration = self.get_x_y_components_from_ramp(self.gravity, hypotenuse, vertical_edge,
                                                                             horizontal_edge, facing)
                        self.x_vel += x_y_acceleration[0]
                        self.y_vel += x_y_acceleration[1]
                        self.fromRamp = 20
                        # self.x_vel *= self.friction
                        # self.y_vel *= self.friction
            else:
                self.fromRamp -= 1
        else:
            self.fromRamp -= 1

    def mouse_pick(self, mouse_pos: tuple, mouse_pressed: tuple):
        if mouse_pressed[0]:
            x_diff = abs(mouse_pos[0] - (self.x + self.size/2))
            y_diff = abs(mouse_pos[1] - (self.y + self.size/2))
            if (x_diff * x_diff)+(y_diff * y_diff) < (self.size/2) * (self.size/2):
                self.held = True
        else:
            self.held = False

    def mouse_moving(self, mouse_pos: tuple, mouse_move: tuple):
        if self.held:
            self.x = mouse_pos[0] - self.size/2
            self.y = mouse_pos[1] - self.size/2
            self.x_vel = mouse_move[0] * 1.5
            self.y_vel = mouse_move[1] * 1.5
