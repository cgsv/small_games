from graphics import *
import time
bd = ["..9748...","7........",".2.1.9...","..7...24.",".64.1.59.",".98...3..","...8.3.2.","........6","...2759.."]
#bd = ["519748...","7........",".2.1.9...","..7...24.",".64.1.59.",".98...3..","...8.3.2.","........6","...2759.."]
#bd = [".........","7........",".2.1.9...","..7...24.",".64.1.59.",".98...3..","...8.3.2.","........6","...2759.."]
#bd = ["."*9] * 9

class Solution(object):
    def find_first_blank(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == '.':
                    return [i, j]
        return [-1, -1]

    def is_valid(self, r, c, num):
        for i in range(9):
            if self.board[r][i] == num or self.board[i][c] == num:
                return False
        for i in range(r/3*3, r/3*3+3):
            for j in range(c/3*3, c/3*3+3):
                if self.board[i][j] == num:
                    return False
        return True

    def dfs(self):
        r, c = self.find_first_blank()
        if r == -1:
            self.print_board()
            if self.enable_gui:
                self.win.getMouse()
        for i in range(1, 10):
            if self.is_valid(r, c, str(i)):
                self.board[r][c] = str(i)
                if self.enable_gui:
                    self.texts[r][c].setText(str(i))
                #time.sleep(0.1)
                self.dfs()
                self.board[r][c] = '.'
                if self.enable_gui:
                    self.texts[r][c].setText(' ')
                #time.sleep(0.1)

    def run_gui(self):
        self.bsize = 40
        win = GraphWin("Sodoku", self.bsize * 9, self.bsize * 9)
        self.win = win
        self.texts = [[None for i in range(9)] for j in range(9)]
        for i in range(9):
            for j in range(9):
                t = Text(Point(j*self.bsize + self.bsize/2, i*self.bsize + self.bsize/2), ' ')
                rect = Rectangle(Point(j*self.bsize, i*self.bsize), Point((j+1)*self.bsize, (i+1)*self.bsize))
                if self.board[i][j] != '.':
                    rect.setFill("green")
                    t.setText(self.board[i][j])
                self.texts[i][j] = t
                rect.draw(win)
                t.draw(win)
        for i in range(1, 3):
            rect = Rectangle(Point(0, i*3*self.bsize-1), Point(self.bsize*9, i*3*self.bsize+1))
            rect.setFill("black")
            rect.draw(win)
            rect = Rectangle(Point(i*3*self.bsize-1, 0), Point(i*3*self.bsize+1, self.bsize*9))
            rect.setFill("black")
            rect.draw(win)

    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: void Do not return anything, modify board in-place instead.
        """
        self.board = map(list, board)
        self.enable_gui = False
        self.enable_gui = True
        if self.enable_gui:
            self.run_gui()
        self.dfs()
        if self.enable_gui:
            self.win.getMouse()

    def print_board(self):
        for item in self.board:
            print item
        print

s = Solution()
s.solveSudoku(bd)
