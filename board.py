import random

import pygame
from ball import CBall
from bomb import CBomb


class CBoard:
    def __init__(self, screen, row_len, add_obj, booms, bomb, arrows, ball_colors, num_of_color,
                 ratio, width, height, left, top, c_s):
        self.screen = screen
        self.width = width
        self.height = height
        self.booms = booms
        self.bomb = bomb
        self.arrows = arrows
        self.ball_colors = ball_colors
        self.ratio = ratio
        self.num_add_obj = add_obj
        self.board = [[None] * height for _ in range(width)]
        self.colors_id = num_of_color
        self.left = left
        self.top = top
        self.cell_size = c_s
        self.curr_ball = None
        self.choice = 0
        self.row_len = row_len
        self.scores = 0
        self.add_balls(self.num_add_obj)
        self.check_and_action()
        self.can_select = True

    # отображение поля
    def render(self):
        self.screen.fill((102, 179, 255), (400, 10, self.width * self.cell_size, self.height * self.cell_size))
        for y in range(self.height + 1):
            pygame.draw.line(self.screen, pygame.Color('white'), (self.left, y * self.cell_size + self.top),
                             (self.width * self.cell_size + self.left, y * self.cell_size + self.top))
        for x in range(self.width + 1):
            pygame.draw.line(self.screen, pygame.Color('white'), (x * self.cell_size + self.left, self.top),
                             (x * self.cell_size + self.left, self.height * self.cell_size + self.top))
        for y in range(self.height):
            for x in range(self.width):
                if self.board[x][y] != None:
                    self.board[x][y].draw()
        pygame.display.update((400, 10, self.width * self.cell_size, self.height * self.cell_size))

    # нажатие на объект, а после показ его перемещения
    def on_click(self, cell_coords):
        b = self.board[cell_coords[0]][cell_coords[1]]

        if self.board[cell_coords[0]][cell_coords[1]] == None:
            if self.curr_ball != None:
                places = self.curr_ball.check_route(cell_coords[0], cell_coords[1])
                if places:
                    for p in range(1, len(places)):
                        self.curr_ball.move(places[p][0], places[p][1])
                        pygame.time.wait(100)
                        self.render()
                    if self.check_and_action():
                        self.curr_ball = None
                    else:
                        self.curr_ball = None
                        self.add_balls(self.num_add_obj)
                        self.check_and_action()


        else:
            self.curr_ball = self.board[cell_coords[0]][cell_coords[1]]

    # проверка на наличие линии
    def row_check(self):
        balls_for_kill = set()
        for i in range(self.height):
            prom = set()
            for j in range(self.width - 1):
                if self.compaire(self.board[j][i], self.board[j + 1][i], prom):
                    prom.add(self.board[j][i])
                    prom.add(self.board[j + 1][i])
                else:
                    if len(prom) >= self.row_len:
                        balls_for_kill = balls_for_kill.union(prom)
                    else:
                        prom = set()
            if len(prom) >= self.row_len:
                balls_for_kill = balls_for_kill.union(prom)

        for i in range(self.width):
            prom = set()
            for j in range(self.height - 1):
                if self.compaire(self.board[i][j], self.board[i][j + 1], prom):
                    prom.add(self.board[i][j])
                    prom.add(self.board[i][j + 1])
                else:
                    if len(prom) >= self.row_len:
                        balls_for_kill = balls_for_kill.union(prom)
                    else:
                        prom = set()
            if len(prom) >= self.row_len:
                balls_for_kill = balls_for_kill.union(prom)

        for x in range(self.width - 1):
            y = 0
            prom = set()
            for d in range(min(self.height - y, self.width - x) - 1):
                if self.compaire(self.board[x + d][y + d], self.board[x + d + 1][y + d + 1], prom):
                    prom.add(self.board[x + d][y + d])
                    prom.add(self.board[x + d + 1][y + d + 1])
                else:
                    if len(prom) >= self.row_len:

                        balls_for_kill = balls_for_kill.union(prom)
                    else:
                        prom = set()
            if len(prom) >= self.row_len:
                balls_for_kill = balls_for_kill.union(prom)

            # Снизу от прямой диагонали
        x = 0
        for y in range(1, self.height - 1):
            prom = set()
            for d in range(min(self.height - y, self.width - x) - 1):
                if self.compaire(self.board[x + d][y + d], self.board[x + d + 1][y + d + 1], prom):
                    prom.add(self.board[x + d][y + d])
                    prom.add(self.board[x + d + 1][y + d + 1])
                else:
                    if len(prom) >= self.row_len:
                        balls_for_kill = balls_for_kill.union(prom)
                    else:
                        prom = set()

            if len(prom) >= self.row_len:
                balls_for_kill = balls_for_kill.union(prom)

        # Сверху от обратной диагонали
        for x in range(self.width - 1, 0, -1):
            y = 0
            prom = set()
            for d in range(min(x, self.height - y - 1)):
                if self.compaire(self.board[x - d][y + d], self.board[x - d - 1][y + d + 1], prom):
                    prom.add(self.board[x - d][y + d])
                    prom.add(self.board[x - d - 1][y + d + 1])
                else:
                    if len(prom) >= self.row_len:
                        balls_for_kill = balls_for_kill.union(prom)
                    else:
                        prom = set()
            if len(prom) >= self.row_len:
                balls_for_kill = balls_for_kill.union(prom)

        # Снизу от обратной диагонали
        x = self.width - 1
        for y in range(1, self.height - 1):
            prom = set()
            for d in range(min(x, self.height - y - 1)):
                if self.compaire(self.board[x - d][y + d], self.board[x - d - 1][y + d + 1], prom):
                    prom.add(self.board[x - d][y + d])
                    prom.add(self.board[x - d - 1][y + d + 1])
                else:
                    if len(prom) >= self.row_len:
                        balls_for_kill = balls_for_kill.union(prom)
                    else:
                        prom = set()
            if len(prom) >= self.row_len:
                balls_for_kill = balls_for_kill.union(prom)
        return balls_for_kill

    # проверка одинакового ли цвета объекты в линии
    def compaire(self, a, b, prom):
        cur_color = None
        for s in prom:
            if type(s) == CBall:
                cur_color = s.color_id
                break

        if a == None or b == None:
            return False
        else:
            if not cur_color:
                if type(a) == CBomb or type(b) == CBomb:
                    return True
                else:
                    if type(a) == CBall and type(b) == CBall and a.color_id == b.color_id:
                        return True
                    else:
                        return False
            else:
                if type(a) == CBomb and type(b) == CBomb:
                    return True
                else:
                    if type(a) == CBall and a.color_id != cur_color:
                        return False
                    if type(b) == CBall and b.color_id != cur_color:
                        return False
                    return True

    # добавляет обеъкты
    def add_balls(self, num):
        for i in range(num):
            fc = self.get_free_cell()
            if fc:
                a = random.choice(fc)
                chance = random.randint(0, 100)
                if chance <= (100 / (len(self.colors_id) + 1)) * self.ratio / 100:
                    self.board[a[0]][a[1]] = CBomb(self, a[0], a[1], self.bomb, random.randint(0, 3))
                else:
                    self.board[a[0]][a[1]] = CBall(self, a[0], a[1], random.choice(self.colors_id))
                self.check_and_action()

    # проверка на нажатие клетки
    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[0] < self.left + self.width * self.cell_size and self.top <= mouse_pos[1] < \
                self.top + self.height * self.cell_size:
            return int((mouse_pos[0] - self.left) / self.cell_size), int((mouse_pos[1] - self.top) / self.cell_size)
        else:
            return None

    # проверка на свободные клетки
    def get_free_cell(self):
        free_zones = []
        for y in range(self.height):
            for x in range(self.width):
                if self.board[x][y] == None:
                    free_zones.append((x, y))
        return free_zones

    # проверка на нажатие
    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell != None:
            self.on_click(cell)

    # метод для увеличивания очков
    def check_and_action(self):
        rows = self.row_check()
        if rows:
            l = len(rows)
            self.scores = self.scores + l + (l - self.row_len) ** 2
            for c in rows:
                if c:
                    if type(c) == CBomb and c.dir_id == 0:
                        for i in range(self.width):
                            if self.board[i][c.y] != None:
                                self.board[i][c.y].killing()
                                if self.board[i][c.y] not in rows:
                                    self.scores += 1
                    elif type(c) == CBomb and c.dir_id == 1:
                        for i in range(self.height):
                            if self.board[c.x][i] != None:
                                self.board[c.x][i].killing()
                                if self.board[c.x][i] not in rows:
                                    self.scores += 1
                    elif type(c) == CBomb and c.dir_id == 2:
                        for i in range(self.height):
                            if self.board[c.x][i] != None:
                                self.board[c.x][i].killing()
                                if self.board[c.x][i] not in rows:
                                    self.scores += 1
                        for i in range(self.width):
                            if self.board[i][c.y] != None:
                                self.board[i][c.y].killing()
                                if self.board[i][c.y] not in rows:
                                    self.scores += 1
                    elif type(c) == CBomb and c.dir_id == 3:
                        for i in range(max(c.x - 2, 0), min(c.x + 3, self.width)):
                            for j in range(max(0, c.y - 2), min(c.y + 3, self.height)):
                                if self.board[i][j] != None:
                                    self.board[i][j].killing()
                                    if self.board[i][j] not in rows:
                                        self.scores += 1
                    else:
                        self.board[c.x][c.y].killing()
            return True
        return False
