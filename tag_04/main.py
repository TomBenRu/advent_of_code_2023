with open('input.txt') as f:
    data = [line.split(':')[1].split('|') for line in f.read().strip().splitlines()]
    data = [[1, [{int(num) for num in winning.split()}, {int(num) for num in control.split()}]] for winning, control in data]

print(data)

sum_scores = 0
for _, (winning, control) in data:
    matching = winning & control
    score = 2 ** (len(matching) - 1) if matching else 0
    sum_scores += score

print(f'{sum_scores=}')

for index, (n, (winning, control)) in enumerate(data):
    matching = winning & control
    for c in range(1, len(matching) + 1):
        if index + c < len(data):
            data[index + c][0] += n

print(f'{sum(card[0] for card in data)=}')


