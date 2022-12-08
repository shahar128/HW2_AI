import itertools
from itertools import product
import json
import copy



def my_product(inp):
    return (list(zip(inp.keys(), values)) for values in product(*inp.values()))


def possible_moves(loc, lenrow, lencol):
    #returns possible moves given locations and map size
    lenrow -= 1
    lencol -= 1
    i = loc[0]
    j = loc[1]
    if i != 0 and i != lenrow and j != 0 and j != lencol:
        return [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    if i == 0:
        if j == 0:
            return [(0, 1), (1, 0)]
        elif j == lencol:
            return [(1, j), (0, j - 1)]
        else:
            return [(0, j + 1), (0, j - 1), (1, j)]
    elif i == lenrow:
        if j == 0:
            return [(i - 1, 0), (i, 1)]
        elif j == lencol:
            return [(i - 1, j), (i, j - 1)]
        else:
            return [(i, j + 1), (i, j - 1), (i - 1, j)]

    if j == 0:
        return [(i - 1, j), (i, 1), (i + 1, j)]
    elif j == lencol:
        return [(i - 1, j), (i, j - 1), (i + 1, j)]

def actions(state, initial):
    """Returns all the actions that can be executed in the given
    state. The result should be a tuple (or other iterable) of actions
    as defined in the problem description file"""
    # state = json.loads(state)
    actions_dict = {}
    lenrow, lencol = len(initial["map"]), len(initial["map"][0])
    for key in state["state"]["taxis"].keys():
        actions_dict[key] = []
        ## possible moves
        t_location = state["state"]["taxis"][key]["location"]
        moves = possible_moves(t_location, lenrow, lencol)
        for move in moves:
            tile_type = initial["map"][move[0]][move[1]]
            if tile_type != 'I' and state["state"]["taxis"][key]['fuel'] > 0:
                to_add = ('move', key, move)
                actions_dict[key].append(to_add)

        ## pickup and drop off
        taxi_list = list(state["state"]["taxis"].keys())

        for person in state["state"]["passengers"].keys():
            person_location = state["state"]["passengers"][person]["location"]
            person_dest = state["state"]["passengers"][person]["destination"]
            # person_on_taxi = state["passengers"][person]["onTaxi"]
            if person_location == t_location and person_location not in taxi_list:
                to_add = ('pick up', key, person)
                actions_dict[key].append(to_add)
            if person_location == key and person_dest == t_location:
                to_add = ('drop off', key, person)
                actions_dict[key].append(to_add)

        ## refuel
        curr_tile_type = initial["map"][t_location[0]][t_location[1]]
        if curr_tile_type == 'G':
            to_add = ("refuel", key)
            actions_dict[key].append(to_add)

        ## wait
        to_add = ("wait", key)
        actions_dict[key].append(to_add)

    combined_actions = []
    for key in actions_dict.keys():
        combined_actions.append(actions_dict[key])
    if len(actions_dict.keys()) == 1:
        name_taxi = list(actions_dict.keys())[0]
        return tuple(actions_dict[name_taxi])

    else:
        prod_actions = list(itertools.product(*combined_actions))
        final_prod_actions = []
        num_taxis = len(state["state"]["taxis"].keys())
        for i in range(len(prod_actions)):
            loc_set = set()
            for j in range(num_taxis):
                verb = prod_actions[i][j][0]
                if verb == "move":
                    loc_set.add(tuple(prod_actions[i][j][2]))
                else:
                    taxi_name = prod_actions[i][j][1]
                    taxi_loc = state["state"]["taxis"][taxi_name]["location"]
                    loc_set.add(tuple(taxi_loc))
            if len(loc_set) == num_taxis:
                final_prod_actions.append(prod_actions[i])
        reset = ("reset",)
        terminate = ('terminate',)

        final_prod_actions.append(terminate)
        final_prod_actions.append(reset)
        return tuple(final_prod_actions)

def result(initial,state, action):
    """Return the states and possibilities that results from executing the given
    action in the given state."""
    # state = json.loads(state)
    num_taxis = len(state["state"]["taxis"].keys())
    if num_taxis == 1:
        action = [list(action)]
    else:
        action = list(action)  # []
    new_state = copy.deepcopy(state)

    for act in action:
        verb = act[0]
        if verb == "move":
            taxi_name = act[1]
            dest = act[2]
            new_state["state"]["taxis"][taxi_name]["location"] = dest
            new_state["state"]["taxis"][taxi_name]["fuel"] -= 1

        elif verb == 'pick up':
            taxi_name = act[1]
            passenger = act[2]
            new_state["state"]["passengers"][passenger]["location"] = taxi_name

        elif verb == 'drop off':
            taxi_name = act[1]
            passenger = act[2]
            new_state["state"]["passengers"][passenger]["location"] = new_state["state"]["taxis"][taxi_name]["location"]

        elif verb == 'refuel':
            taxi_name = act[1]
            new_state["state"]["taxis"][taxi_name]["fuel"] = initial["taxis"][taxi_name]["fuel"]

        elif verb == 'terminate':
            pass
        elif verb == 'reset':
            new_initial = copy.deepcopy(initial)
            del new_initial["optimal"]
            del new_initial["map"]
            for taxi in new_initial["taxis"].keys():
                del new_initial["taxis"][taxi]["capacity"]
                return new_initial
    return new_state

def turn_to_stoch(state, dests):
    stoch_states = {}
    for dest in dests:
        new_state = copy.deepcopy(state)
        prob = 1
        for item in dest:
            pass_name = item[0]
            pass_dest = item[1]
            curr_dest = state["state"]["passengers"][pass_name]["destination"]
            prob_change = state["state"]["passengers"][pass_name]["prob_change_goal"]
            if pass_dest == curr_dest:
                prob *= (1 - prob_change) + (prob_change/len(state["state"]["passengers"][pass_name]["possible_goals"]))
            else:
                new_state["state"]["passengers"][pass_name]["destination"] = pass_dest
                prob *= (prob_change/len(state["state"]["passengers"][pass_name]["possible_goals"]))
        prob = round(prob,6)
        hash_val = hash(json.dumps(new_state["state"]))
        stoch_states[hash_val] = prob
    return stoch_states

ids = ["111111111", "222222222"]


class OptimalTaxiAgent:
    def __init__(self, initial):
        self.initial = initial

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

        taxi_combined = list(itertools.product(taxis_locations, fuel_product))

        loc_dest_dict = {}
        dests = {}
        for passenger in initial["passengers"].keys():
            loc_list = list(pass_position[passenger]['possible_locations'])
            taxis_list = list(initial["taxis"].keys())
            loc_list.extend(taxis_list)
            dest_list = list(pass_position[passenger]['possible_dest'])
            temp_list = []
            dests[passenger] = list(initial["passengers"][passenger]['possible_goals'])
            for loc in loc_list:
                for dest in dest_list:
                    temp = {"loc": loc, "dest": dest, }
                    temp_list.append(temp)
            loc_dest_dict[passenger] = temp_list
        passengers_combined = list(my_product(loc_dest_dict))
        dests_combined = list(my_product(dests))
        print(dests_combined)

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

        for item in to_remove:
            passengers_combined.remove(item)

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
                    passengers_dict[pass_name] = {"location": pass_loc, "destination": pass_dest,
                                                  "possible_goals": pass_goals, "prob_change_goal": pass_change}
                temp_state = {"taxis": taxis_dict, "passengers": passengers_dict}
                hash_val = hash(json.dumps(temp_state))
                states_dict[hash_val] = {"state": temp_state, "action": None, "value": 0}
        print(states_dict)



    def act(self, state):
        return 0


class TaxiAgent:
    def __init__(self, initial):
        self.initial = initial

    def act(self, state):
        raise NotImplemented
