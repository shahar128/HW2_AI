import itertools
from itertools import product
import json
import copy
import utils
from collections import deque

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

def createRoutingTables(grid):
    # Initialize the graph with vertices for each tile in the grid
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] in ["G", "P"]:
                grid[i][j] = 1
            else:
                grid[i][j] = 0
    graph = {}
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 1:
                graph[(i, j)] = []

    # Add edges between adjacent tiles
    for vertex in graph:
        i, j = vertex
        if i > 0 and grid[i - 1][j] == 1:
            graph[vertex].append((i - 1, j))
        if i < len(grid) - 1 and grid[i + 1][j] == 1:
            graph[vertex].append((i + 1, j))
        if j > 0 and grid[i][j - 1] == 1:
            graph[vertex].append((i, j - 1))
        if j < len(grid[i]) - 1 and grid[i][j + 1] == 1:
            graph[vertex].append((i, j + 1))

    # Create the routing tables for all vertices
    routingTables = {}
    for source in graph:
        routingTables[source] = {}
        queue = deque([source])
        visited = set()
        # Set the distance to the source vertex to 0
        routingTables[source][source] = {"nextHop": source, "distance": 0}
        while queue:
            vertex = queue.popleft()
            visited.add(vertex)
            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    routingTables[source][neighbor] = {
                        "nextHop": vertex,
                        "distance": routingTables[source][vertex]["distance"] + 1
                    }
                    queue.append(neighbor)

    return routingTables



def man_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


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
        # ofer changed
        taxi_capacity = state["state"]['taxis'][key]['capacity']
        # taxi_curr_capacity = state["state"]['taxis'][key]['currCap']
        taxi_list = list(state["state"]["taxis"].keys())

        for person in state["state"]["passengers"].keys():
            person_location = state["state"]["passengers"][person]["location"]
            person_dest = state["state"]["passengers"][person]["destination"]
            # person_on_taxi = state["passengers"][person]["onTaxi"]
            ##ofer changed
            if person_location == t_location and person_location not in taxi_list and taxi_capacity > 0 and person_dest != person_location:
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
        if action == 0:
            action = "reset"
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
            # oferchanged
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
    turns = initial["turns to go"]
    ##initialize
    temp_dict = {}
    for i in range(turns + 1):
        temp_dict[i] = 0
    for hash_state in states_dict.keys():
        # states_dict[hash_state]["reward"] = 0
        states_dict[hash_state]["value"] = copy.deepcopy(temp_dict)

    # rounds

    for i in range(1, turns + 1):
        for hash_value in states_dict.keys():
            state = states_dict[hash_value]
            actions_tup = actions(state, initial)
            max_val = float('-inf')
            reward = 0
            if len(initial["taxis"].keys()) == 1:
                utilities = []
                for act in actions_tup:
                    sigma = 0
                    res = result(initial, state, act)
                    if act == "reset" or act == ("reset",):
                        hash_val1 = hash(json.dumps(res))
                        sigma = states_dict[hash_val1]["value"][i-1]
                    else:
                        stoch_res = turn_to_stoch(res, dests_combined)
                        for s_res in stoch_res:
                            V = states_dict[s_res]["value"][i-1]
                            P = stoch_res[s_res]
                            sigma += V * P
                    reward = 0
                    if act == "reset" or act == ("reset",):
                        reward -= 50
                    elif act == "terminate":
                        reward -= 10000
                    elif act[0] == "refuel":
                        reward -= 10
                    elif act[0] == "drop off":
                        reward += 100
                    utilities.append((sigma + reward, act))
                max_util = max(utilities, key=lambda tup: tup[0])
                    # if sigma + reward >= max_val:
                states_dict[hash_value]["action"][i] = max_util[1]
                states_dict[hash_value]["value"][i] = max_util[0]
                # if max_util[0]!= 0:
                #     print(max_util[0])

                    # max_val = max(max_val, sigma + reward)
            else:
                for act in actions_tup:
                    sigma = 0
                    res = result(initial, state, act)
                    stoch_res = turn_to_stoch(res, dests_combined)
                    reward = 0
                    for s_res in stoch_res:
                        V = states_dict[s_res]["value"]
                        P = stoch_res[s_res]
                        sigma += V * P
                    for taxi_act in act:
                        if taxi_act == "reset":
                            reward -= 50
                        elif taxi_act == "terminate":
                            reward -= 10000
                        elif taxi_act[0] == "refuel":
                            reward -= 10
                        elif taxi_act[0] == "drop off":
                            reward += 100
                        elif taxi_act[0] == "wait":
                            reward -= 100
                    if sigma + reward >= max_val:
                        states_dict[hash_value]["action"] = act
                        states_dict[hash_value]["value"] = sigma + reward
                    max_val = max(max_val, sigma + reward)
    # print(states_dict)

    return states_dict


ids = ["206968281", "318238839"]


class OptimalTaxiAgent:
    def __init__(self, initial):
        self.initial = initial
        self.states_dict = {}
        self.turns = self.initial["turns to go"]
        temp_dict = {}
        for i in range(self.turns + 1):
            temp_dict[i] = 0
        self.temp_dict = temp_dict

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

                self.states_dict[hash_val] = {"state": temp_state, "action": copy.deepcopy(self.temp_dict), "value": 0, "reward": 0}
        self.states_dict = value_iteration(self.states_dict, self.initial, dests_combined)
    #     x =     {
    #     "taxis": {'taxi 1': {"location": (0, 0), "fuel": 10, "capacity": 1}},
    #     "passengers": {'Dana': {"location": (2, 2), "destination": (0, 0),
    #                             "possible_goals": ((0, 0), (2, 2)), "prob_change_goal": 0.1}}
    # }
    #     xx = hash(json.dumps(x))
    #     print(self.states_dict[xx])

    def act(self, state):
        print(state)
        new_state = copy.deepcopy(state)
        del new_state["optimal"]
        del new_state["map"]
        turn_to_go = state["turns to go"]
        del new_state["turns to go"]
        # for taxi in new_state["taxis"].keys():
        #     new_state["taxis"][taxi]["currCap"] = 0
        #     for passenger in new_state["passengers"].keys():
        #         #########not good
        #         if new_state["passengers"][passenger]["location"] == taxi:
        #             new_state["taxis"][taxi]["currCap"] += 1

        hash_val = hash(json.dumps((new_state)))
        action = self.states_dict[hash_val]["action"][turn_to_go]
        print(action)
        if len(state["taxis"].keys()) == 1:
            if action == ('reset',):
                # print((action))
                return 'reset'
            elif action == ('terminate',):
                return 'terminate'
            else:
                # print(state)
                # print(action)
                # print(state)
                return ((action,))
        # print(action)
        # print(state)
        return action


class TaxiAgent:
    def __init__(self, initial):
        self.initial = initial
        passengers_list = list(self.initial["passengers"].keys())
        if len(passengers_list) > 2:
            priority_passengers = []
            for passenger in passengers_list:
                pass_prob = self.initial["passengers"][passenger]["prob_change_goal"]
                num_goals = len(self.initial["passengers"][passenger]["possible_goals"])
                priority_passengers.append((passenger, pass_prob, num_goals))
            sorted_elements = sorted(priority_passengers, key=lambda x: (x[1], x[2]), reverse=True)
            num_to_del = len(passengers_list) - 2
            for i in range(num_to_del):
                pass_name = sorted_elements[i][0]
                # del self.new_initial["passengers"][pass_name]
                del self.initial["passengers"][pass_name]
            print(self.initial)
        self.states_dict = {}
        self.Queue = utils.FIFOQueue()
        self.new_initial = copy.deepcopy(self.initial)
        self.map = self.initial["map"]
        self.taxis_list = list(self.initial["taxis"].keys())
        self.gas_stations = []
        self.depth = 2
        self.signal = False
        grid = copy.deepcopy(self.map)
        self.routing_table = createRoutingTables(grid)
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == 'G':
                    self.gas_stations.append((i, j))
        del self.new_initial["optimal"]
        del self.new_initial["map"]
        del self.new_initial["turns to go"]


        self.hash_val_initial = hash(json.dumps(self.new_initial))
        self.new_initial = {"state": self.new_initial, "probability": None, "action": None, "value": float("-inf")}
        self.Queue.append(self.new_initial)
        self.temp_init = self.new_initial
        while len(self.Queue) != 0:
            node = self.Queue.pop()
            hashed_val = hash(json.dumps(node["state"]))
            if hashed_val not in self.states_dict.keys():
                self.temp_init = node
                self.mdp(node, 2)
                hash_val = hash(json.dumps(node["state"]))
                self.states_dict[hash_val] = node
                act = node["action"]
                res = result(self.initial, node, act)
                dests = self.calculateDests(self.initial)
                stoch_states = self.stochStates(res, dests)
                for hash_val in stoch_states.keys():
                    self.Queue.append(stoch_states[hash_val])
        # print(self.states_dict)

    def stochStates(self, state, dests):
        # del state["optimal"]
        # del state["map"]
        # del state["turns to go"]
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
            stoch_states[hash_val] = {"state": new_state, "probability": prob, "action": 0, "value": float("-inf")}
        return stoch_states

    def calculateDests(self, initial):
        dests = {}
        for passenger in initial["passengers"].keys():
            dests[passenger] = list(initial["passengers"][passenger]['possible_goals'])
        dests_combined = list(my_product(dests))
        return dests_combined

    def heuristic(self, state):
        # points = 0
        #
        # # Consider the distance and gas remaining for each passenger-carrying taxi
        # for passenger in state["state"]["passengers"].keys():
        #     if state["state"]["passengers"][passenger]["location"] in self.taxis_list:
        #         pass_dest = state["state"]["passengers"][passenger]["destination"]
        #         taxi_name = state["state"]["passengers"][passenger]["location"]
        #         taxi_loc = state["state"]["taxis"][taxi_name]["location"]
        #         man_dist = man_distance(taxi_loc, pass_dest)
        #         gas_remaining = state["state"]["taxis"][taxi_name]["fuel"]
        #         if man_dist > gas_remaining:
        #             # Subtract a large value from the score if the taxi doesn't have enough gas to reach the destination
        #             points -= 1000
        #         else:
        #             if man_dist != 0:
        #                 points += (1 / man_dist) * 1000
        #             else:
        #                 points += 2000
        #
        # # Consider the distance to the nearest passenger for each empty taxi
        # for taxi in state["state"]["taxis"].keys():
        #     min_values = []
        #     for passenger in state["state"]["passengers"].keys():
        #         if state["state"]["passengers"][passenger]["location"] not in self.taxis_list:
        #             taxi_loc = state["state"]["taxis"][taxi]["location"]
        #             pass_loc = state["state"]["passengers"][passenger]["location"]
        #             man_dist = man_distance(taxi_loc, pass_loc)
        #             gas_remaining = state["state"]["taxis"][taxi]["fuel"]
        #             if man_dist > gas_remaining:
        #                 # Subtract a value from the score if the taxi doesn't have enough gas to reach the passenger
        #                 man_dist -= 100
        #             min_values.append(man_dist)
        #     if len(min_values) != 0:
        #         min_val = min(min_values)
        #         if min_val != 0:
        #             points += (1 / min_val) * 100
        #         else:
        #             points += 200
        return 1

    # def heuristic(self, state):
    #     # implement your heuristic function here
    #     # pass on taxi
    #     points = 0
    #     for passenger in state["state"]["passengers"].keys():
    #         if state["state"]["passengers"][passenger]["location"] in self.taxis_list:
    #             pass_dest = state["state"]["passengers"][passenger]["destination"]
    #             taxi_name = state["state"]["passengers"][passenger]["location"]
    #             taxi_loc = state["state"]["taxis"][taxi_name]["location"]
    #             man_dist = man_distance(taxi_loc, pass_dest)
    #             if man_dist != 0:
    #                 points += (1/man_dist)*1000
    #             else:
    #                 points += 2000
    #     # empty taxi
    #
    #     for taxi in state["state"]["taxis"].keys():
    #         min_values = []
    #         for passenger in state["state"]["passengers"].keys():
    #             if state["state"]["passengers"][passenger]["location"] not in self.taxis_list:
    #                 taxi_loc = state["state"]["taxis"][taxi]["location"]
    #                 pass_loc = state["state"]["passengers"][passenger]["location"]
    #                 man_dist = man_distance(taxi_loc, pass_loc)
    #                 min_values.append(man_dist)
    #         if len(min_values) != 0:
    #             min_val = min(min_values)
    #             if min_val != 0:
    #                 points += (1 / min_val) * 100
    #             else:
    #                 points += 200
    #     return points

    def empty_taxi(self, state, act):
        points = 0
        for taxi in state["state"]["taxis"].keys():
            min_values = []
            gas_remaining = state["state"]["taxis"][taxi]["fuel"]
            taxi_loc = state["state"]["taxis"][taxi]["location"]
            for passenger in state["state"]["passengers"].keys():
                pass_loc = state["state"]["passengers"][passenger]["location"]
                pass_dest = state["state"]["passengers"][passenger]["destination"]
                if pass_loc not in self.taxis_list and pass_dest != pass_loc:
                    distance = self.routing_table[taxi_loc][pass_loc]["distance"]
                    min_values.append((distance, pass_loc))
            if len(min_values):
                min_pass = min(min_values, key=lambda tup: tup[0])
                if min_pass[0] <= gas_remaining:
                    go_to = self.routing_table[min_pass[1]][taxi_loc]["nextHop"]
                    if act[2] == go_to:
                        points += 100
                        self.signal = True
                    else:
                        points -= 50
                        self.signal = True
                else:
                    if len(self.gas_stations) != 0:
                        min_gas_list = []
                        for station in self.gas_stations:
                            dist = self.routing_table[station][taxi_loc]["distance"]
                            min_gas_list.append((dist, station))
                        min_gas = min(min_gas_list, key=lambda tup: tup[0])
                        if gas_remaining >= min_gas[0]:
                            go_to = self.routing_table[min_gas[1]][taxi_loc]["nextHop"]
                            if act[2] == go_to:
                                points += 100
                                self.signal = True
                            else:
                                points -= 50
                                self.signal = True
                        else:
                            points -= 150

        return points


    def busy_taxi(self, state,act):
        points = 0
        for taxi in state["state"]["taxis"].keys():
            min_values = []
            gas_remaining = state["state"]["taxis"][taxi]["fuel"]
            taxi_loc = state["state"]["taxis"][taxi]["location"]
            for passenger in state["state"]["passengers"].keys():
                if state["state"]["passengers"][passenger]["location"] == taxi:
                    pass_dest = state["state"]["passengers"][passenger]["destination"]
                    distance = self.routing_table[taxi_loc][pass_dest]["distance"]
                    min_values.append((distance, pass_dest))
            if len(min_values):
                min_pass = min(min_values, key=lambda tup: tup[0])
                if min_pass[0] <= gas_remaining:
                    go_to = self.routing_table[min_pass[1]][taxi_loc]["nextHop"]
                    if act[2] == go_to:
                        points += 150
                        self.signal = True
                    else:
                        points -= 100
                        self.signal = True
                else:
                    if len(self.gas_stations) != 0:
                        min_gas_list = []
                        for station in self.gas_stations:
                            dist = self.routing_table[station][taxi_loc]["distance"]
                            min_gas_list.append((dist, station))
                        min_gas = min(min_gas_list, key=lambda tup: tup[0])
                        if gas_remaining >= min_gas[0]:
                            go_to = self.routing_table[min_gas[1]][taxi_loc]["nextHop"]
                            if act[2] == go_to:
                                points += 150
                                self.signal = True
                            else:
                                points -= 100
                                self.signal = True
                        else:
                            points -= 200
        return points


    def reward(self, state, action):
        # return the reward for taking the given action in the given state
        if len(self.taxis_list) == 1:
            action = [action]
        points = 0
        for act in action:
            if len(act) == 3:
                verb = act[0]
                if verb == "pick up":
                    points += 100
                elif verb == "drop off":
                    points += 200
                elif verb == "wait":
                    points -= 50
                elif verb == "move":

                    points += self.empty_taxi(state,act)
                    points += self.busy_taxi(state,act)
            elif len(act) == 2:
                if act[0] == "refuel":
                    # in refuel
                    for taxi in state["state"]["taxis"].keys():
                        min_values = []
                        gas_remaining = state["state"]["taxis"][taxi]["fuel"]
                        taxi_loc = state["state"]["taxis"][taxi]["location"]
                        for passenger in state["state"]["passengers"].keys():
                            pass_loc = state["state"]["passengers"][passenger]["location"]
                            pass_dest = state["state"]["passengers"][passenger]["destination"]
                            if pass_loc not in self.taxis_list and pass_dest != pass_loc:
                                distance = self.routing_table[taxi_loc][pass_loc]["distance"]
                                min_values.append((distance, pass_loc))
                        if len(min_values):
                            min_pass = min(min_values, key=lambda tup: tup[0])
                            if min_pass[0] == gas_remaining:
                                points += 200

            elif act == 'reset' or act == ("reset",):
                temp = 0
                self.signal = False
                # temp += self.empty_taxi(state, act)
                # temp += self.busy_taxi(state, act)
                if not self.signal:
                    points += 0
                in_loc = True
                for passenger in state["state"]["passengers"].keys():
                    pass_loc = state["state"]["passengers"][passenger]["location"]
                    pass_dest = state["state"]["passengers"][passenger]["destination"]
                    if pass_dest != pass_loc:
                        in_loc = False
                        break
                if in_loc:
                    points += 100
                have_fuel = False
                for taxi in self.taxis_list:
                    fuel = state["state"]["taxis"][taxi]["fuel"]
                    taxi_loc = state["state"]["taxis"][taxi]["location"]
                    taxi_tile = self.map[taxi_loc[0]][taxi_loc[1]]
                    if (fuel == 0 and taxi_tile == 'G') or fuel > 0:
                        have_fuel = True
                        break
                if not have_fuel:
                    points += 0
        return points


    def mdp(self, state, depth):
        if depth == 0:
            # base case: return heuristic value of state
            return self.heuristic(state)

        # get all possible actions for the current state
        action = actions(state, self.initial)
        dests = self.calculateDests(self.initial)

        values = []
        for act in action:
            # compute the value of taking the action and transitioning to the next state
            res = result(self.initial, state, act)
            stoch_states = self.stochStates(res, dests)
            for hash_val in stoch_states.keys():
                prob = stoch_states[hash_val]["probability"]
                value = self.reward(state, act) + prob * self.mdp(stoch_states[hash_val], depth - 1)
                values.append([value, act])

        # return the maximum value among all possible actions
        max_val = max(values, key=lambda tup: tup[0])
        if depth == self.depth:
            state["action"] = max_val[1]
        return max_val[0]



    # def pass_on_taxi(self, state):
    #     points = 0
    #     for passenger in state["state"]["passengers"].keys():
    #         if state["state"]["passengers"][passenger]["location"] in self.taxis_list:
    #             taxi_name = state["state"]["passengers"][passenger]["location"]
    #             taxi_loc = state["state"]["taxis"][taxi_name]["location"]
    #             pass_dest = state["state"]["passengers"][passenger]["destination"]
    #             man_dist = man_distance(taxi_loc, pass_dest)
    #             if man_dist != 0:
    #                 points += (1/man_dist)*1
    #             else:
    #                 points += 2000
    #     return points

    # def pass_on_taxi(self, state):
    #     points = 0
    #     for taxi in self.taxis_list:
    #         # if taxi has passengers
    #         cap = self.initial["taxis"][taxi]["capacity"]
    #         if self.temp_init["state"]["taxis"][taxi]["capacity"] != cap and state["state"]["taxis"][taxi]["capacity"] != cap:
    #             min_list_init = [0, float("inf")]
    #             min_list_state = [0, float("inf")]
    #             taxi_loc_init = self.temp_init["state"]["taxis"][taxi]["location"]
    #             taxi_loc_state = state["state"]["taxis"][taxi]["location"]
    #             for passenger in self.temp_init["state"]["passengers"].keys():
    #                 if self.temp_init["state"]["passengers"][passenger]["location"] == taxi:
    #                     pass_dest_init = self.temp_init["state"]["passengers"][passenger]["destination"]
    #                     man_dist_init = man_distance(pass_dest_init, taxi_loc_init)
    #                     if man_dist_init < min_list_init[1]:
    #                         min_list_init[0] = passenger
    #                         min_list_init[1] = man_dist_init
    #                 if state["state"]["passengers"][passenger]["location"] == taxi:
    #                     pass_dest_state = state["state"]["passengers"][passenger]["destination"]
    #                     man_dist_state = man_distance(pass_dest_state, taxi_loc_state)
    #                     if man_dist_state < min_list_state[1]:
    #                         min_list_state[0] = passenger
    #                         min_list_state[1] = man_dist_state
    #             if min_list_state[1] < min_list_init[1]:
    #                 points += 100
    #     return points



    # def pass_on_taxi(self, state, action):
    #     # need to be two or more taxis
    #     points = 0
    #     if action[0] == "move":
    #         for taxi in self.taxis_list:
    #             if state["state"]["taxis"][taxi]["capacity"] != self.initial["taxis"][taxi]["capacity"]:
    #                 min_list = [0, float("inf")]
    #                 taxi_loc = state["state"]["taxis"][taxi]["location"]
    #                 for passenger in state["state"]["passengers"].keys():
    #                     if state["state"]["passengers"][passenger]["location"] == taxi:
    #                         pass_dest = state["state"]["passengers"][passenger]["destination"]
    #                         man_dist = man_distance(pass_dest, taxi_loc)
    #                         if man_dist < min_list[1]:
    #                             min_list[0] = passenger
    #                             min_list[1] = man_dist
    #                 if state["state"]["taxis"][taxi]["fuel"] >= min_list[1]:
    #                     new_loc = action[2]
    #                     pass_dest = state["state"]["passengers"][min_list[0]]["destination"]
    #                     new_man_dist = man_distance(pass_dest, new_loc)
    #                     if new_man_dist <= min_list[1]:
    #                         points += 10
    #                 else:
    #                     if len(self.gas_stations) != 0:
    #                         min_dist = float("inf")
    #                         for station in self.gas_stations:
    #                             man_dist = man_distance(taxi_loc, station)
    #                             if man_dist < min_dist:
    #                                 min_dist = man_dist
    #                         if state["state"]["taxis"][taxi]["fuel"] >= min_dist:
    #                             points += 5
    #                         else:
    #                             points -= 20
    #     return points
    #
    # def empty_taxi(self, state):
    #     points = 0
    #     for taxi in self.taxis_list:
    #         # if taxi is empty
    #         cap = self.initial["taxis"][taxi]["capacity"]
    #         if self.temp_init["state"]["taxis"][taxi]["capacity"] == cap and state["state"]["taxis"][taxi]["capacity"] == cap:
    #             min_list_temp_init = [0, float("inf")]
    #             taxi_loc = self.temp_init["state"]["taxis"][taxi]["location"]
    #             for passenger in self.temp_init["state"]["passengers"].keys():
    #                 pass_loc = self.temp_init["state"]["passengers"][passenger]["location"]
    #                 pass_dest = self.temp_init["state"]["passengers"][passenger]["destination"]
    #                 if pass_loc != pass_dest and pass_loc not in self.taxis_list:
    #                     man_dist = man_distance(pass_loc, taxi_loc)
    #                     if man_dist < min_list_temp_init[1]:
    #                         min_list_temp_init[0] = passenger
    #                         min_list_temp_init[1] = man_dist
    #             min_list_state = [0, float("inf")]
    #             taxi_loc = state["state"]["taxis"][taxi]["location"]
    #             for passenger in state["state"]["passengers"].keys():
    #                 pass_loc = state["state"]["passengers"][passenger]["location"]
    #                 pass_dest = state["state"]["passengers"][passenger]["destination"]
    #                 if pass_loc != pass_dest and pass_loc not in self.taxis_list:
    #                     man_dist = man_distance(pass_loc, taxi_loc)
    #                     if man_dist < min_list_state[1]:
    #                         min_list_state[0] = passenger
    #                         min_list_state[1] = man_dist
    #             fuel = state["state"]["taxis"][taxi]["fuel"]
    #             if min_list_state[1] < min_list_temp_init[1] and fuel > min_list_state[1]:
    #                 points += 100
    #     return points
    #
    # def pick_up_drop_off(self, state):
    #     points = 0
    #     for taxi in self.taxis_list:
    #         state_cap = state["state"]["taxis"][taxi]["capacity"]
    #         init_cap = self.temp_init["state"]["taxis"][taxi]["capacity"]
    #         if state_cap < init_cap:
    #             # pick up
    #             points += 1000
    #         elif state_cap > init_cap:
    #             # drop off
    #             points += 1000
    #     return points
    #
    # def pass_in_dest(self, state):
    #     points = 0
    #     for passenger in state["state"]["passengers"].keys():
    #         if state["state"]["passengers"][passenger]["location"] in self.taxis_list and self.temp_init["state"]["passengers"][passenger]["location"] in self.taxis_list :
    #             taxi_name = state["state"]["passengers"][passenger]["location"]
    #             taxi_loc_init = self.temp_init["state"]["taxis"][taxi_name]["location"]
    #             taxi_loc_state = state["state"]["taxis"][taxi_name]["location"]
    #             pass_dest_init = self.temp_init["state"]["passengers"][passenger]["destination"]
    #             pass_dest_state = state["state"]["passengers"][passenger]["destination"]
    #             if taxi_loc_init != pass_dest_init and taxi_loc_state == pass_dest_state:
    #                 points += 0
    #     return points
    #

    # def all_in_dest(self, state, action, parent):
    #     points = 0
    #     if action == "reset":
    #         is_in_dest = True
    #         for passenger in state["state"]["passengers"].keys():
    #             pass_dest = state["state"]["passengers"][passenger]["destination"]
    #             pass_loc = state["state"]["passengers"][passenger]["location"]
    #             if pass_dest != pass_loc:
    #                 is_in_dest = False
    #                 break
    #         if is_in_dest:
    #             points += 100
    #     return points
    #
    # def calculate_h(self, state):
    #     w1, w2, w3, w4 = 1, 1, 0, 0
    #     w1 *= self.pass_on_taxi(state)
    #     w2 *= self.empty_taxi(state)
    #     # w4 *= self.pass_in_dest(state)
    #     return w1 + w2 + w3 + w4


    #
    # def ChooseAction(self, root_state, i):
    #     if i == 0:
    #         value = self.calculate_h(root_state)
    #
    #         root_state["value"] = value
    #         return
    #     action = actions(root_state, self.initial)
    #     dests = self.calculateDests(self.initial)
    #
    #     for act in action:
    #         # if act[0] == 'wait':
    #         #     continue
    #         res = result(self.initial, root_state, act)
    #         stoch_states = self.stochStates(res, dests)
    #         val = 0
    #         for hash_val in stoch_states.keys():
    #             stoch_states[hash_val]["value"] = 0
    #             self.ChooseAction(stoch_states[hash_val], i - 1)
    #             prob = stoch_states[hash_val]["probability"]
    #             value = stoch_states[hash_val]["value"]
    #             val += value * prob
    #         # x ={'taxis': {'taxi 1': {'location': (0, 1), 'fuel': 3, 'capacity': 0}}, 'passengers': {'Dana': {'location': 'taxi 1', 'destination': (0, 0), 'possible_goals': ((0, 0), (2, 2)), 'prob_change_goal': 0.1}}}
    #         # ha = hash(json.dumps(x))
    #         # ha1 = hash(json.dumps(root_state["state"]))
    #         # if ha == ha1:
    #         #     print(act, val)
    #
    #         if val > root_state["value"]:
    #             root_state["value"] = val
    #             root_state["action"] = act

    def act(self, state):

        new_state = copy.deepcopy(state)
        del new_state["optimal"]
        del new_state["map"]
        del new_state["turns to go"]
        if len(new_state["passengers"].keys()) == 3:
            del new_state["passengers"]["Wolfgang"]
        hash_val = hash(json.dumps((new_state)))
        action = self.states_dict[hash_val]["action"]

        # print(self.states_dict[hash_val])
        if hash_val == self.hash_val_initial and action == ('reset',):
            return 'terminate'
        print("i did",action)
        # if len(state["taxis"].keys()) == 1:
        if action == ('reset',):
            return 'reset'
        elif action == ('terminate',):
            return 'terminate'
        # else:
        if len(state["taxis"].keys()) == 1:
            return ((action,))
        return action
