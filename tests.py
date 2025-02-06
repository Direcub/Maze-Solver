import unittest
from objects import *

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_entrance_exit(self):
        m1 = Maze(0, 0, 10, 10, 10, 10)
        m1._break_entrance_and_exit()
        self.assertEqual(m1._cells[0][0].has_top_wall, False)
        self.assertEqual(m1._cells[-1][-1].has_bottom_wall, False)

    def test_visitation(self):
        m1 = Maze(0, 0, 10, 10, 10, 10)
        m1._break_entrance_and_exit()
        m1._break_walls_r(0, 0,)
        m1._reset_cells_visited()
        for i in range(len(m1._cells)):
            for j in range(len(m1._cells[i])):
                self.assertEqual(m1._cells[i][j].visited, False)

if __name__ == "__main__":
    unittest.main()