import copy
import itertools
import pprint

with open('input.txt') as f:
    data = [[[t == '#' for t in line] for line in pattern.splitlines()]
            for pattern in f.read().strip().split('\n\n')]


def solve_1(pattern: list[list[bool]]):
    solutions = []
    for m, matrix in enumerate((pattern, list(zip(*pattern)))):
        for c in range(len(matrix)-1):
            if matrix[c] == matrix[c + 1]:
                rows_to_proof = min(c + 1, len(matrix) - (c + 1))
                for i in range(1, rows_to_proof):
                    if matrix[c-i] != matrix[c+1+i]:
                        break
                else:
                    solution = (100 * (c + 1), (c, m)) if m == 0 else (c + 1, (c, m))
                    solutions.append(solution)
    return solutions


def solve_2(pattern: list[list[bool]]):
    pattern = copy.deepcopy(pattern)
    old_solution, old_reflection_specifier = solve_1(pattern)[0]
    for r, line in enumerate(pattern):
        for c, tile in enumerate(line):
            pattern[r][c] = not pattern[r][c]
            new_solutions = solve_1(pattern)
            for new_solution, new_reflection_specifier in new_solutions:
                if new_reflection_specifier != old_reflection_specifier:
                    return new_solution
            pattern[r][c] = not pattern[r][c]


# sourcery skip: sum-comprehension
sum_patten_solutions_1 = 0
sum_patten_solutions_2 = 0
for p in data:
    sum_patten_solutions_1 += solve_1(p)[0][0]
    sum_patten_solutions_2 += solve_2(p)

print(f'{sum_patten_solutions_1=}')
print(f'{sum_patten_solutions_2=}')
