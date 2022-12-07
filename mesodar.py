import itertools
from itertools import product
import json


def my_product(inp):
    return (list(zip(inp.keys(), values)) for values in product(*inp.values()))


initial =  {
        "optimal": False,
        "map": [['P', 'P', 'G'],
                ['P', 'P', 'P'],
                ['G', 'P', 'P']],
        "taxis": {'taxi 1': {"location": (0, 0), "fuel": 3, "capacity": 1},
                  'taxi 2': {"location": (0, 0), "fuel": 3, "capacity": 1}},
        "passengers": {'Dana': {"location": (0, 2), "destination": (2, 2),
                                "possible_goals": ((2, 2),), "prob_change_goal": 0.1},
                       'Dan': {"location": (2, 0), "destination": (2, 2),
                               "possible_goals": ((2, 2),), "prob_change_goal": 0.1}
                       },
        "turns to go": 100
    }
# for 1 taxi and 1 passenger:

# 1. possible places for taxis

map = initial['map']
len_row = len(map)
len_col = len(map[0])
possible_tiles = set()
for i in range(len_row):
    for j in range(len_col):
        if map[i][j] == 'P' or map[i][j] == 'G':
            possible_tiles.add((i, j))


# 2. name of taxis and 3. fuel
taxis = {}
taxis_list = [None]
taxis_tiles = {}
for taxi in initial['taxis'].keys():
    fuel = initial['taxis'][taxi]['fuel']
    taxis[taxi] = list(range(fuel + 1))
    taxis_list.append(taxi)
    taxis_tiles[taxi] = possible_tiles

# passengers name and  4. dest list
pass_position = {}
pass_taxi = {}

for passenger in initial['passengers'].keys():
    location = initial['passengers'][passenger]["location"]
    set_location = set()
    set_location.add(location)
    possible_goals = initial['passengers'][passenger]["possible_goals"]
    for val in possible_goals:
        set_location.add(val)
    pass_position[passenger] = {'possible_locations': set_location, "possible_dest": possible_goals}
    pass_taxi[passenger] = taxis_list

# maybe

fuel_product = list(my_product(taxis))
# passengers_product = list(my_product(pass_taxi))
taxis_locations = list(my_product(taxis_tiles))
to_remove = []
for item in taxis_locations:
    tup_set = set()
    for tup in item:
        tup_set.add(tup[1])
    if len(tup_set) != len(item):
        to_remove.append(item)
for item in to_remove:
    taxis_locations.remove(item)

taxi_combined = list(itertools.product(taxis_locations,fuel_product))

loc_dest_dict = {}
for passenger in initial["passengers"].keys():
    loc_list = list(pass_position[passenger]['possible_locations'])
    taxis_list = list(initial["taxis"].keys())
    loc_list.extend(taxis_list)
    dest_list = list(pass_position[passenger]['possible_dest'])
    temp_list = []
    for loc in loc_list:
        for dest in dest_list:
            temp = {"loc": loc, "dest": dest, }
            temp_list.append(temp)
    loc_dest_dict[passenger] = temp_list

passengers_combined = list(my_product(loc_dest_dict))

to_remove = []
count = 0
for taxi in initial["taxis"].keys():
    print(taxi)
    for passengers in passengers_combined:
        count = 0
        for item in passengers:
            if item[1]["loc"] == taxi:
                count += 1
        if count > initial["taxis"][taxi]["capacity"]:
            to_remove.append(passengers)
print(to_remove)
for item in to_remove:
    passengers_combined.remove(item)
print(passengers_combined[0:10])




states_dict = {}
for taxi_state in taxi_combined:
    for pass_state in passengers_combined:
        taxis_dict = {}
        for taxis_loc in taxi_state[0]:
            taxi_name = taxis_loc[0]
            taxi_loc = taxis_loc[1]
            taxis_dict[taxi_name] = {"location": taxi_loc, "fuel": 0}
        for taxis_fuel in taxi_state[1]:
            taxi_name = taxis_fuel[0]
            taxi_fuel = taxis_fuel[1]
            taxis_dict[taxi_name]["fuel"] = taxi_fuel
        passengers_dict = {}
        for item in pass_state:
            pass_name = item[0]
            pass_loc = item[1]['loc']
            pass_dest = item[1]['dest']
            pass_goals = initial["passengers"][pass_name]["possible_goals"]
            pass_change = initial["passengers"][pass_name]["prob_change_goal"]
            passengers_dict[pass_name] = {"location": pass_loc,"destination": pass_dest,
                                          "possible_goals": pass_goals,"prob_change_goal": pass_change}
        temp_state = {"taxis": taxis_dict, "passengers": passengers_dict}
        hash_val = hash(json.dumps(temp_state))
        states_dict[hash_val] = {"state": temp_state, "action": None, "value": 0}

print(len(states_dict))