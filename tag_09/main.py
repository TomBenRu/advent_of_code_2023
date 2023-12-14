import pprint

with open('input.txt') as f:
    data = [[int(v) for v in line.split()] for line in f.read().strip().splitlines()]

sum_predictions = 0

for line in data:
    lines = [line.copy()]
    while True:
        lines.append([])
        for i in range(len(lines[-2])-1):
            lines[-1].append(lines[-2][i+1] - lines[-2][i])
        if not any(lines[-1]):
            break
    for i in range(len(lines)-1, 0, -1):
        lines[i-1].append(lines[i-1][-1] + lines[i][-1])
    sum_predictions += (res := lines[0][-1])

print(f'{sum_predictions=}')


sum_predictions_2 = 0

for line in data:
    lines = [line.copy()]
    while True:
        lines.append([])
        for i in range(len(lines[-2])-1):
            lines[-1].append(lines[-2][i+1] - lines[-2][i])
        if not any(lines[-1]):
            break
    for i in range(len(lines)-1, 0, -1):
        lines[i-1].insert(0, lines[i-1][0] - lines[i][0])
    sum_predictions_2 += (res := lines[0][0])

print(f'{sum_predictions_2=}')

