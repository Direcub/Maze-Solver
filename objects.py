from tkinter import Tk, BOTH, Canvas
import time
import random


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title("The Amazing Maze Solver")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.root)
        self.canvas.pack()
        self.is_running = False

    
    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    
    def wait_for_close(self):
        self.is_running = True
        while self.is_running == True:
            self.redraw()
        self.redraw()
    
    
    def close(self):
        self.is_running = False

    
    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point_one = point1
        self.point_two = point2

    
    def draw(self, canvas, fill_color):
        canvas.create_line(self.point_one.x, self.point_one.y, self.point_two.x, self.point_two.y, fill=fill_color, width=2)
    
class Cell:
    def __init__(self, x1, y1, x2, y2, win=None):
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.has_right_wall = True
        self.has_left_wall = True
        self.top_left = Point(x1, y1)
        self.top_right = Point(x2, y1)
        self.bottom_right = Point(x2, y2)
        self.bottom_left = Point(x1, y2)
        self.visited = False
        self.win = win


    def break_wall(self, direction):
        if direction == 'up':
            self.has_top_wall = False
        if direction == 'down':
            self.has_bottom_wall = False
        if direction == 'left':
            self.has_left_wall = False
        if direction == 'right':
            self.has_right_wall = False

    
    def _draw_line(self, point1, point2, color="black"):
        line = Line(point1, point2)
        if hasattr(self.win, 'canvas'):
            line.draw(self.win.canvas, color)

    
    def draw(self):
        if self.has_top_wall:
            self._draw_line(self.top_left, self.top_right)
        else:
            self._draw_line(self.top_left, self.top_right, "lightgray")
        if self.has_left_wall:
            self._draw_line(self.top_left, self.bottom_left)
        else:
            self._draw_line(self.top_left, self.bottom_left, "lightgray")
        if self.has_right_wall:
            self._draw_line(self.top_right, self.bottom_right)
        else:
            self._draw_line(self.top_right, self.bottom_right, "lightgray")
        if self.has_bottom_wall:
            self._draw_line(self.bottom_left, self.bottom_right)
        else:
            self._draw_line(self.bottom_left, self.bottom_right, "lightgray")
    
    
    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo:
            color = "gray"
        center1 = Point((self.top_left.x + self.bottom_right.x)/2, (self.top_left.y + self.bottom_right.y)/2)
        center2 = Point((to_cell.top_left.x + to_cell.bottom_right.x)/2, (to_cell.top_left.y + to_cell.bottom_right.y)/2)
        line = Line(center1, center2)
        line.draw(self.win.canvas, color)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.create_cells()
        if seed != None:
            self.seed = random.seed(seed)

    
    def create_cells(self):
        self._cells = []
        for i in range(self.num_cols):
            current_column = []
            for j in range(self.num_rows):
                cell = Cell(
                    self.x1 + (i * self.cell_size_x),
                    self.y1 + (j * self.cell_size_y),
                    self.x1 + (i * self.cell_size_x) + self.cell_size_x,
                    self.y1 + (j * self.cell_size_y) + self.cell_size_y,
                    self.win
                )
                current_column.append(cell)
            self._cells.append(current_column)
        self.full_draw()

    
    def full_draw(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.draw_cell(i, j)
        
    
    def draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()


    def _animate(self):
        if hasattr(self.win, 'canvas'):
            self.win.redraw()
            time.sleep(0.0025)

    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self.draw_cell(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self.draw_cell(-1, -1)

    def _reset_cells_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._cells[i][j].visited = False

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            if i < self.num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            if j < self.num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))
            if len(next_index_list) == 0:
                self.draw_cell(i, j)
                return
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            self._break_walls_r(next_index[0], next_index[1])

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True
        if i > 0 and not self._cells[i - 1][j].visited and not self._cells[i][j].has_left_wall:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j], undo=True)
        if i < self.num_rows -1 and not self._cells[i + 1][j].visited and not self._cells[i][j].has_right_wall:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            else:
                    self._cells[i][j].draw_move(self._cells[i+1][j], undo=True)
        if j > 0 and not self._cells[i][j-1].visited and not self._cells[i][j].has_top_wall:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1], undo=True)
        if j < self.num_cols - 1 and not self._cells[i][j+1].visited and not self._cells[i][j].has_bottom_wall:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1], undo=True)
        return False
