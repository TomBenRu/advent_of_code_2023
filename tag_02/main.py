import pprint

with open('input.txt') as f:
    data = f.read().strip().splitlines()

data_parsed = {}
for line in data:
    game, grabs = line.split(':')
    grabs: str
    game_nr = int(game.strip().split()[1])
    grab_dicts = [{c.strip().split()[1].strip(): int(c.strip().split()[0]) for c in grab.strip().split(',')}
                  for grab in grabs.split(';')]
    data_parsed[game_nr] = grab_dicts

pprint.pprint(data_parsed)

"""The Elf would first like to know which games would have been possible if the bag contained only 
12 red cubes, 13 green cubes, and 14 blue cubes?"""

contend_bag = {'red': 12, 'green': 13, 'blue': 14}

# Game 1
sum_possible_ids = 0

# Game 2
sum_power_max_set = 0

for game_num, grabs in data_parsed.items():
    red, green, blue = 0, 0, 0
    for grab in grabs:
        red = max(grab.get('red', 0), red)
        green = max(grab.get('green', 0), green)
        blue = max(grab.get('blue', 0), blue)
    if red <= contend_bag['red'] and green <= contend_bag['green'] and blue <= contend_bag['blue']:
        sum_possible_ids += game_num
    sum_power_max_set += red * green * blue


print(f'{sum_possible_ids=}')
print(f'{sum_power_max_set=}')


