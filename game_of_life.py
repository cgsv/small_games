import random, time
from graphics import *

class Cells:

    def __init__(self, row, col, prob = 0.5):
        self.row = row
        self.col = col
        self.data = [[0 for i in range(col)] for j in range(row)]
        self.gen_life_random(prob)

    def get_life_cnt(self):
        sum = 0
        for i in range(self.row):
            for j in range(self.col):
                sum += self.data[i][j]
        return sum

    def gen_life_random(self, prob): # life probability (0 ~ 1)
        for i in range(self.row):
            for j in range(self.col):
                if random.random() < prob:
                    self.data[i][j] = 1

    def print_cells(self):
        for line in self.data:
            for item in line:
                print item,
            print

    def is_valid(self, r, c):
        return r >= 0 and r < self.row and c >= 0 and c < self.col

    def is_alive(self, r, c):
        return self.is_valid(r, c) and self.data[r][c] == 1

    def get_nb_live_num(self, r, j):
        return self.is_alive(r-1,j-1) + self.is_alive(r-1,j) + self.is_alive(r-1,j+1) + \
                self.is_alive(r,j-1) + self.is_alive(r,j+1) + \
                self.is_alive(r+1,j-1) + self.is_alive(r+1,j) + self.is_alive(r+1,j+1)

    def set_change_handler(self, hdl):
        self.event_handler = hdl

    def to_next_state(self):
        data2 = [d[:] for d in self.data] # deep copy data
        changed = False
        for i in range(self.row):
            for j in range(self.col):
                nbs = self.get_nb_live_num(i, j)
                if data2[i][j]:
                    if nbs < 2 or nbs > 3:
                        self.data[i][j] = 0
                        changed = True
                        self.event_handler.handle_change(i, j, 0)
                else:
                    if nbs == 3:
                        self.data[i][j] = 1
                        changed = True
                        self.event_handler.handle_change(i, j, 1)
        return changed

class GameOfLifeGui:

    def __init__(self, cells, bsize = 30):
        self.cells = cells
        self.bsize = bsize
        self.row = self.cells.row #height
        self.col = self.cells.col #width
        self.width = self.col * bsize
        self.height = self.row * bsize
        self.steps = 0
        #self.run_gui()

    def handle_change(self, i, j, state):
        self.rects[i][j].setFill("red" if state else "white")

    def update_state(self):
        #time.sleep(.2)
        return self.cells.to_next_state()

    def run_gui(self):
        win = GraphWin("Game of life", self.width, self.height)
        self.win = win
        self.rects = [[None for i in range(self.col)] for j in range(self.row)]
        for i in range(self.col): # x pos
            for j in range(self.row): # y pos
                rect = Rectangle(Point(i*self.bsize, j*self.bsize), Point((i+1)*self.bsize, (j+1)*self.bsize))
                if self.cells.data[j][i]:
                    rect.setFill("red")
                else:
                    rect.setFill("white")
                self.rects[j][i] = rect
                rect.draw(win)
        while self.update_state():
            self.steps += 1
            lives = self.cells.get_life_cnt()
            self.win.master.title("Game of life. steps: " + str(self.steps) + ", lives: " + str(lives))
        self.win.getMouse()

cells = Cells(20,20,0.2)
game = GameOfLifeGui(cells, 30)
cells.set_change_handler(game)
game.run_gui()

