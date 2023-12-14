import math

with open('input.txt') as f:
    data = f.read()

data_1 = [[int(v) for v in line.split(':')[1].split()] for line in data.strip().splitlines()]
data_2 = [int(line.split(':')[1].replace(' ', '')) for line in data.strip().splitlines()]

print(data_1)
print(data_2)


def best_distance(time: int):
    t_load = time / 2
    return t_load


def t_loads_from_distance(time: int, distance: int) -> tuple[int, int]:
    t_load_1 = (time / 2) - ((time / 2) ** 2 - distance) ** 0.5
    t_load_2 = (time / 2) + ((time / 2) ** 2 - distance) ** 0.5
    return t_load_1, t_load_2


def distance_from_t_load(time: int, t_load: int) -> int:
    distance = (time - t_load) * t_load
    return distance


result_1 = 1
for time, distance in zip(data_1[0], data_1[1]):
    t_1, t_2 = t_loads_from_distance(time, distance)
    better_t_loads = math.ceil(t_2) - int(t_1) - 1
    result_1 *= better_t_loads

print(f'{result_1=}')

t_1, t_2 = t_loads_from_distance(data_2[0], data_2[1])
result_2 = math.ceil(t_2) - int(t_1) - 1

print(f'{result_2=}')



