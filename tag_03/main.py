with open('input.txt') as f:
    data = f.read().strip().splitlines()

adjacents = {(0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)}

sum_numbers = 0
row_index, col_index = 0, 0
while row_index < len(data) and col_index < len(data[0]):
    new_col_index = col_index
    symbol: str = data[row_index][col_index]
    if symbol.isnumeric():
        for a in adjacents:
            adj_y, adj_x = row_index + a[0], col_index + a[1]
            if 0 <= adj_y < len(data) and 0 <= adj_x < len(data[0]):
                if not data[adj_y][adj_x].isnumeric() and data[adj_y][adj_x] != '.':
                    num = data[row_index][col_index]
                    for i in range(col_index-1, -1, -1):
                        if (num_before := data[row_index][i]).isnumeric():
                            num = num_before + num
                        else:
                            break
                    for j in range(col_index+1, len(data[0])):
                        if (num_after := data[row_index][j]).isnumeric():
                            num += num_after
                            new_col_index = j
                        else:
                            break
                    sum_numbers += int(num)
    if new_col_index + 1 < len(data[0]):
        col_index = new_col_index + 1
    else:
        col_index = 0
        row_index += 1

print(f'{sum_numbers=}')


sum_gear_ratio = 0

for row_index, row in enumerate(data):
    for col_index, symbol in enumerate(row):
        nums = []
        if symbol == '*':
            used_adjacents = set()
            for a in adjacents:
                adj_y, adj_x = row_index + a[0], col_index + a[1]
                if (adj_y, adj_x) in used_adjacents:
                    continue
                used_adjacents.add((adj_y, adj_x))
                if 0 <= adj_y < len(data) and 0 <= adj_x < len(data[0]):
                    if data[adj_y][adj_x].isnumeric():
                        num = data[adj_y][adj_x]
                        for i in range(adj_x-1, -1, -1):
                            if (adj_y, i) in used_adjacents:
                                break
                            used_adjacents.add((adj_y, i))
                            if (num_before := data[adj_y][i]).isnumeric():
                                num = num_before + num
                            else:
                                break
                        for j in range(adj_x+1, len(data[0])):
                            if (adj_y, j) in used_adjacents:
                                break
                            used_adjacents.add((adj_y, j))
                            if (num_after := data[adj_y][j]).isnumeric():
                                num += num_after
                            else:
                                break

                        nums.append(int(num))
        if len(nums) == 2:
            sum_gear_ratio += nums[0] * nums[1]

print(f'{sum_gear_ratio=}')
