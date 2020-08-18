import random
import constant as c


class Board:
    # Initialize board with drawable area of
    # width in [1, width]
    # height in [1, height]
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.st = None
        self.en = None
        self.matrix = [[0 for x in range(self.width + 2)] for y in range(self.height + 2)]
        self.create_wall()

    def create_wall(self):
        for x in range(self.height + 2):
            for y in range(self.width + 2):
                if x == 0 or x == self.height + 1 or y == 0 or y == self.width + 1:
                    self.matrix[x][y] = -1

    def create_dest(self, pos):
        self.matrix[pos[0]][pos[1]] = 1
        if self.st is None:
            self.st = pos
        else:
            self.en = pos

    def create_one_wall(self, pos):
        self.matrix[pos[0]][pos[1]] = -1

    def create_example_board(self):
        self.create_blank_board()
        for x in range(1, self.height + 1):
            for y in range(1, self.width + 1):
                if x == y == 1 or x == y == c.cell_nr:
                    continue
                k = random.randint(0, 2)
                if k == 0:
                    self.matrix[x][y] = -1

    def create_blank_board(self):
        self.matrix = [[0 for x in range(self.width + 2)] for y in range(self.height + 2)]
        self.create_wall()
