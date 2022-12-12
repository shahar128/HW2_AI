import itertools
from itertools import product
import json
import copy

def my_product(inp):
    return (list(zip(inp.keys(), values)) for values in product(*inp.values()))

def possible_moves(loc, lenrow, lencol):
    # returns possible moves given locations and map size
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
            print(move)
            tile_type = initial["map"][move[0]][move[1]]
            if tile_type != 'I' and state["state"]["taxis"][key]['fuel'] > 0:
                to_add = ('move', key, move)
                actions_dict[key].append(to_add)

        ## pickup and drop off
        #ofer changed
        taxi_capacity = state["state"]['taxis'][key]['capacity']
        # taxi_curr_capacity = state["state"]['taxis'][key]['currCap']
        taxi_list = list(state["state"]["taxis"].keys())

        for person in state["state"]["passengers"].keys():
            person_location = state["state"]["passengers"][person]["location"]
            person_dest = state["state"]["passengers"][person]["destination"]
            # person_on_taxi = state["passengers"][person]["onTaxi"]
            ##ofer changed
            if person_location == t_location and person_location not in taxi_list and taxi_capacity >0 and person_dest != person_location :
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
    reset = ("reset",)
    # terminate = ('terminate',)
    for key in actions_dict.keys():
        combined_actions.append(actions_dict[key])
    if len(actions_dict.keys()) == 1:
        name_taxi = list(actions_dict.keys())[0]
        actions_dict[name_taxi].append(reset)
        # actions_dict[name_taxi].append(terminate)
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


        # final_prod_actions.append(terminate)
        final_prod_actions.append(reset)
        return tuple(final_prod_actions)


def result(initial, state, action):
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
            #oferchanged
            new_state["state"]["taxis"][taxi_name]["capacity"] -= 1
            new_state["state"]["passengers"][passenger]["location"] = taxi_name

        elif verb == 'drop off':
            taxi_name = act[1]
            passenger = act[2]
            new_state["state"]["taxis"][taxi_name]["capacity"] += 1
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
            del new_initial["turns to go"]
            # for taxi in new_initial["taxis"].keys():
            #     new_initial["taxis"][taxi]["currCap"] = 0
            return new_initial
    return new_state["state"]


def turn_to_stoch(state, dests):
    stoch_states = {}
    for dest in dests:
        new_state = copy.deepcopy(state)
        prob = 1
        for item in dest:
            pass_name = item[0]
            pass_dest = item[1]
            curr_dest = state["passengers"][pass_name]["destination"]
            prob_change = state["passengers"][pass_name]["prob_change_goal"]
            if pass_dest == curr_dest:
                prob *= (1 - prob_change) + (
                            prob_change / len(state["passengers"][pass_name]["possible_goals"]))
            else:
                new_state["passengers"][pass_name]["destination"] = pass_dest
                prob *= (prob_change / len(state["passengers"][pass_name]["possible_goals"]))
        prob = round(prob, 6)
        hash_val = hash(json.dumps(new_state))
        # if hash_val == 649863192296947903:
        #     print(new_state["state"])
        # print(new_state["state"])
        stoch_states[hash_val] = prob
    return stoch_states

# def policy_iteration()

def value_iteration(states_dict, initial, dests_combined):
    ##initialize
    for hash_state in states_dict.keys():
        # state = states_dict[hash_state]
        # actions_tup = actions(state, initial)
        # max_val = float('-inf')
        # for act in actions_tup:
        #     if act == "reset":
        #         max_val = max(max_val, -50)
        #     elif act == "terminate":
        #         max_val = max(max_val, 0)
        #     else:
        #         temp_val = 0
        #         num_taxis = len(initial["taxis"].keys())
        #         if num_taxis > 1:
        #             for taxi_act in act:
        #                 if taxi_act[0] == "refuel":
        #                     temp_val -= 10
        #                 elif taxi_act[0] == 'drop off':
        #                     temp_val += 100
        #             max_val = max(max_val, temp_val)
        #         else:
        #             if act[0] == "refuel":
        #                 temp_val -= 10
        #             elif act[0] == 'drop off':
        #                 #to add the act
        #                 temp_val += 100
        #             max_val = max(max_val, temp_val)

        states_dict[hash_state]["reward"] = 0
        states_dict[hash_state]["value"] = 0


    # rounds
    max_iter = 100  # Maximum number of iterations
    epsilon = 0.01 # Error tolerance

    for i in range(max_iter):
        for hash_value in states_dict.keys():
            state = states_dict[hash_value]
            actions_tup = actions(state, initial)
            max_val = float('-inf')
            reward = 0
            if len(initial["taxis"].keys()) == 1:
                for act in actions_tup:
                    sigma = 0
                    res = result(initial, state, act)
                    stoch_res = turn_to_stoch(res, dests_combined)
                    for s_res in stoch_res:
                        V = states_dict[s_res]["value"]
                        P = stoch_res[s_res]
                        sigma += V*P
                    reward = 0
                    if act == "reset":
                        reward -= 50
                    elif act == "terminate":
                        reward -= 10000
                    elif act[0] == "refuel":
                        reward -= 10
                    elif act[0] == "drop off":
                        reward += 100
                    elif act[0] == "wait":
                        reward -= 100
                    if sigma + reward >= max_val:
                        states_dict[hash_value]["action"] = act
                        states_dict[hash_value]["value"] = sigma + reward
                    max_val = max(max_val, sigma + reward)
            else:
                for act in actions_tup:
                    sigma = 0
                    res = result(initial, state, act)
                    stoch_res = turn_to_stoch(res, dests_combined)
                    reward = 0
                    for s_res in stoch_res:
                        V = states_dict[s_res]["value"]
                        P = stoch_res[s_res]
                        sigma += V*P
                    for taxi_act in act:
                        if act == "reset":
                            reward -= 50
                        elif act == "terminate":
                            reward -= 10000
                        elif act[0] == "refuel":
                            reward -= 10
                        elif act[0] == "drop off":
                            reward += 100
                        elif act[0] == "wait":
                            reward -= 100
                    if sigma + reward >= max_val:
                        states_dict[hash_value]["action"] = act
                        states_dict[hash_value]["value"] = sigma + reward
                    max_val = max(max_val, sigma + reward)

    return states_dict

ids = ["avukadoareyoubashel", "weloveofer"]


class OptimalTaxiAgent:
    def __init__(self, initial):
        self.initial = initial
        self.states_dict = {}

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
        to_remove = []
        count = 0
        for taxi in initial["taxis"].keys():
            for passengers in passengers_combined:
                count = 0
                for item in passengers:
                    if item[1]["loc"] == taxi:
                        count += 1
                if count > initial["taxis"][taxi]["capacity"]:
                    to_remove.append(passengers)

        for item in to_remove:
            passengers_combined.remove(item)
        # print(passengers_combined)
        for taxi_state in taxi_combined:
            for pass_state in passengers_combined:
                taxis_dict = {}
                for taxis_loc in taxi_state[0]:
                    taxi_name = taxis_loc[0]
                    taxi_loc = taxis_loc[1]
                    ### ofer changed
                    capacity = initial["taxis"][taxi_name]["capacity"]
                    taxis_dict[taxi_name] = {"location": taxi_loc, "fuel": 0, "capacity": capacity}
                for taxis_fuel in taxi_state[1]:
                    taxi_name = taxis_fuel[0]
                    taxi_fuel = taxis_fuel[1]
                    taxis_dict[taxi_name]["fuel"] = taxi_fuel
                passengers_dict = {}
                for item in pass_state:
                    pass_name = item[0]
                    pass_loc = item[1]['loc']
                    ###
                    if type(pass_loc) == str:
                        taxis_dict[pass_loc]["capacity"] -= 1
                    pass_dest = item[1]['dest']
                    pass_goals = initial["passengers"][pass_name]["possible_goals"]
                    pass_change = initial["passengers"][pass_name]["prob_change_goal"]
                    passengers_dict[pass_name] = {"location": pass_loc, "destination": pass_dest,
                                                  "possible_goals": pass_goals, "prob_change_goal": pass_change}

                temp_state = {"taxis": taxis_dict, "passengers": passengers_dict}
                hash_val = hash(json.dumps(temp_state))
                self.states_dict[hash_val] = {"state": temp_state, "action": None, "value": 0, "reward": 0}
        # print(self.states_dict)
        self.states_dict = value_iteration(self.states_dict, self.initial, dests_combined)


    def act(self, state):
        new_state = copy.deepcopy(state)
        del new_state["optimal"]
        del new_state["map"]
        del new_state["turns to go"]
        # for taxi in new_state["taxis"].keys():
        #     new_state["taxis"][taxi]["currCap"] = 0
        #     for passenger in new_state["passengers"].keys():
        #         #########not good
        #         if new_state["passengers"][passenger]["location"] == taxi:
        #             new_state["taxis"][taxi]["currCap"] += 1

        hash_val = hash(json.dumps((new_state)))
        action = self.states_dict[hash_val]["action"]
        print(state)
        if len(state["taxis"].keys()) == 1:
            if action == ('reset',):
                print((action))
                return 'reset'
            elif action == ('terminate',):
                return 'terminate'
            else:
                # print(state)
                print(action)
                # print(state)
                return ((action,))
        print(action)
        # print(state)
        return action



class TaxiAgent:
    def __init__(self, initial):
        self.initial = initial

    def act(self, state):
        raise NotImplemented
