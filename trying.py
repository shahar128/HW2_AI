import itertools
from itertools import product
import json
import copy
import utils
# from collections import namedtuple
# state = namedtuple('state', ['numtaxis','numpass', 'numgas','whattodo'])
# s1 = state(1,1,{'x': 1},'move taxi 1 (0,1)')
#
# x = hash(s1[0:3])
#
# print(x)
# diction = {x : s1}
# print(diction)
# print(diction[x].whattodo)

# initial =     {
#         "optimal": True,
#         "map": [['P', 'P', 'P'],
#                 ['P', 'G', 'P'],
#                 ['P', 'P', 'P']],
#         "taxis": {'taxi 1': {"location": (0, 0), "fuel": 10, "capacity": 1}},
#         "passengers": {'Dana': {"location": (2, 2), "destination": (0, 0),
#                                 "possible_goals": ((0, 0), (2, 2)), "prob_change_goal": 0.1}},
#         "turns to go": 100
#     }
# diction = {}
# taxis_names = initial['taxis'].keys()
# taxis_gas = {}
# taxis_location = {}
# pass_names = initial['passengers'].keys()
# pass_all_data = initial['passengers']
# pass_dest = {}
# map = initial['map']
# len_row = len(map)
# len_col = len(map[0])
# possible = set()
# for i in range(len_row):
#     for j in range(len_col):
#         if map[i][j] == 'P' or map[i][j] == 'G':
#             possible.add((i, j))
# cum_gas = 1
# for taxi in taxis_names:
#     gas = initial['taxis'][taxi]['fuel']
#     taxis_gas[taxi] = gas
#     cum_gas *= (gas + 1)
#     taxis_location[taxi] = initial['taxis'][taxi]['location']
# cum_dest = 1
# for passenger in pass_names:
#     num_dest = len(initial['passengers'][passenger]["possible_goals"])
#     cum_dest *= num_dest
#
# print((cum_dest + len(taxis_names)) * len(possible) * cum_gas)
#
#
# x = {'1': 1, '2': 2}
# print(x)
# x.pop('1')
# print(x)

# x = {"taxi 1": [0,1,2,3], "taxi 2": [0,1,2,3,4], "taxi 3": [7,8]}
# from itertools import product
# def my_product(inp):
#     return (list(zip(inp.keys(), values)) for values in product(*inp.values()))
# # print(list(my_product(x)))
#
#
# dana_loc = [(0,1), (0,0),"taxi1","taxi2"]
# dana_dest = [(3,3),(5,5)]
#
# ofer_loc = [(1,1), (0,0)]
# ofer_dest = [(13,3),(25,5)]
# z = []
#
# for loc in dana_loc:
#     for dest in dana_dest:
#         temp = {"loc": loc, "dest": dest,}
#         z.append(temp)
# print(z)
# f = {"dana": z, "ofer": z}
# print("000")
# # y = {"dana": [{"loc": "taxi 1", "dest": (0,1)}, {"loc": (1,2), "dest": (0,1)}], "ofer": ["taxi 1", "taxi 2", None] }
# print(list(my_product(f)))
# import json
#
# x = -8366790848761051619
# y = {'taxis': {'taxi 1': {'location': (0, 1), 'fuel': 0}, 'taxi 2': {'location': (2, 0), 'fuel': 0}}, 'passengers': {'Dana': {'location': 'taxi 2', 'destination': (2, 2), 'possible_goals': ((2, 2),), 'prob_change_goal': 0.1}, 'Dan': {'location': 'taxi 2', 'destination': (2, 2), 'possible_goals': ((2, 2),), 'prob_change_goal': 0.1}}}
# print(hash(json.dumps(y)))
# def possible_moves(loc, lenrow, lencol):
#     # returns possible moves given locations and map size
#     lenrow -= 1
#     lencol -= 1
#     i = loc[0]
#     j = loc[1]
#     if i != 0 and i != lenrow and j != 0 and j != lencol:
#         return [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
#     if i == 0:
#         if j == 0:
#             return [(0, 1), (1, 0)]
#         elif j == lencol:
#             return [(1, j), (0, j - 1)]
#         else:
#             return [(0, j + 1), (0, j - 1), (1, j)]
#     elif i == lenrow:
#         if j == 0:
#             return [(i - 1, 0), (i, 1)]
#         elif j == lencol:
#             return [(i - 1, j), (i, j - 1)]
#         else:
#             return [(i, j + 1), (i, j - 1), (i - 1, j)]
#     if j == 0:
#         return [(i - 1, j), (i, 1), (i + 1, j)]
#     elif j == lencol:
#         return [(i - 1, j), (i, j - 1), (i + 1, j)]


# def possible_moves(location, matrix_size):
#     # Unpack the location tuple
#     row, col = location
#
#     # Initialize a list of possible moves
#     moves = []
#
#     # Check if we can move up
#     if row > 0:
#         moves.append((row - 1, col))
#
#     # Check if we can move down
#     if row < matrix_size[0] - 1:
#         moves.append((row + 1, col))
#
#     # Check if we can move left
#     if col > 0:
#         moves.append((row, col - 1))
#
#     # Check if we can move right
#     if col < matrix_size[1] - 1:
#         moves.append((row, col + 1))
#
#     # Return the list of possible moves
#     return moves
#
#
# x = [['P', 'P', 'G', 'P', 'P'], ]
# print(possible_moves((1,1), (5,5)))
from itertools import product
def my_product(inp):
    return (list(zip(inp.keys(), values)) for values in product(*inp.values()))

def possible_moves(location, matrix_size):
    # Unpack the location tuple
    row, col = location

    # Initialize a list of possible moves
    moves = []

    # Check if we can move up
    if row > 0:
        moves.append((row - 1, col))

    # Check if we can move down
    if row < matrix_size[0] - 1:
        moves.append((row + 1, col))

    # Check if we can move left
    if col > 0:
        moves.append((row, col - 1))

    # Check if we can move right
    if col < matrix_size[1] - 1:
        moves.append((row, col + 1))

    # Return the list of possible moves
    return moves

def calculateDests(initial):
    dests = {}
    for passenger in initial["passengers"].keys():
        dests[passenger] = list(initial["passengers"][passenger]['possible_goals'])
    dests_combined = list(my_product(dests))

    return dests_combined

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
        moves = possible_moves(t_location, (lenrow, lencol))
        for move in moves:
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


initial =      {
        'optimal': True,
        "turns to go": 100,
        'map': [['P', 'P', 'P', 'I', 'P', 'P', 'P'],
                ['P', 'I', 'P', 'P', 'P', 'P', 'I'],
                ['P', 'P', 'I', 'P', 'P', 'I', 'P'],
                ['P', 'G', 'P', 'I', 'P', 'G', 'P'],
                ['P', 'P', 'P', 'P', 'P', 'I', 'P'],
                ['P', 'P', 'G', 'I', 'P', 'P', 'P']],
        'taxis': {'taxi 1': {'location': (5, 6), 'fuel': 21, 'capacity': 3}},
        'passengers': {'Omer': {'location': (1, 5), 'destination': (2, 2),
                                'possible_goals': ((2, 2), (4, 3)), 'prob_change_goal': 0.2},
                       'Roee': {'location': (2, 1), 'destination': (4, 3),
                                'possible_goals': ((4, 3), (2, 2)), 'prob_change_goal': 0.5},
                       'Dana': {'location': (4, 2), 'destination': (5, 2),
                                'possible_goals': ((4, 3), (2, 2), (5, 2)), 'prob_change_goal': 0.2},
                       'Efrat': {'location': (5, 6), 'destination': (2, 3),
                                 'possible_goals': ((2, 3), (2, 2), (4, 3)), 'prob_change_goal': 0.3}},
    }
# print(calculateDests(x))
#
# def stochStates(state, dests):
#     stoch_states = {}
#     for dest in dests:
#         new_state = copy.deepcopy(state)
#         prob = 1
#         for item in dest:
#             pass_name = item[0]
#             pass_dest = item[1]
#             curr_dest = state["passengers"][pass_name]["destination"]
#             prob_change = state["passengers"][pass_name]["prob_change_goal"]
#             if pass_dest == curr_dest:
#                 prob *= (1 - prob_change) + (
#                         prob_change / len(state["passengers"][pass_name]["possible_goals"]))
#             else:
#                 new_state["passengers"][pass_name]["destination"] = pass_dest
#                 prob *= (prob_change / len(state["passengers"][pass_name]["possible_goals"]))
#         prob = round(prob, 6)
#         hash_val = hash(json.dumps(new_state))
#         stoch_states[hash_val] = {"state": new_state, "probability": prob, "action": None, "value": 0}
#     return stoch_states
#
# def calculate_h(state, action):
#     return 1
#
# def ChooseAction(root_state, i, action=None):
#     if i == 0:
#         value = calculate_h(root_state, action)
#         root_state["value"] = value
#         return
#     action = actions(root_state, initial)
#     dests = calculateDests(initial)
#     for act in action:
#         res = result(initial, root_state, act)
#         stoch_states =stochStates(res, dests)
#         val = 0
#         for hash_val in stoch_states.keys():
#             ChooseAction(stoch_states[hash_val], i - 1, act)
#             prob = stoch_states[hash_val]["probability"]
#             value = stoch_states[hash_val]["value"]
#             val += value * prob
#         if val > root_state["value"]:
#             root_state["value"] = val
#             root_state["action"] = act
# from utils import FIFOQueue
# new_initial = copy.deepcopy(initial)
# del new_initial["optimal"]
# del new_initial["map"]
# del new_initial["turns to go"]
# new_initial = {"state": new_initial, "probability": None, "action": None, "value": 0}
# Queue = FIFOQueue()
# states_dict = {}
# Queue.append(new_initial)
# while len(Queue) != 0:
#     node = Queue.pop()
#     hashed_val = hash(json.dumps(node["state"]))
#     if hashed_val not in states_dict.keys():
#         ChooseAction(node, 2)
#         hash_val = hash(json.dumps(node["state"]))
#         states_dict[hash_val] = node
#         print(len(states_dict.keys()))
#         act = node["action"]
#         res = result(initial, node, act)
#         dests = calculateDests(initial)
#         stoch_states = stochStates(res, dests)
#         for hash_val in stoch_states.keys():
#             Queue.append(stoch_states[hash_val])
# print(len(states_dict.keys()))
map1 = [['P', 'P', 'P', 'I', 'P', 'P', 'P'],
                ['P', 'I', 'P', 'P', 'P', 'P', 'I'],
                ['P', 'P', 'I', 'P', 'P', 'I', 'P'],
                ['P', 'G', 'P', 'I', 'P', 'G', 'P'],
                ['P', 'P', 'P', 'P', 'P', 'I', 'P'],
                ['P', 'P', 'G', 'I', 'P', 'P', 'P']]
gas_stations = []
for i in range(len(map1)):
    for j in range(len(map1[0])):
        if map1[i][j] == 'G':
            gas_stations.append((i, j))
print(gas_stations)