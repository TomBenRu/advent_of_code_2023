import heapq
from collections import defaultdict

with open('input.txt') as f:
    data = f.read().strip().splitlines()

hashed_data = {(r, c): int(data[r][c]) for r in range(len(data)) for c in range(len(data[r]))}

# print(hashed_data)

start_point = (0, 0)
end_point = (len(data) - 1, len(data[0]) - 1)


class TileNode:
    def __init__(self, coord: tuple[int, int], direction: tuple[int, int],
                 heat_loss: int, sum_heat_loss: int, path: list[tuple[int, int]]):
        self.coord = coord
        self.direction = direction
        self.heat_loss = heat_loss
        self.sum_heat_loss = sum_heat_loss
        self.path = path

    def __lt__(self, other: 'TileNode'):
        return (self.sum_heat_loss, len(self.path)) < (other.sum_heat_loss, len(other.path))

    def __repr__(self):
        return f'{self.coord=}, {self.sum_heat_loss=}'


def print_path(p: list[tuple[int, int]]):
    path = set(p)
    grid = [[] for _ in range(len(data))]
    for r in range(len(data)):
        for c in range(len(data[0])):
            grid[r].append('#' if (r, c) in path else data[r][c])

    for row in grid:
        print(''.join(row))


def get_next_directions(tile: TileNode) -> set[tuple[int, int]]:
    return {(0, 1), (0, -1), (1, 0), (-1, 0)} - {tile.direction, (-tile.direction[0], -tile.direction[1])}


def min_lost(part_1: bool):
    todo, visited = [TileNode(start_point, (0, 0), 0, 0, [(0, 0)])], set()
    heapq.heapify(todo)
    path = None
    while todo:
        # print(f'{len(todo)=}')
        # print(f'{visited=}')
        t = heapq.heappop(todo)
        if (t.coord, t.direction) in visited:
            continue
        if t.coord == end_point:
            return t
        visited.add((t.coord, t.direction))
        # input(f'{t=}')
        for y, x in get_next_directions(t):
            sum_heat_loss = t.sum_heat_loss
            new_path = []
            steps = range(1, 4) if part_1 else range(1, 11)
            for s in steps:
                new_coord = t.coord[0] + y * s, t.coord[1] + x * s
                if new_coord not in hashed_data:
                    break
                sum_heat_loss += hashed_data[new_coord]
                new_path += [new_coord]
                if not part_1 and s < 4:
                    continue
                new_tile_node = TileNode(new_coord, (y, x), hashed_data[new_coord],
                                         sum_heat_loss, t.path + new_path)
                # input(f'{new_tile_node=}')
                heapq.heappush(todo, new_tile_node)


def solve(part_1: bool):
    return min_lost(part_1)


end_node_1 = solve(True)
print_path(end_node_1.path)
print(end_node_1)

end_node_2 = solve(False)
print_path(end_node_2.path)
print(end_node_2)

