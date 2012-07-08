
from StringIO import StringIO
from unittest import TestCase, main

from search_and_rescue import load_sea_grid, value_at, valid_cells_from, max_path, max_cell, sum_path

class TestSeachAndRescue(TestCase):

    def testLoadSeaGrid(self):
        fobj = StringIO("""
        0,1,2
        4,3,2
        """)
        expected = [
            [0, 1, 2],
            [4, 3, 2],
            ]
        actual = load_sea_grid(fobj)
        self.assertEqual(expected, actual)

    def testValueAt(self):
        grid = [
            [1, 2, 4],
            [3, 5, 6],
            [3, 5, 6],
            ]
        expected = 5
        cell = (1, 0)
        actual = value_at(grid, cell)
        self.assertEqual(expected, actual)

    def test_valid_cells_from_center(self):
        grid = [
            [1, 2, 4],
            [3, 5, 6],
            [7, 8, 9],
            ]
        current_xy = (1,1)
        self.assertEqual(5, value_at(grid, current_xy))
        
        seen_cells = []
        expected = [ (0, 1), (1, 0), (2, 1), (1, 2) ]
        actual = valid_cells_from(current_xy, seen_cells, len(grid))
        self.assertEqual(sorted(expected), sorted(actual))

    def test_valid_cells_from_left_edge(self):
        grid = [
            [1, 2, 4],
            [3, 5, 6],
            [7, 8, 9],
            ]
        current_xy = (0,1)
        self.assertEqual(3, value_at(grid, current_xy))
        
        seen_cells = []
        expected = [ (0, 0), (0, 2), (1, 1) ]
        actual = valid_cells_from(current_xy, seen_cells, len(grid))
        self.assertEqual(sorted(expected), sorted(actual))

    def test_valid_cells_from_right_edge(self):
        grid = [
            [1, 2, 4],
            [3, 5, 6],
            [7, 8, 9],
            ]
        current_xy = (2,1)
        self.assertEqual(6, value_at(grid, current_xy))
        
        seen_cells = []
        expected = [ (2, 0), (1, 1), (2, 2) ]
        actual = valid_cells_from(current_xy, seen_cells, len(grid))
        self.assertEqual(sorted(expected), sorted(actual))

    def test_valid_cells_from_top_edge(self):
        grid = [
            [1, 2, 4],
            [3, 5, 6],
            [7, 8, 9],
            ]
        current_xy = (1,2)
        self.assertEqual(2, value_at(grid, current_xy))
        
        seen_cells = []
        expected = [ (0, 2), (1, 1), (2, 2) ]
        actual = valid_cells_from(current_xy, seen_cells, len(grid))
        self.assertEqual(sorted(expected), sorted(actual))

    def test_valid_cells_from_bottom_edge(self):
        grid = [
            [1, 2, 4],
            [3, 5, 6],
            [7, 8, 9],
            ]
        current_xy = (1,0)
        self.assertEqual(8, value_at(grid, current_xy))
        
        seen_cells = []
        expected = [ (0, 0), (1, 1), (2, 0) ]
        actual = valid_cells_from(current_xy, seen_cells, len(grid))
        self.assertEqual(sorted(expected), sorted(actual))

    def test_valid_cells_seen_cells_excluded(self):
        grid = [
            [1, 2, 4],
            [3, 5, 6],
            [7, 8, 9],
            ]
        current_xy = (1,0)
        self.assertEqual(8, value_at(grid, current_xy))
        
        seen_cells = [(1, 1)]
        expected = [ (0, 0), (2, 0) ]
        actual = valid_cells_from(current_xy, seen_cells, len(grid))
        self.assertEqual(sorted(expected), sorted(actual))

    def test_max_path(self):
        grid = [
            [1, 2, 4],
            [3, 5, 6],
            [7, 8, 9],
            ]
        paths = [
            [ (0,0), (0,1), (0,2) ],
            [ (0,0), (1,0), (2,0) ],
            ]
        expected = [ (0,0), (1,0), (2,0) ]
        actual = max_path(grid, paths)
        self.assertEqual(expected, actual)

    def test_max_path_all_zero(self):
        grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            ]
        paths = [
            [ (0,0), (0,1), (0,2) ],
            [ (0,0), (1,0), (2,0) ],
            ]
        expected = [ (0,0), (1,0), (2,0) ]
        actual = max_path(grid, paths)
        self.assertEqual(expected, actual)

    def test_max_cell(self):
        grid = [
            [1, 2, 4],
            [3, 5, 6],
            [7, 8, 9],
            ]
        cells = [(0,0), (1,0), (2,0)]
        expected = (2,0)
        self.assertEqual(9, value_at(grid, expected))
        actual = max_cell(grid, cells)
        self.assertEqual(expected, actual)

    def test_max_cell_all_zero(self):
        """Handle when the max value of any of the cells is zero"""
        grid = [
            [1, 5, 4],
            [3, 5, 6],
            [0, 0, 0],
            ]
        cells = [(0,0), (1,0), (2,0)]
        expected = (2,0)
        actual = max_cell(grid, cells)
        self.assertEqual(expected, actual)

    def test_sum_path(self):
        grid = [
            [1, 2, 4],
            [3, 5, 6],
            [7, 8, 9],
            ]
        path = [(0,0), (1,0), (2,0)]
        expected = 24
        actual = sum_path(grid, path)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    main()
