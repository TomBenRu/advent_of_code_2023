with open('test_input.txt') as f:
    workflow, ratings = f.read().strip().split('\n\n')

workflows = {
    v.split('{')[0]: [(s.split(':')[0] if len(s.split(':')) == 2 else 'True',
                       s.split(':')[1] if len(s.split(':')) == 2 else s.split(':')[0])
                      for s in v.split('{')[1][:-1].split(',')
                      ]
    for v in workflow.splitlines()
}
ratings = [{a.split('=')[0]: int(a.split('=')[1]) for a in s.strip('{}').split(',')} for s in ratings.splitlines()]

print(f'{workflows=}')
print(f'{ratings=}')


def accept_rating(rating: dict[str, int], wf_name: str):
    if wf_name == 'A':
        return sum(rating.values())
    if wf_name == 'R':
        return 0

    for condition, goal in workflows[wf_name]:
        if eval(condition, {'x': rating['x'], 'm': rating['m'], 'a': rating['a'], 's': rating['s']}):
            return accept_rating(rating, goal)


def solve():
    return sum(accept_rating(r, "in") for r in ratings)


result_1 = solve()
print(f'{result_1=}')
