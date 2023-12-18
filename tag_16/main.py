import sys
from collections import defaultdict


sys.setrecursionlimit(15000)


with open('input.txt') as f:
    data = f.read().strip().splitlines()

hashed_data = {}
for r, line in enumerate(data):
    for c, t in enumerate(line):
        hashed_data[(r, c)] = t

start_coord = (0, 0)
start_direction = (0, 1)

energized_tiles = defaultdict(int)
visited = set()
'''
tile: /
(1, 2), ( 0, +1) -> (0, 2), (-1, 0)
(1, 2), ( 0, -1) -> (2, 2), (+1, 0)
(1, 2), ( 1,  0) -> (1, 1), ( 0,-1)
(1, 2), (-1,  0) -> (1, 3), ( 0,+1)
tile: \\
(1, 2), ( 0, +1) -> (2, 2), (+1, 0)
(1, 2), ( 0, -1) -> (0, 2), (-1, 0)
(1, 2), ( 1,  0) -> (1, 3), ( 0,+1)
(1, 2), (-1,  0) -> (1, 1), ( 0,-1)
'''


def print_energized_grid():
    energized = [['.' for _ in range(len(data[0]))] for _ in range(len(data))]
    for y, x in energized_tiles:
        energized[y][x] = '#'

    for line in energized:
        print(''.join(line))


def start_tiles_with_directions_part_2():
    start_tiles_directions = []
    for y, x in [v for v in hashed_data if v[0] in (0, len(data) - 1) or v[1] in (0, len(data[0]) - 1)]:
        if y == x == 0:
            start_tiles_directions += [((y, x), (1, 0)), ((y, x), (0, 1))]
        elif y == 0 and x == len(data[0]) - 1:
            start_tiles_directions += [((y, x), (1, 0)), ((y, x), (0, -1))]
        elif y == len(data) - 1 and x == 0:
            start_tiles_directions += [((y, x), (-1, 0)), ((y, x), (0, 1))]
        elif y == len(data) - 1 and x == len(data[0]) - 1:
            start_tiles_directions += [((y, x), (-1, 0)), ((y, x), (0, -1))]
        elif y == 0:
            start_tiles_directions.append(((y, x), (1, 0)))
        elif y == len(data) - 1:
            start_tiles_directions.append(((y, x), (-1, 0)))
        elif x == 0:
            start_tiles_directions.append(((y, x), (0, 1)))
        elif x == len(data[0]) - 1:
            start_tiles_directions.append(((y, x), (0, -1)))
        else:
            raise ValueError('Sehr komisch!!!')
    return start_tiles_directions


def transform_slash(tile_coord, direction):
    next_tile_coord = tile_coord[0] - direction[1], tile_coord[1] - direction[0]
    next_direction = -direction[1], -direction[0]
    return next_tile_coord, next_direction


def transform_backslash(tile_coord, direction):
    next_tile_coord = tile_coord[0] + direction[1], tile_coord[1] + direction[0]
    next_direction = direction[1], direction[0]
    return next_tile_coord, next_direction


def pass_tile(tile_coord, direction):
    if tile_coord in hashed_data:
        # input(f'{tile_coord=}, {direction=}, {hashed_data[tile_coord]=}')
        energized_tiles[tile_coord] += 1
        if (tile_coord, direction) in visited:
            return False
        visited.add((tile_coord, direction))
    else:
        return False
    if hashed_data[tile_coord] == '/':
        next_tile_coord, next_direction = transform_slash(tile_coord, direction)
        pass_tile(next_tile_coord, next_direction)
    elif hashed_data[tile_coord] == '\\':
        next_tile_coord, next_direction = transform_backslash(tile_coord, direction)
        pass_tile(next_tile_coord, next_direction)
    elif hashed_data[tile_coord] == '|':
        if direction[1] == 0:
            next_tile_coord = tile_coord[0] + direction[0], tile_coord[1] + direction[1]
            next_direction = direction
            pass_tile(next_tile_coord, next_direction)
        else:
            next_tile_coord_1, next_direction_1 = transform_slash(tile_coord, direction)
            next_tile_coord_2, next_direction_2 = transform_backslash(tile_coord, direction)
            pass_tile(next_tile_coord_1, next_direction_1)
            pass_tile(next_tile_coord_2, next_direction_2)
    elif hashed_data[tile_coord] == '-':
        if direction[0] == 0:
            next_tile_coord = tile_coord[0] + direction[0], tile_coord[1] + direction[1]
            next_direction = direction
            pass_tile(next_tile_coord, next_direction)
        else:
            next_tile_coord_1, next_direction_1 = transform_slash(tile_coord, direction)
            next_tile_coord_2, next_direction_2 = transform_backslash(tile_coord, direction)
            pass_tile(next_tile_coord_1, next_direction_1)
            pass_tile(next_tile_coord_2, next_direction_2)
    else:
        next_tile_coord = tile_coord[0] + direction[0], tile_coord[1] + direction[1]
        next_direction = direction
        pass_tile(next_tile_coord, next_direction)


def solve():
    pass_tile(start_coord, start_direction)
    result_part_1 = len(energized_tiles)

    result_part_2 = 0
    for coord, direction in start_tiles_with_directions_part_2():
        energized_tiles.clear()
        visited.clear()
        pass_tile(coord, direction)
        result_part_2 = max(result_part_2, len(energized_tiles))

    return result_part_1, result_part_2


part_1, part_2 = solve()

print(f'{part_1=}')
print(f'{part_2=}')
