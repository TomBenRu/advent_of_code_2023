import functools
import math
import pprint

with open('input.txt') as f:
    instructions, map_data = f.read().strip().split('\n\n')

instructions: str
instructions = [int(v) for v in instructions.replace('R', '1').replace('L', '0')]
map_data = {line.split(' = ')[0]: line.split(' = ')[1].strip('()').split(', ') for line in map_data.splitlines()}

print(instructions)
print(map_data)

curr_element = 'AAA'

index = 0
while True:
    curr_element = map_data[curr_element][instructions[index % len(instructions)]]
    if curr_element == 'ZZZ':
        break
    index += 1

print('result 1:', index + 1)


with open('input.txt') as f:
    instructions, map_data = f.read().strip().split('\n\n')

instructions: str
instructions = [int(v) for v in instructions.replace('R', '1').replace('L', '0')]
map_data = {line.split(' = ')[0]: line.split(' = ')[1].strip('()').split(', ') for line in map_data.splitlines()}

curr_nodes = [k for k in map_data.keys() if k[2] == 'A']

results_mean = {}
for element in curr_nodes:
    index = 0
    curr_element = element
    turns_to_first_goal = 0
    turns_of_cycle = 0
    first_goal = ''
    while True:
        curr_element = map_data[curr_element][instructions[index % len(instructions)]]
        if first_goal:
            if curr_element == first_goal:
                turns_of_cycle = index + 1 - turns_to_first_goal
                break

        elif curr_element[2] == 'Z':
            turns_to_first_goal = index + 1
            first_goal = curr_element
        index += 1

    results_mean[element] = {'first_goal': first_goal,
                             'turns_to_first_goal': turns_to_first_goal,
                             'turns_of_cycle': turns_of_cycle}


def kgv(*args):
    def kgv_zwei(a, b):
        return abs(a*b) // math.gcd(a, b)
    return functools.reduce(kgv_zwei, args)


start_node_max_cycle, max_cycle = max([(k, v['turns_of_cycle']) for k, v in results_mean.items()], key=lambda x: x[1])

index = 0
while True:
    if index % 1_000_000 == 0:
        print(f'{index=}')
    value = results_mean[start_node_max_cycle]['turns_to_first_goal'] + max_cycle * index
    if not any((value - v['turns_to_first_goal']) % v['turns_of_cycle']
               for k, v in results_mean.items() if k != start_node_max_cycle):
        break
    index += 1

print('result 2:', results_mean[start_node_max_cycle]['turns_to_first_goal'] + index * max_cycle)


