import pprint

with open('input.txt') as f:
    data = f.read().strip().split(',')


def number_from_string(lable: str) -> int:
    result = 0
    for c in lable:
        result += ord(c)
        result *= 17
        result %= 256
    return result


def solve_1():
    sum_results = 0
    for step in data:
        result = number_from_string(step)
        sum_results += result

    return sum_results


def label_boxes():
    lb = {}
    for step in data:
        lable = step[:-1].split('=')[0]
        lb[lable] = number_from_string(lable)
    return lb


print(f'part 1: {solve_1()}')


labels_focal_lengths = [(v.split('=')[0], int(v.split('=')[1])) if v[-1] != '-' else (v[:-1], None) for v in data]
labels_boxes = label_boxes()
boxes = {i: [] for i in range(256)}


def solve_2():
    for lb, focal_length in labels_focal_lengths:
        box = labels_boxes[lb]
        if focal_length:
            for l in boxes[box]:
                if l[0] == lb:
                    l[1] = focal_length
                    break
            else:
                boxes[box].append([lb, focal_length])
        else:
            for i, l in enumerate(boxes[box]):
                if l[0] == lb:
                    boxes[box].pop(i)

    sum_results = 0

    for box_num, content in boxes.items():
        for pos, (_, focal_length) in enumerate(content, start=1):
            sum_results += (zw := (box_num + 1) * pos * focal_length)

    return sum_results


print(f'part 2: {solve_2()}')
