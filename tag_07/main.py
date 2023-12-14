import collections

with open('input.txt') as f:
    data = dict([[line.split()[0], int(line.split()[1])] for line in f.read().strip().splitlines()])

print(data)

card_ranks_1 = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, 'T': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
card_ranks_2 = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, 'T': 9, 'J': 0, 'Q': 11, 'K': 12, 'A': 13}
type_ranks = {(1, 1, 1, 1, 1): 1, (1, 1, 1, 2): 2, (1, 2, 2): 3, (1, 1, 3): 4, (2, 3): 5, (1, 4): 6, (5,): 7}

hand_type_ranks = []
for hand, score in data.items():
    counter = collections.Counter(hand)
    type_rank = type_ranks[tuple(sorted(counter.values()))]
    hand_type_ranks.append((hand, type_rank))

hand_type_ranks.sort(key=lambda x: (x[1], card_ranks_1[x[0][0]], card_ranks_1[x[0][1]], card_ranks_1[x[0][2]],
                                    card_ranks_1[x[0][3]], card_ranks_1[x[0][4]]))

result_1 = 0
for i, (hand, _) in enumerate(hand_type_ranks, start=1):
    result_1 += i * data[hand]

print(f'{result_1=}')


hand_type_ranks_2 = []
for hand, score in data.items():
    max_type_rank = 1
    for replace_card, rank in card_ranks_2.items():
        hand_mod = hand.replace('J', replace_card)
        counter = collections.Counter(hand_mod)
        type_rank = type_ranks[tuple(sorted(counter.values()))]
        max_type_rank = max(max_type_rank, type_rank)
    hand_type_ranks_2.append((hand, max_type_rank))

hand_type_ranks_2.sort(key=lambda x: (x[1], card_ranks_2[x[0][0]], card_ranks_2[x[0][1]], card_ranks_2[x[0][2]],
                                      card_ranks_2[x[0][3]], card_ranks_2[x[0][4]]))

result_2 = 0
for i, (hand, _) in enumerate(hand_type_ranks_2, start=1):
    result_2 += i * data[hand]

print(f'{result_2=}')
