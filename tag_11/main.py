import itertools
import pprint

with open('input.txt') as f:
    data = [list(line) for line in f.read().splitlines()]


def get_rows_cols_to_expand() -> tuple[list[int], list[int]]:
    row_indexes = []
    col_indexes = []
    for r in range(len(data)):
        if all(c == '.' for c in data[r]):
            row_indexes.append(r)
    for c in range(len(data[0])):
        if all(row[c] == '.' for row in data):
            col_indexes.append(c)
    return row_indexes, col_indexes


def get_galaxy_coordinates() -> list[tuple[int, int]]:
    coordinates = []
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            if col == '#':
                coordinates.append((r, c))
    return coordinates


galaxy_coordinates = get_galaxy_coordinates()
rows_to_expand, cols_to_expand = get_rows_cols_to_expand()

galaxy_pairs = itertools.combinations(galaxy_coordinates, 2)

expansion_factors = [2, 1_000_000]
sum_distances = [0, 0]


for galaxy_1, galaxy_2 in galaxy_pairs:
    y_1, y_2 = sorted([galaxy_1[0], galaxy_2[0]])
    x_1, x_2 = sorted([galaxy_1[1], galaxy_2[1]])
    for i in range(2):
        dif_y = y_2 - y_1 + sum(y_1 < r < y_2 for r in rows_to_expand) * (expansion_factors[i] - 1)
        dif_x = x_2 - x_1 + sum(x_1 < c < x_2 for c in cols_to_expand) * (expansion_factors[i] - 1)
        sum_distances[i] += dif_y + dif_x

print(f'{sum_distances[0]=}')
print(f'{sum_distances[1]=}')
