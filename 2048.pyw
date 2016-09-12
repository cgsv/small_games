import random
from graphics import *

class g2048:

    def __init__(self):
        self.data = [0 for i in range(16)]
        #random.seed("cgsv")
        self.add_new_num()
        self.add_new_num()
        self.run_gui()

    def update_view(self):
        for i in range(16):
            txt = str(self.data[i])
            if txt == '0': txt = ' '
            self.texts[i].setText(txt)

    def run_gui(self):
        win = GraphWin("2048", 300, 300)
        self.texts = [None for i in range(16)]
        self.win = win
        for i in range(5):
            l = Line(Point(i * 75, 0), Point(i * 75, 300))
            l.draw(win)
        for i in range(5):
            l = Line(Point(0, i * 75), Point(300, i * 75))
            l.draw(win)
        for j in range(4):
            for i in range(4):
                t = Text(Point(i*75 + 75/2, j*75 + 75/2), ' ')
                self.texts[j*4+i] = t
                t.setStyle("bold")
                t.setTextColor("blue")
                t.draw(win)
        self.update_view()
        self.main_loop()
        t = Text(Point(150, 150), 'GAME OVER')
        t.setSize(30)
        t.setStyle("bold")
        t.setTextColor("red")
        t.draw(win)
        win.getMouse()

    def main_loop(self):
        while True:
            k = self.win.getKey()
            if k == 'q': break
            self.move(k)
            if self.over:
                break

    def move(self, direction):
        if direction == 'Left':
            if self.reduce_hor(0):
                self.add_new_num()
        elif direction == 'Right':
            if self.reduce_hor(1):
                self.add_new_num()
        elif direction == 'Up':
            if self.reduce_ver(0):
                self.add_new_num()
        elif direction == 'Down':
            if self.reduce_ver(1):
                self.add_new_num()
        self.update_view()

    def print_map(self):
        for i in range(4):
            print self.data[i*4: i*4+4]

    def add_new_num(self):
        zero_idxs = filter(lambda x: self.data[x] == 0, range(16))
        assert len(zero_idxs) > 0
        idx = random.choice(zero_idxs)
        self.data[idx] = random.choice([2,4])
        self.over = False
        if len(zero_idxs) == 1:
            self.over = True
            for i in range(3):
                for j in range(3):
                    if self.data[i*4+j] == self.data[(i+1)*4+j] or self.data[i*4+j] == self.data[i*4+j+1]:
                        self.over = False
                        return

    #reduce four elements (default to left)
    #if can reduce: return True
    def reduce_line(self, line):
        tmp = filter(lambda x: x > 0, line)
        tmp += [0] * (4 - len(tmp))
        res = [0, 0, 0, 0]
        if tmp[0] == tmp[1] and tmp[2] == tmp[3]:
            res[0], res[1] = 2 * tmp[0], 2 * tmp[2]
        elif tmp[0] == tmp[1]:
            res[0], res[1], res[2] = 2 * tmp[0], tmp[2], tmp[3]
        elif tmp[1] == tmp[2]:
            res[0], res[1], res[2] = tmp[0], 2 * tmp[2], tmp[3]
        elif tmp[2] == tmp[3]:
            res[0], res[1], res[2] = tmp[0], tmp[1], 2 * tmp[3]
        else:
            res[:] = tmp
        if res == line: return False
        line[:] = res
        return True

    def reduce_hor(self, is_right):
        res = False
        for i in range(4):
            d = self.data[i*4: i*4+4]
            if is_right: d.reverse()
            if self.reduce_line(d): 
                res = True
                if is_right: d.reverse()
                self.data[i*4: i*4+4] = d
        return res 

    def reduce_ver(self, is_down):
        res = False
        for i in range(4):
            d = self.data[i: 16 : 4]
            if is_down: d.reverse()
            if self.reduce_line(d): 
                res = True
                if is_down: d.reverse()
                self.data[i: 16: 4] = d
        return res 

game = g2048()



