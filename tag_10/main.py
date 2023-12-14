import pickle
from typing import Literal


def type_from_point(data: list[str], point: tuple[int, int]) -> str:
    return data[point[0]][point[1]]


def neighbours(point: tuple[int, int]) -> list[tuple[int, int]]:
    all_neighbours = []
    for p in ((0, -1), (-1, 0), (0, 1), (1, 0)):
        if (0 <= point[0] + p[0] < len(data)) and (0 <= point[1] + p[1] < len(data[0])):
            all_neighbours.append((point[0] + p[0], point[1] + p[1]))
    return all_neighbours


def get_pipe_type_from_neighbours(data: list[str], point: tuple[int, int]) -> str:
    connections = set()
    for p in neighbours(point):
        dif_point = (p[0]-point[0], p[1]-point[1])
        if dif_point == (0, -1) and (type_from_point(data, p) in {'-', 'F', 'L'}):
            connections.add(dif_point)
        elif dif_point == (- 1, 0) and (type_from_point(data, p) in {'|', '7', 'F'}):
            connections.add(dif_point)
        elif dif_point == (0, 1) and (type_from_point(data, p) in {'-', '7', 'J'}):
            connections.add(dif_point)
        elif dif_point == (1, 0) and (type_from_point(data, p) in {'|', 'L', 'J'}):
            connections.add(dif_point)
        for pipe_type, connection in pipes.items():
            if connection == connections:
                return pipe_type


def connected_points(data: list[str], point: tuple[int, int]) -> set[tuple[int, int]]:
    pipe_type = type_from_point(data, point)
    connections: set[tuple[int, int]] = pipes[pipe_type]
    return {(point[0]+c[0], point[1]+c[1]) for c in connections
            if 0 <= point[0]+c[0] < len(data) and 0 <= point[1]+c[1] < len(data[0])
            and type_from_point(data, (point[0]+c[0], point[1]+c[1]))}


def save_data_with_path(data: list[str], visited_points: set[tuple[int, int]], inner_points: set[tuple[int, int]],
                        missed_nodes: set[tuple[int, int]], file: str):
    data_with_path = [list(line) for line in data]

    for r in range(len(data_with_path)):
        for c in range(len(data_with_path[0])):
            if (r, c) in visited_points:
                continue
            elif (r, c) in inner_points:
                data_with_path[r][c] = ' '
            elif (r, c) in missed_nodes:
                data_with_path[r][c] = 'M'
            else:
                data_with_path[r][c] = '.'

    # for p in visited_points:
    #     data_with_path[p[0]][p[1]] = 'X'
    # for i in inner_points:
    #     data_with_path[i[0]][i[1]] = ' '
    # for m in missed_nodes:
    #     data_with_path[m[0]][m[1]] = 'M'

    data_with_path = [''.join(line) for line in data_with_path]
    data_with_path = '\n'.join(data_with_path)
    with open(file, 'w') as f:
        f.write(data_with_path)


with open('input.txt') as f:
    data = f.read().strip().splitlines()

pipes = {'|': {(-1, 0), (1, 0)}, '-': {(0, -1), (0, 1)}, 'L': {(-1, 0), (0, 1)}, 'J': {(0, -1), (-1, 0)},
         '7': {(0, -1), (1, 0)}, 'F': {(0, 1), (1, 0)}}

starting_point = None
for row in range(len(data)):
    for col in range(len(data[0])):
        if data[row][col] == 'S':
            starting_point = row, col
            break
    if starting_point:
        break

starting_type = get_pipe_type_from_neighbours(data, starting_point)
data[starting_point[0]] = data[starting_point[0]].replace('S', starting_type)

curr_points = list(connected_points(data, starting_point))
visited_points = {starting_point} | set(curr_points)
distances = [1, 1]
while True:
    found = False
    for i, p in enumerate(curr_points):
        if next_point := next((n for n in connected_points(data, p)
                               if n not in visited_points and type_from_point(data, n) != '.'), None):
            distances[i] += 1
            visited_points.add(next_point)
            curr_points[i] = next_point
            found = True
    if not found:
        break

print(f'result 1: {max(distances)}')


direction_symbol_turn = {
    (0, -1): {'F': {'turn': 'left', 'new_direction': (1, 0)}, 'L': {'turn': 'right', 'new_direction': (-1, 0)}},
    (-1, 0): {'F': {'turn': 'right', 'new_direction': (0, 1)}, '7': {'turn': 'left', 'new_direction': (0, -1)}},
    (0, 1): {'7': {'turn': 'right', 'new_direction': (1, 0)}, 'J': {'turn': 'left', 'new_direction': (-1, 0)}},
    (1, 0): {'L': {'turn': 'left', 'new_direction': (0, 1)}, 'J': {'turn': 'right', 'new_direction': (0, -1)}}
}
visited_nodes = set()
path = []
curr_node = starting_point
first_neighbour = None
turns = {'right': 0, 'left': 0}

while True:
    connected = list(connected_points(data, curr_node))
    if not first_neighbour:
        first_neighbour = new_node = connected[0]
    else:
        new_node = next((n for n in connected if n not in visited_nodes), None)
    if not new_node:
        break

    if (type_n := type_from_point(data, new_node)) in 'FL7J':
        direction = (new_node[0]-curr_node[0], new_node[1]-curr_node[1])
        turn = direction_symbol_turn[direction][type_n]['turn']
        turns[turn] += 1
    visited_nodes.add(new_node)
    path.append(new_node)
    curr_node = new_node

print(turns)
print(f'{path=}')

cycle_turn: Literal['right', 'left'] = 'right' if turns['right'] > turns['left'] else 'left'


def direction_inner_node(cycle_turn: Literal['right', 'left'], direction: tuple[int, int]) -> tuple[int, int]:
    if cycle_turn == 'right':
        #  1  0  ->  0 -1
        # -1  0  ->  0  1
        #  0 -1  -> -1  0
        #  0  1  ->  1, 0

        return direction[1], -direction[0]

    if cycle_turn == 'left':
        #  1  0  ->  0  1
        # -1  0  ->  0 -1
        #  0 -1  ->  1  0
        #  0  1  -> -1, 0

        return -direction[1], direction[0]


inner_nodes = set()


def inner_nodes_from_start_node(start_node: tuple[int, int]):
    global inner_nodes
    curr_neighbours = {n for n in neighbours(start_node) if n not in visited_nodes and n not in inner_nodes}
    inner_nodes |= curr_neighbours
    for n in curr_neighbours:
        inner_nodes_from_start_node(n)


for i in range(-2, len(path) - 2):
    # Wegen Eckverbindungen müssen die direction von der vorhergehenden Node zur aktuellen Node und die direktion
    # von der aktuellen Node zur nachfolgenden Node für die aktuelle Node zugrunde gelegt werden.
    direction_1 = path[i+1][0] - path[i][0], path[i+1][1] - path[i][1]
    direction_2 = path[i+2][0] - path[i+1][0], path[i+2][1] - path[i+1][1]
    dir_inner_node_1 = direction_inner_node(cycle_turn, direction_1)
    dir_inner_node_2 = direction_inner_node(cycle_turn, direction_2)
    inner_node_1 = path[i+1][0] + dir_inner_node_1[0], path[i+1][1] + dir_inner_node_1[1]
    inner_node_2 = path[i+1][0] + dir_inner_node_2[0], path[i+1][1] + dir_inner_node_2[1]
    for inner_node in (inner_node_1, inner_node_2):
        if (inner_node not in visited_nodes) and (inner_node not in inner_nodes):
            print(f'{path[i+1]=}, {inner_node=}')
            inner_nodes.add(inner_node)
            inner_nodes_from_start_node(inner_node)

print(f'{len(inner_nodes)=}')
with open('solved_nodes.pkl', 'rb') as f:
    solved_nodes = pickle.load(f)
solved_nodes = list(solved_nodes)
for i, (x, y) in enumerate(solved_nodes):
    solved_nodes[i] = (y-1, x-1)
solved_nodes = set(solved_nodes)

missed_nodes = solved_nodes - inner_nodes

save_data_with_path(data, set(path), solved_nodes, missed_nodes, 'data_solved.txt')
save_data_with_path(data, set(path), inner_nodes, missed_nodes, 'data_try.txt')
