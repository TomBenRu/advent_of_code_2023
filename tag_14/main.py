import copy
import pprint
import sys
from typing import Literal

with open('input.txt') as f:
    data = f.read().strip().splitlines()

data_hashed = {}
for r, line in enumerate(data):
    for c, tile in enumerate(line):
        data_hashed[(r, c)] = tile

# print(data_hashed)


def print_data_hashed(curr_data: dict[tuple[int, int], str]):
    sorted_keys = sorted(curr_data.keys(), key=lambda x: (x[0], x[1]))
    curr_row_number = -1
    matrix = []
    for r, c in sorted_keys:
        if r != curr_row_number:
            matrix.append(curr_data[(r, c)])
        else:
            matrix[-1] += curr_data[(r, c)]
        curr_row_number = r
    for line in matrix:
        print(line)


def hashable_thing_from_dict(thing: dict[tuple[int, int], str]):
    sorted_keys = sorted(thing.keys(), key=lambda x: (x[0], x[1]))
    curr_row_number = -1
    matrix = []
    for r, c in sorted_keys:
        if r != curr_row_number:
            matrix.append(thing[(r, c)])
        else:
            matrix[-1] += thing[(r, c)]
        curr_row_number = r
    return tuple(matrix)


def tilt_north_south(curr_data_hashed: dict[tuple[int, int], str], direction: Literal['north', 'south']):
    data_hashed_for_tilting = {k: t for k, t in curr_data_hashed.items() if t == '#'}
    line_nums = range(len(data)) if direction == 'north' else range(len(data) - 1, -1, -1)
    for r in line_nums:
        for c in range(len(data[r])):
            if curr_data_hashed[(r, c)] == 'O':
                # print(f'{curr_data_hashed[(r, c)]=}')
                curr_data_hashed[(r, c)] = '.'
                coord = r, c
                while True:
                    if direction == 'north':
                        coord_new = coord[0] - 1, coord[1]
                    else:
                        coord_new = coord[0] + 1, coord[1]
                    if not curr_data_hashed.get(coord_new) or coord_new in data_hashed_for_tilting:
                        data_hashed_for_tilting[coord] = 'O'
                        # print(f'{data_hashed_for_tilting[coord]=}')
                        break
                    coord = coord_new

    load = 0
    for (r, _), rock in data_hashed_for_tilting.items():
        if rock == 'O':
            load += len(data) - r

    new_data_hashed = {coord: data_hashed_for_tilting[coord] if data_hashed_for_tilting.get(coord) else t
                       for coord, t in curr_data_hashed.items()}

    return load, new_data_hashed


def tilt_west_east(curr_data_hashed: dict[tuple[int, int], str], direction: Literal['west', 'east']):
    data_hashed_for_tilting = {k: t for k, t in curr_data_hashed.items() if t == '#'}
    col_nums = range(len(data[0])) if direction == 'west' else range(len(data) - 1, -1, -1)
    for r in range(len(data)):
        for c in col_nums:
            tile = curr_data_hashed[(r, c)]
            if tile == 'O':
                curr_data_hashed[(r, c)] = '.'
                coord = r, c
                while True:
                    if direction == 'west':
                        coord_new = coord[0], coord[1] - 1
                    else:
                        coord_new = coord[0], coord[1] + 1
                    if not curr_data_hashed.get(coord_new) or coord_new in data_hashed_for_tilting:
                        data_hashed_for_tilting[coord] = 'O'
                        break
                    coord = coord_new
    load = 0
    for (r, _), rock in data_hashed_for_tilting.items():
        if rock == 'O':
            load += len(data) - r

    new_data_hashed = {coord: data_hashed_for_tilting[coord] if data_hashed_for_tilting.get(coord) else t
                       for coord, t in curr_data_hashed.items()}

    return load, new_data_hashed


result_1, _ = tilt_north_south(copy.deepcopy(data_hashed), 'north')
print(f'{result_1=}')


new_hashed_data = data_hashed
results = {}
result_2 = 0
first_appearance = None
for i in range(1, 1_000_000_001):
    for d in ('north', 'west', 'south', 'east'):
        result, new_hashed_data = (tilt_north_south(new_hashed_data, d) if d in {'north', 'south'}
                                   else tilt_west_east(new_hashed_data, d))
        if (hashable := hashable_thing_from_dict(new_hashed_data)) in results and d == 'east':
            cycle = i - results[hashable]
            if first_appearance is None:
                first_appearance = (1_000_000_000 - i) % cycle + i

        if i == first_appearance and d == 'east':
            result_2 = result
            break

    else:
        results[hashable] = i
        continue
    break


print(f'{result_2=}')
