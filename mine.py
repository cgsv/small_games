from random import random, seed
from graphics import *
import time

pstr = [' ', '1', '2', '3', '4', '5', '6', '7', '8', '*']

class Mine:

    def __init__(self, width = 10, height = 10, mprob = 0.3, bsize = 20):
        self.w = width
        self.h = height
        self.mine_prob = mprob
        self.mine_cnt = 0
        self.visited_cnt = 0
        self.bsize = bsize 
        # add two more lines and cols for easy calculation
        self.data = [[0 for i in range(width + 2)] for j in range(height + 2)]
        self.texts = [[None for i in range(width + 2)] for j in range(height + 2)]
        self.visited = [[False for i in range(width + 2)] for j in range(height + 2)]
        #seed("cgsv")
        self.generate_mine()
        self.run_gui()

    def run_gui(self):
        win = GraphWin("Minesweeper", self.w * self.bsize, self.h * self.bsize)
        win.bind("<Button-3>", self._rclick)
        self.win = win
        for i in range(self.w+1):
            l = Line(Point(i * self.bsize, 0), Point(i * self.bsize, self.h * self.bsize))
            l.draw(win)
        for i in range(self.h+1):
            l = Line(Point(0, i * self.bsize), Point(self.w * self.bsize, i * self.bsize))
            l.draw(win)
        for j in range(1, self.h + 1):
            for i in range(1, self.w + 1):
                t = Text(Point((i-1)*self.bsize + self.bsize/2, (j-1)*self.bsize + self.bsize/2), ' ')
                self.texts[j][i] = t
                t.draw(win)
        #print 'done'
        t = Text(Point(self.w/2*self.bsize, self.h/2*self.bsize), ' ')
        t.setSize(30)
        t.setStyle("bold")
        t.setTextColor("blue")
        msg = ""
        if self.event_loop(win):
            msg += "Success\n "
        else:
            for j in range(1, self.h + 1):
                for i in range(1, self.w + 1):
                    if self.data[j][i] == 9:
                        self.texts[j][i].setText('*')
            msg += "Failed\n "
        msg +=  "%.2f s" % (time.time() - self.start_time)
        t.setText(msg)
        t.draw(win)
        win.getMouse()
        win.close()

    def _rclick(self, e):
        i = e.x / self.bsize + 1
        j = e.y / self.bsize + 1
        if self.visited[j][i]: return
        if self.texts[j][i].getText() == ' ':
            self.texts[j][i].setText('M')
        elif self.texts[j][i].getText() == 'M':
            self.texts[j][i].setText(' ')

    def event_loop(self, win):
        first = True
        while True:
            p = win.getMouse()
            i = p.x / self.bsize + 1
            j = p.y / self.bsize + 1
            if self.visited[j][i]: continue
            if first:
                self.start_time = time.time()
                first = False
            if self.texts[j][i].getText() == 'M':
                continue
            s = pstr[self.data[j][i]]
            if s != ' ':
                self.texts[j][i].setText(s)
                self.visited[j][i] = True
                self.visited_cnt += 1
                if s == '*':
                    return False
            else:
                self.reveal_zero_region(i, j)
            if self.visited_cnt + self.mine_cnt == self.w * self.h:
                return True

    def reveal_zero_region(self, i, j):
        q = [[i,j]]
        while len(q) > 0:
            i, j = q.pop()
            if i < 1 or i > self.w or j < 1 or j > self.h or self.visited[j][i]:
                continue
            s = pstr[self.data[j][i]]
            if s != ' ':
                self.texts[j][i].setText(s)
            else:
                rect = Rectangle(Point((i-1)*self.bsize, (j-1)*self.bsize), Point((i)*self.bsize, (j)*self.bsize))
                rect.setFill("green")
                rect.draw(self.win)
            self.visited[j][i] = True
            self.visited_cnt += 1
            if self.data[j][i] == 0:
                for r in range(i-1, i+2):
                    for c in range(j-1, j+2):
                        if r == i and c == j: continue
                        q.insert(0, [r, c])

    def generate_mine(self):
        for j in range(1, self.h + 1):
            for i in range(1, self.w + 1):
                if random() < self.mine_prob:
                    self.data[j][i] = 9 # 9 for mine
                    self.mine_cnt += 1
                    self.update_nb(j, i)

    def update_nb(self, r, c):
        for j in range(r-1, r+2):
            for i in range(c-1, c+2):
                if self.data[j][i] != 9:
                    self.data[j][i] += 1

m = Mine(30, 15, 0.1, bsize = 30)

