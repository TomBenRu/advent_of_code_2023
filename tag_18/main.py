import shapely

directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

with open('input.txt') as f:
    data = [(directions[line.split()[0]], int(line.split()[1]), line.split()[2].strip('()'))
            for line in f.read().strip().splitlines()]
print(data)
start_cube = (0, 0)


def generate_grid():
    path = {}
    curr_coord = start_cube
    for instr_num, (direction, length, color) in enumerate(data):
        for step in range(1, length + 1):
            new_coord = curr_coord[0] + direction[0], curr_coord[1] + direction[1]
            if step == length:
                next_instr_num = (instr_num + 1) % len(data)
                relevant_for_area = ((direction == (1, 0) and data[next_instr_num][0] == (0, -1))
                                     or direction == (0, -1) and data[next_instr_num][0] == (-1, 0)
                                     or direction == (1, 0) and data[next_instr_num][0] == (0, 1)
                                     or direction == (0, 1) and data[next_instr_num][0] == (-1, 0))
            else:
                relevant_for_area = direction in ((1, 0), (-1, 0))
            path[new_coord] = (color, direction, relevant_for_area)
            curr_coord = new_coord

    min_x, min_y, max_x, max_y = (min(x for _, x in path), min(y for y, _ in path),
                                  max(x for _, x in path), max(y for y, _ in path))
    grid = {}
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            grid[(y-min_y, x-min_x)] = path.get((y, x)) or (None, None, False)

    return grid, len(path)


def get_area(grid: dict[tuple[int, int], tuple[str | None, tuple[int, int] | None, bool]], len_path: int):
    area = 0
    for coord, (color, direction, relevant_for_area) in grid.items():
        if not direction:
            count = 0
            next_coord = coord[0], coord[1] - 1
            while grid.get(next_coord):
                if grid[next_coord][2]:
                    count += 1
                next_coord = next_coord[0], next_coord[1] - 1
            if count % 2:
                area += 1
    return area + len_path


def generate_corners(instructions: list[tuple[tuple[int, int], int]]) -> list[tuple[int, int]]:
    corners = [(0, 0)]
    for direction, steps in instructions:
        corners.append((corners[-1][0] + direction[0] * steps, corners[-1][1] + direction[1] * steps))
    return corners


def calculate_shape(corners: list[tuple[int, int]]) -> int:
    polygon = shapely.Polygon(corners)
    area = polygon.area
    length = polygon.length
    return area + length / 2 + 1


def solve(part_1: bool):
    # grid, len_path = generate_grid()
    # return get_area(grid, len_path)
    directions_2 = {'0': (0, 1), '1': (1, 0), '2': (0, -1), '3': (-1, 0)}
    instructions = ([(d, s) for d, s, _ in data] if part_1
                    else [(directions_2[c[-1]], int(c[1:-1], 16)) for _, _, c in data])
    return int(calculate_shape(generate_corners(instructions)))


result_1 = solve(True)
print(f'{result_1=}')
result_2 = solve(False)
print(f'{result_2=}')
