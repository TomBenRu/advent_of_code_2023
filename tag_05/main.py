import itertools
import pprint

with open('input.txt') as f:
    data = f.read().strip().split('\n\n')

seed_to_soil_map = [[int(n) for n in r.split()] for r in data[1].split(':')[1].strip().split('\n')]
soil_to_fertilizer_map = [[int(n) for n in r.split()] for r in data[2].split(':')[1].strip().split('\n')]
fertilizer_to_water_map = [[int(n) for n in r.split()] for r in data[3].split(':')[1].strip().split('\n')]
water_to_light_map = [[int(n) for n in r.split()] for r in data[4].split(':')[1].strip().split('\n')]
light_to_temperature_map = [[int(n) for n in r.split()] for r in data[5].split(':')[1].strip().split('\n')]
temperature_to_humidity_map = [[int(n) for n in r.split()] for r in data[6].split(':')[1].strip().split('\n')]
humidity_to_location_map = [[int(n) for n in r.split()] for r in data[7].split(':')[1].strip().split('\n')]

seeds = [int(s) for s in data[0].split(':')[1].split()]

# part 1
min_location = float('inf')
for i, seed in enumerate(seeds):
    soil = seed
    for assignment in seed_to_soil_map:
        if assignment[1] <= seed < assignment[1] + assignment[2]:
            soil = seed - assignment[1] + assignment[0]
            break
    fertilizer = soil
    for assignment in soil_to_fertilizer_map:
        if assignment[1] <= soil < assignment[1] + assignment[2]:
            fertilizer = soil - assignment[1] + assignment[0]
            break
    water = fertilizer
    for assignment in fertilizer_to_water_map:
        if assignment[1] <= fertilizer < assignment[1] + assignment[2]:
            water = fertilizer - assignment[1] + assignment[0]
            break
    light = water
    for assignment in water_to_light_map:
        if assignment[1] <= water < assignment[1] + assignment[2]:
            light = water - assignment[1] + assignment[0]
            break
    temperature = light
    for assignment in light_to_temperature_map:
        if assignment[1] <= light < assignment[1] + assignment[2]:
            temperature = light - assignment[1] + assignment[0]
            break
    humidity = temperature
    for assignment in temperature_to_humidity_map:
        if assignment[1] <= temperature < assignment[1] + assignment[2]:
            humidity = temperature - assignment[1] + assignment[0]
            break
    location = humidity
    for assignment in humidity_to_location_map:
        if assignment[1] <= humidity < assignment[1] + assignment[2]:
            location = humidity - assignment[1] + assignment[0]
            break
    if location < min_location:
        min_location = location

print(f'{min_location=}')


# part 2

def overlap_ranges(range_1: tuple[int, int], range_2: tuple[int, int]):
    start = max(range_1[0], range_2[0])
    end = min(range_1[0]+range_1[1]-1, range_2[0]+range_2[1]-1)
    new_range_1 = None
    not_assigned_ranges = []
    if start <= end:
        new_range_1 = (start, end-start+1)
        if range_1[0] < start:
            not_assigned_ranges.append((range_1[0], start-range_1[0]))
        if range_1[0] + range_1[1] - 1 > end:
            not_assigned_ranges.append((end+1, range_1[0]+range_1[1]-end))
    else:
        not_assigned_ranges.append(range_1)
    return new_range_1, not_assigned_ranges


seeds_rearranged: list[tuple[int, int]] = []
not_assigned_ranges = []
for seed_start, seed_range in ((s, seeds[i+1]) for i, s in enumerate(seeds) if not i % 2):
    seeds_rearranged.append((seed_start, seed_range))


def calculate_next_arrangement(rearranged: list[tuple[int, int]],
                               assignment_map: list[list[int]]) -> list[tuple[int, int]]:
    for i, (element_start, element_range) in enumerate(rearranged):
        for assignment in assignment_map:
            new_element_range, not_assigned = overlap_ranges((element_start, element_range),
                                                          (assignment[1], assignment[2]))
            if new_element_range:
                if not_assigned:
                    rearranged[i] = new_element_range
                    rearranged += not_assigned

    next_rearranged = []
    for element_range in rearranged:
        for assignment in assignment_map:
            if assignment[1] <= element_range[0] < assignment[1] + assignment[2]:
                next_rearranged.append((element_range[0]-assignment[1] + assignment[0], element_range[1]))
                break
        else:
            next_rearranged.append(element_range)
    return next_rearranged


soil_rearranged = calculate_next_arrangement(seeds_rearranged, seed_to_soil_map)
fertilizer_rearranged = calculate_next_arrangement(soil_rearranged, soil_to_fertilizer_map)
water_rearranged = calculate_next_arrangement(fertilizer_rearranged, fertilizer_to_water_map)
light_rearranged = calculate_next_arrangement(water_rearranged, water_to_light_map)
temperature_rearranged = calculate_next_arrangement(light_rearranged, light_to_temperature_map)
humidity_rearranged = calculate_next_arrangement(temperature_rearranged, temperature_to_humidity_map)
location_rearranged = calculate_next_arrangement(humidity_rearranged, humidity_to_location_map)

print(f'{min(r[0] for r in location_rearranged)=}')




