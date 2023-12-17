import functools
import itertools
import re
import sys
import time

with open('input.txt') as f:
    data = [[line.split()[0], [int(n) for n in line.split()[1].split(',')]] for line in f.read().strip().splitlines()]

part_2 = True
factor = 5
if part_2:
    for line in data:
        line[0] = line[0] + ('?' + line[0]) * (factor - 1)
        line[1] = line[1] * factor

# print(data)


def pattern_from_groups(groups: list[int]) -> str:
    pattern = r'[?\.]*'
    for i, g in enumerate(groups):
        if i == len(groups) - 1:
            pattern += f'[#?]{{{g}}}[?\.]*'
        else:
            pattern += f'[#?]{{{g}}}[?\.]+'
    return pattern


def pattern_from_groups_2(groups: list[int], num_groups: int) -> str:
    # sourcery skip: assign-if-exp, use-join
    pattern = r''
    for i in range(num_groups):
        if i == 0:
            pattern += f'\.*#{{{groups[i]}}}'
        else:
            try:
                pattern += f'\.+#{{{groups[i]}}}'
            except IndexError as e:
                input(f'{e=}, {i=}, {groups=}')
    if num_groups == len(groups):
        pattern += '\.*'
    return pattern


def get_min_needed_tiles(curr_springs: str, groups: list[int], curr_index_to_put_in: int) -> int:
    needed_damaged_springs = sum(groups) - curr_springs.count('#')
    needed_groups = []
    for g in sorted(groups, reverse=True):
        needed_groups.append(g)
        if sum(needed_groups) >= needed_damaged_springs:
            break

    min_sum_free_tiles = len(needed_groups) + (curr_springs[curr_index_to_put_in-1] == '.') + (curr_springs[-1] == '.')

    return needed_damaged_springs + min_sum_free_tiles


def check_valid(springs_mod: str, pattern: str) -> bool:
    return bool(re.fullmatch(pattern, springs_mod))


def check_valid_2(springs_mod: str, pattern: str, final=False) -> tuple[bool, int | None]:
    match = re.fullmatch(pattern, springs_mod) if final else re.match(pattern, springs_mod)
    return bool(match), match.end() - 1 if match else None


@functools.cache
def find_results_2(curr_springs: str, groups: tuple[int, ...]) -> int:
    curr_springs = curr_springs.lstrip('.')
    if not curr_springs:
        return not groups
    if not groups:
        return '#' not in curr_springs
    if curr_springs[0] == '#':
        if len(curr_springs) < groups[0]:
            return 0
        if '.' in curr_springs[:groups[0]]:
            return 0
        if curr_springs[groups[0]] == '#':
            return 0
        return find_results_2(curr_springs[groups[0]+1:], tuple(groups[1:]))

    return find_results_2('#' + curr_springs[1:], groups) + find_results_2(curr_springs[1:], groups)



def find_results(curr_springs: str, groups: list[int], pattern: str, index_last_input: int):
    # sourcery skip: use-fstring-for-concatenation
    sure_broken = curr_springs.count('#')
    sum_broken = sum(groups)
    broken_springs_to_put_in = sum_broken - sure_broken

    if not broken_springs_to_put_in and check_valid(curr_springs, pattern):
        sum_possible_strings[0] += 1
        # print('found:', sum_possible_strings[0])
        # if sum_possible_strings[0] > 17000:
        #     print(f'{groups=}')
        #     input(f'{curr_springs=}')
        return True

    indexes_question_marks = [i for i in range(index_last_input+1, len(curr_springs)) if curr_springs[i] == '?']

    if indexes_question_marks:
        curr_index_to_put_in = indexes_question_marks[0]

        if len(curr_springs) - index_last_input < get_min_needed_tiles(curr_springs, groups, curr_index_to_put_in):
            # print('yeah!')
            return False

    for i in indexes_question_marks:
        new_springs = curr_springs[:i] + '#' + curr_springs[i+1:]
        # input(f'{new_springs=}')
        if check_valid(new_springs, pattern):
            # input('valid')
            find_results(new_springs, groups, pattern, i)
    return False

t0 = time.time()
sum_possible_strings = [0]
sum_possible_strings_2 = 0
all_current_springs = set()
for i, (springs, groups) in enumerate(data, start=1):
    all_current_springs = set()
    # if i != 3: continue
    # print(f'{springs=}, {groups=} --------------------------------------------------------------')
    pattern = pattern_from_groups(groups)
    # find_results(springs, groups, pattern, -1)
    sum_possible_strings_2 += find_results_2(springs + '.', tuple(groups))

    # print(f'{sum_possible_strings_2=}, done: {i} / {len(data)}, Zeit: {int(time.time()-t0)}')

print(f'{sum_possible_strings_2=}')
