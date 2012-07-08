

import sys

def load_sea_grid(fobj):
    """
    Load the csv file representing the grid with
    a precent in each entry and return a nested
    list of the lists representing the grid.
    """
    grid = []
    for line in fobj:
        if not line.strip():
            continue
        row = []
        for val in line.split(','):
            val = val.strip()
            row.append(int(val))
        grid.append(row)
    return grid

def value_at(grid, x_and_y):
    """Returns the (x,y) coordinate in the grid"""
    x,y = x_and_y
    h = len(grid)
    row = grid[h - y - 1]
    value = row[x]
    return value

def valid_cells_from(current_xy, seen_cells, grid_height):
    """
    Returns a list of x,y tuples that are valid moves
    on the grid from where you've been.
    """
    x,y = current_xy
    possible_next_cells = []

    # up
    if y < grid_height-1: possible_next_cells.append( (x, y+1) )
    # down
    if y > 0: possible_next_cells.append( (x, y-1) )
    # left
    if x > 0: possible_next_cells.append( (x-1, y) )
    # right
    if x < grid_height-1: possible_next_cells.append( (x+1, y) )

    # Filter out cells we've been to before
    for cell in possible_next_cells[:]:
        if cell in seen_cells:
            possible_next_cells.remove(cell)
    return possible_next_cells

def max_cell(grid, cells):
    """
    For a set of (x,y) cells, return the one
    that has the maximum value on the grid
    """
    high_value = 0
    high_cell = None
    for c in cells:
        cell_value = value_at(grid, c)
        if cell_value >= high_value:
            high_value = cell_value
            high_cell = c
    return high_cell

def sum_path(grid, path):
    """Adds the value of all cells in the path"""   
    path_total = 0
    for cell in path:
        path_total += value_at(grid, cell)
    return path_total

def max_path(grid, paths):
    """
    For a set of paths, return the one that has the high
    values on the grid for the coordinates in that path
    """
    high_value = 0
    high_path = None
    for p in paths:
        path_total = sum_path(grid, p)
        if path_total >= high_value:
            high_value = path_total
            high_path = p
    return high_path

def find_best_path_from(grid, seen_cells, path_length):
    """
    Given a grid of arbitrary size (assumed to be square)
    and a list seen_cells consisting of size two tuples
    representing the x and y coordinates of cells that
    have already been visited (the last representing the
    previous move taken), 
    return a list of tuples representing the path way with
    the maximum total value that can be gained from the
    specified starting point. None is returned if there
    are no paths that can go for the specified length

    This function assumes a
    small grid and a path_length.
    """
    cur_cell = seen_cells[-1]
    possible_next_cells = valid_cells_from(cur_cell, seen_cells, len(grid))

    # We can't move to any of the next places
    if not possible_next_cells:
        return None

    # Terminal Case
    if 1 == path_length:
        return [ cur_cell, max_cell(grid, possible_next_cells) ]

    possible_paths = []
    for cell in possible_next_cells:
        new_seen_cells = seen_cells[:]
        new_seen_cells.append(cell)
        best_path = find_best_path_from(grid, new_seen_cells, path_length-1)
        if best_path: # None if no valid path
            possible_paths.append(best_path)
    if possible_paths:
        return [ cur_cell ] + max_path(grid, possible_paths)
    else:
        return None

def find_best_path(grid, path_length):
    """Finds the optimal path through the grid"""
    best_paths = []
    for x in xrange(len(grid)):
        for y in xrange(len(grid)):
            cell = (x,y)
            new_path = find_best_path_from(grid, [cell], path_length - 1)
            best_paths.append(new_path)
    return max_path(grid, best_paths)

def show_all_best_paths(grid, path_length):
    """Print out the best path from all possible starting points"""
    for x in xrange(len(grid)):
        for y in xrange(len(grid)):
            cell = (x,y)
            new_path = find_best_path_from(grid, [cell], path_length - 1)
            print format_path(grid, new_path)

def format_path(grid, path):
    """Format the path into a human readable string"""
    total = sum_path(grid, path)
    alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    pretty_cells = []
    for x,y in path:
        pretty_x = alpha[x]
        pretty_y = len(grid) - y
        cell = "(%s,%s)" % (pretty_x, pretty_y)
        pretty_cells.append(cell)
    return "%s: %s" % (total, " -> ".join(pretty_cells))

def main(args):
    if 2 != len(args):
        print "usage: %s input-file" % args[0]
        return 1;
    else:
        fpath = args[1]
        with open(fpath) as f:
            sea_grid = load_sea_grid(f)
        # print format_path(sea_grid, find_best_path(sea_grid, 8))
        show_all_best_paths(sea_grid, 8)
if __name__ == '__main__':
    sys.exit(main(sys.argv))
