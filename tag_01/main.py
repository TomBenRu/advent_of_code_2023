with open('input.txt') as f:
    data = f.read().strip().splitlines()

result_1 = sum(int([c for c in line if c.isnumeric()][0] + [c for c in line if c.isnumeric()][-1]) for line in data)

print(f'{result_1=}')

with open('input.txt') as f:
    data = f.read().strip().splitlines()

num_words = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8',
             'nine': '9'}

for i, line in enumerate(data):
    line: str
    new_line = ''
    for j, c in enumerate(line):
        if c.isnumeric():
            new_line += c
        else:
            for num in num_words:
                if line[j:].startswith(num):
                    new_line += num_words[num]
    data[i] = new_line

result_2 = sum(int([c for c in line if c.isnumeric()][0] + [c for c in line if c.isnumeric()][-1]) for line in data)

print(f'{result_2=}')
