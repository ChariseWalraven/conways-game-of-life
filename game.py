# from preloaded import htmlize  # this can help you debug your code
from itertools import product


def get_generation(
    cells: list[list[int]],
    generations: int,
) -> list[list[int]]:

    result = []
    for _ in range(generations):
        next_gen_cells = []
        cells = pad_cells(cells)

        for row_idx, row in enumerate(cells):
            next_gen_row = []
            for cell_idx, cell in enumerate(row):

                # get all neighbours and put in a single list, then check the
                # amount of live neighbours
                # get positions of all neighbours
                co_ord_shifter = range(-1, 2)  # returns a list with
                # values to shift coordinates by

                # get all combinations for both x and y shifts
                combis = product(co_ord_shifter, co_ord_shifter)

                # get list of xy combinations of neighbours, filter for coords
                # that are in bounds and not the current element's coords
                neighbours_cr_coords = filter(
                    lambda cr: (
                        is_cell_in_range(cr[0], row)
                        and is_row_in_range(cr[1], cells)
                        and not is_current_cell(cr, (cell_idx, row_idx))
                    ),
                    map(
                        lambda cr: (cell_idx + cr[0], row_idx + cr[1]),
                        combis,
                    ),
                )

                neighbours = []

                for cr in neighbours_cr_coords:
                    c_idx, r_idx = cr
                    # BUG: out of index in test 2 (not sure which gen)
                    c = cells[r_idx][c_idx]

                    neighbours.append(c)

                num_live_neighbours = len([n for n in neighbours if n == 1])

                is_cell_alive = cell == 1
                is_cell_dead = cell == 0

                # fmt: off
                should_cell_survive = is_cell_alive \
                    and 2 <= num_live_neighbours <= 3
                # fmt: on

                should_cell_revive = is_cell_dead and num_live_neighbours == 3

                cell = 1 if should_cell_survive or should_cell_revive else 0

                next_gen_row.append(cell)
            next_gen_cells.append(next_gen_row)

            # remove empty rows and columns

        next_gen_cells = [r for r in next_gen_cells if 1 in r]
        inv_next_gen_cells = invert_cells(next_gen_cells)
        next_gen_cells = [r for r in inv_next_gen_cells if 1 in r]
        next_gen_cells = invert_cells(next_gen_cells)

        result = next_gen_cells

    return result


# invert cell rows and columns
def invert_cells(cells):
    inv_cells = []
    cell_len = len(cells[0])
    for c_idx in range(cell_len):
        inv_row = []
        for r_idx in range((len(cells))):
            inv_row.append(cells[r_idx][c_idx])
        inv_cells.append(inv_row)
    return inv_cells


def pad_cells(cells):
    padded_cell = [0 for i in range(len(cells[0]) + 2)]
    board = [padded_cell, *(pad_row(row) for row in cells), padded_cell]

    return board


def pad_row(row):
    row.insert(0, 0)
    row.append(0)
    return row


def is_cell_in_range(cell_idx, row):
    return len(row) > cell_idx > -1


def is_row_in_range(row_idx, cells):
    return len(cells) > row_idx > -1


def is_current_cell(xy, curr_cell_coords):
    return xy == curr_cell_coords


tests = [
    [
        [1, 0, 0],
        [0, 1, 1],
        [1, 1, 0],
    ],
    [
        [1, 1, 1, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 1, 1, 1],
    ],
]

res = get_generation(tests[1], 16)

desired_res = [
    [
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1],
    ],
    [
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    ],
]

print(res)
