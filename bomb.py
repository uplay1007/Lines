import pygame


class CBomb(pygame.sprite.Sprite):
    def __init__(self, board, x, y, im, dir):
        self.board = board
        self.x = x
        self.y = y
        self.im = im
        self.dir = self.board.arrows[dir]
        self.dir_id = dir
        self.status = "Stand"

    # отрисовка бомбы, с дополнительным спрайтом направления взрыва и ее уничтожения
    def draw(self):
        if self.status == "Stand":
            self.board.screen.blit(self.im, (self.x * self.board.cell_size + self.board.left,
                                             self.y * self.board.cell_size + self.board.top))
            self.board.screen.blit(self.dir,
                                   (self.x * self.board.cell_size + self.board.left + self.board.cell_size // 4,
                                    self.y * self.board.cell_size + self.board.top + self.board.cell_size // 2.5))
        elif self.status == "Killing":
            if self.frame == self.max_frame:
                self.kill()
                self.board.can_select = True
            else:
                self.im = self.board.booms[self.frame]
                self.im = pygame.transform.scale(self.im, (self.board.cell_size, self.board.cell_size))
                self.board.screen.blit(self.im, (self.x * self.board.cell_size + self.board.left,
                                                 self.y * self.board.cell_size + self.board.top))
                self.frame += 1

    def move(self, x1, y1):
        self.board.board[self.x][self.y] = None
        self.board.board[x1][y1] = self
        self.x = x1
        self.y = y1

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

    def killing(self):
        self.status = "Killing"
        self.board.can_select = True
        self.frame = 0
        self.max_frame = 12

    def kill(self):
        print(self.x, self.y)
        self.board.board[self.x][self.y] = None
        del self
