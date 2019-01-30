rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[rows[i]+cols[i] for i in range(9)], [rows[i]+cols[8-i] for i in range(9)]]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    if len(grid) != 81:
        return {}
    rows = 'ABCDEFGHI'
    cols = '123456789'
    f = lambda x: x if x != '.' else cols
    return {rows[x//9]+cols[x%9]: f(grid[x]) for x in range(81)}


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:eiddccglbtfljjnnfeuceljigglkueercckhhefeiftd

        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    values_elim = values.copy()
    for k, v in values.items():
        if len(v) == 1:
            for n in peers[k]:
                values_elim[n] = values_elim[n].replace(v,'')
    return values_elim


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for d in '123456789':
            cells = [x for x in unit if d in values[x]]
            if len(cells) == 1:
                values[cells[0]] = d
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    

def search(values):
    """
    Using depth-first search and propagation, create a search tree and solve the sudoku.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    # Solved
    if sum(len(v) > 1 for v in values.values()) == 0: 
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    non_solved = {k:len(v) for k,v in values.items() if len(v) > 1}
    key_min = min(non_solved.keys(), key=non_solved.get)
    # Recursion to solve each one of the resulting sudokus
    for val in values[key_min]:
        values_copy = values.copy()
        values_copy[key_min] = val
        leaf = search(values_copy)
        if leaf:
            return leaf


def naked_twins(values):
    out = values.copy()
    for k, v in values.items():
        if len(v) == 2:
            for n in peers[k]:
                if values[n] == v:
                    for n1 in peers[k].intersection(peers[n]):
                        for d in v:
                            out[n1] = out[n1].replace(d,'')
    return out
                                

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)  
