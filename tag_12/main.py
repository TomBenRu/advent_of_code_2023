import itertools
import re
import sys
import time

with open('test_input.txt') as f:
    data = [[line.split()[0], [int(n) for n in line.split()[1].split(',')]] for line in f.read().strip().splitlines()]

part_2 = True
factor = 1
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
    pattern = r'\.*'
    for i in range(num_groups):
        if i == len(groups) -1:
            pattern += f'#{{{groups[i]}}}\.*'
        else:
            pattern += f'##{{{groups[i]}}}\.*'
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


def check_valid_2(springs_mod: str, pattern: str) -> bool:
    return bool(re.match(pattern, springs_mod))


def find_results_2(curr_springs: str, groups: list[int], index_last_input: int, index_last_group: int):
    sure_broken = curr_springs.count('#')
    sum_broken = sum(groups)
    pattern = pattern_from_groups_2(groups, index_last_group + 2)
    broken_springs_to_put_in = sum_broken - sure_broken
    if not broken_springs_to_put_in and check_valid(curr_springs, pattern):
        sum_possible_strings[0] += 1
        return True
    indexes_question_marks = [i for i in range(index_last_input+1, len(curr_springs)) if curr_springs[i] == '?']

    curr_group = groups[index_last_group+1]
    all_new_springs = [curr_springs]
    for g in range(curr_group):
        for q in indexes_question_marks:
            for i in range(g):
                new_springs = all_new_springs[-1][:q] + '#'
            new_springs += '.' if all_new_springs[-1][q+1] in {'.', }

    for i in indexes_question_marks:
        for j in range(curr_group):
            new_springs = new_springs[:i] + '#' + curr_springs[i+1+j:]
            if check_valid_2(new_springs+'.', pattern):
                find_results_2(new_springs+'.', groups, i + j, index_last_group+1)
    return False


def find_results(curr_springs: str, groups: list[int], pattern: str, index_last_input: int):
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
for i, (springs, groups) in enumerate(data, start=1):
    print(f'{springs=}, {groups=} --------------------------------------------------------------')
    pattern = pattern_from_groups(groups)
    # find_results(springs, groups, pattern, -1)
    find_results_2(springs, groups, -1, -1)
    print(f'{sum_possible_strings[0]=}, remaining: {len(data) - i}, Zeit: {int(time.time()-t0)}')

print(f'{sum_possible_strings[0]=}')
