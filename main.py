from objects import *


def main():
        win = Window(1800, 1800)
        maze = Maze(10, 10, 10, 10, 20, 20, win)
        maze.create_cells()
        maze._break_entrance_and_exit()
        maze._break_walls_r(0, 0,)
        maze._reset_cells_visited()
        is_solvable = maze.solve()
        if not is_solvable:
                print("maze can not be solved!")
        else:
                print("maze solved!")
        win.wait_for_close()

main()