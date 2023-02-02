import os
import sys

import pygame


class CBall(pygame.sprite.Sprite):
    def __init__(self, board, x, y, color_id):
        self.board = board
        self.x = x
        self.y = y
        self.color_id = color_id
        self.color = self.board.ball_colors[self.color_id]
        self.color = pygame.transform.scale(self.color, (self.board.cell_size, self.board.cell_size))
        self.r = self.board.cell_size / 2
        self.status = "Stand"
        self.frame = 0
        self.max_frame = 11

    # отрисовка мячика и его уничтожение
    def draw(self):
        if self == self.board.curr_ball:
            pygame.draw.rect(self.board.screen, pygame.Color('red'),
                             (self.x * self.board.cell_size + self.board.left + 1,
                              self.y * self.board.cell_size + self.board.top + 1,
                              self.board.cell_size - 1,
                              self.board.cell_size - 1), 2)

        if self.status == "Stand":
            self.board.screen.blit(self.color, (self.x * self.board.cell_size + self.board.left,
                                                self.y * self.board.cell_size + self.board.top))
        elif self.status == "Killing":
            if self.frame == self.max_frame:
                self.kill()
                self.board.can_select = True
            else:
                self.color = self.board.booms[self.frame]
                self.color = pygame.transform.scale(self.color, (self.board.cell_size, self.board.cell_size))
                self.board.screen.blit(self.color, (self.x * self.board.cell_size + self.board.left,
                                                    self.y * self.board.cell_size + self.board.top))
                self.frame += 1

    # перемещение шарика
    def move(self, x1, y1):
        self.board.board[self.x][self.y] = None
        self.board.board[x1][y1] = self
        self.x = x1
        self.y = y1

    # поиск пути
    def check_route(self, x1, y1):
        new_mat = [[-1] * (self.board.height + 2) for _ in range(self.board.width + 2)]
        for i in range(self.board.width):
            for j in range(self.board.height):
                if self.board.board[i][j] == None:
                    new_mat[i + 1][j + 1] = 0
        new_mat[self.x + 1][self.y + 1] = 1
        k = 1
        places = []
        end_achived = False
        added = True
        while not end_achived and added == True:
            added = False
            for i in range(1, self.board.width + 1):
                for j in range(1, self.board.height + 1):
                    if new_mat[i][j] == k:
                        if i == x1 + 1 and j == y1 + 1:
                            end_achived = True
                            break
                        if new_mat[i - 1][j] == 0:
                            new_mat[i - 1][j] = k + 1
                            added = True
                        if new_mat[i][j + 1] == 0:
                            new_mat[i][j + 1] = k + 1
                            added = True
                        if new_mat[i + 1][j] == 0:
                            new_mat[i + 1][j] = k + 1
                            added = True
                        if new_mat[i][j - 1] == 0:
                            new_mat[i][j - 1] = k + 1
                            added = True
            k += 1
        if end_achived:
            cur = (x1 + 1, y1 + 1)
            for i in range(k - 1, 0, -1):
                places.append((cur[0] - 1, cur[1] - 1))
                if new_mat[cur[0] - 1][cur[1]] == i - 1:
                    cur = (cur[0] - 1, cur[1])
                    continue
                if new_mat[cur[0]][cur[1] + 1] == i - 1:
                    cur = (cur[0], cur[1] + 1)
                    continue
                if new_mat[cur[0] + 1][cur[1]] == i - 1:
                    cur = (cur[0] + 1, cur[1])
                    continue
                if new_mat[cur[0]][cur[1] - 1] == i - 1:
                    cur = (cur[0], cur[1] - 1)
                    continue
            places = places[::-1]
            return places
        else:
            return None

    # смена состояния для смены кадров при уничтожении
    def killing(self):
        self.status = "Killing"
        self.board.can_select = True
        self.frame = 0
        self.max_frame = 12

    # уничтожение мячика
    def kill(self):
        print(self.x, self.y)
        self.board.board[self.x][self.y] = None
        del self
