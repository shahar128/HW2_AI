import numpy as np
# This MDP will start at the given state, and explore the tree of possible states and actions to a depth of 2. At each level, it will use the heuristic function to evaluate the value of each state, and then choose the action that leads to the state with the highest value.
# shahar128@gmail.com
# code in python for mdp that given a state opens a tree in depth of 2 calculate hureistic value and decide what action to do
# def mdp(state, depth):
#     if depth == 0:
#         # base case: return heuristic value of state
#         return heuristic(state)
#
#     # get all possible actions for the current state
#     actions = get_actions(state)
#
#     values = []
#     for action in actions:
#         # compute the value of taking the action and transitioning to the next state
#         next_state = transition(state, action)
#         value = reward(state, action) + mdp(next_state, depth - 1)
#         values.append(value)
#
#     # return the maximum value among all possible actions
#     return max(values)
#
#
# def heuristic(state):
#     # implement your heuristic function here
#     pass
#
#
# def get_actions(state):
#     # return a list of all possible actions for the given state
#     pass
#
#
# def transition(state, action):
#     # return the next state given the current state and action
#     pass
#
#
# def reward(state, action):
#     # return the reward for taking the given action in the given state
#     pass
#

# def heuristic(self, state):
#     points = 0
#
#     # Consider the distance and gas remaining for each passenger-carrying taxi
#     for passenger in state["state"]["passengers"].keys():
#         if state["state"]["passengers"][passenger]["location"] in self.taxis_list:
#             pass_dest = state["state"]["passengers"][passenger]["destination"]
#             taxi_name = state["state"]["passengers"][passenger]["location"]
#             taxi_loc = state["state"]["taxis"][taxi_name]["location"]
#             man_dist = man_distance(taxi_loc, pass_dest)
#             gas_remaining = state["state"]["taxis"][taxi_name]["fuel"]
#             if man_dist > gas_remaining:
#                 # Subtract a large value from the score if the taxi doesn't have enough gas to reach the destination
#                 points -= 1000
#             else:
#                 if man_dist != 0:
#                     points += (1/man_dist)*1000
#                 else:
#                     points += 2000
#
#     # Consider the distance to the nearest passenger for each empty taxi
#     for taxi in state["state"]["taxis"].keys():
#         min_values = []
#         for passenger in state["state"]["passengers"].keys():
#             if state["state"]["passengers"][passenger]["location"] not in self.taxis_list:
#                 taxi_loc = state["state"]["taxis"][taxi]["location"]
#                 pass_loc = state["state"]["passengers"][passenger]["location"]
#                 man_dist = man_distance(taxi_loc, pass_loc)
#                 gas_remaining = state["state"]["taxis"][taxi]["fuel"]
#                 if man_dist > gas_remaining:
#                     # Subtract a value from the score if the taxi doesn't have enough gas to reach the passenger
#                     man_dist -= 100
#                 min_values.append(man_dist)
#         if len(min_values) != 0:
#             min_val = min(min_values)
#             if min_val != 0:
#                 points += (1 / min_val) * 100
#             else:
#                 points += 200
#     return points
# def get_next_tile(grid, start, end, current):
#     # First, we'll create a queue of tiles to visit and add the start tile to it
#     queue = [start]
#
#     # We'll also create a dictionary to store the "came from" information for each tile, which will allow us to reconstruct the path later
#     came_from = {}
#
#     # We'll set the "came from" value for the start tile to None, since it has no predecessor
#     came_from[start] = None
#
#     # Now we'll start the search. We'll continue looping as long as there are tiles in the queue
#     while queue:
#         # Get the next tile to visit from the queue
#         current_tile = queue.pop(0)
#
#         # If the current tile is the end tile, we're done!
#         if current_tile == end:
#             break
#
#         # Get the row and column of the current tile
#         row, col = current_tile
#
#         # Check the tiles in the four cardinal directions (north, south, east, west)
#         for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
#             # Calculate the row and column of the neighboring tile
#             new_row, new_col = row + direction[0], col + direction[1]
#
#             # Make sure the neighboring tile is within the grid and is a possible tile
#             if (0 <= new_row < len(grid)) and (0 <= new_col < len(grid[0])) and (grid[new_row][new_col] == 1):
#                 # Add the neighboring tile to the queue and set its "came from" value to the current tile
#                 queue.append((new_row, new_col))
#                 came_from[(new_row, new_col)] = current_tile
#
#     # Now that we've finished the search, we can reconstruct the path by starting at the end tile and following the "came from" information backwards
#     path = []
#     while current_tile != start:
#         path.append(current_tile)
#         current_tile = came_from[current_tile]
#     path.append(start)  # Add the start tile to the path
#     path.reverse()  # Reverse the path to get the order from start to end
#
#     # Return the next tile to go to, which is the second tile in the path (since the first tile is the current tile)
#     return path[1]
#
#
# grid =          [[1,1, 1, 1, 1],
#                 [1, 0, 1, 1, 1],
#                 [1, 1, 0, 1, 1],
#                 [1, 1,1, 0,1]]
# start = (1,2)
# end = (3,2)
# curr = start
# print(get_next_tile(grid,start,end,curr))

from collections import deque
#
# def generate_routing_table(grid):
#     # Initialize a routing table for each tile in the grid
#     routing_table = {(i, j): {} for i in range(len(grid)) for j in range(len(grid[0]))}
#
#     # Perform a breadth-first search on the grid to populate the routing table
#     for i in range(len(grid)):
#         for j in range(len(grid[0])):
#             # Skip tiles that are not connected (represented by a 0 in the grid)
#             if grid[i][j] == 0:
#                 continue
#
#             # Initialize a queue for the breadth-first search and add the current tile
#             queue = deque([(i, j, 0)])
#             visited = set()
#             prev = {(i, j): None}
#
#             # Perform the breadth-first search
#             while queue:
#                 x, y, distance = queue.popleft()
#                 visited.add((x, y))
#
#                 # Add the current tile to the routing table for the starting tile
#                 routing_table[(i, j)][(x, y)] = (prev[(x, y)], distance)
#
#                 # Add the neighbors of the current tile to the queue if they are not visited
#                 for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
#                     if (x + dx, y + dy) not in visited and 0 <= x + dx < len(grid) and 0 <= y + dy < len(grid[0]):
#                         queue.append((x + dx, y + dy, distance + 1))
#                         prev[(x + dx, y + dy)] = (x, y)
#
#     return routing_table
#
# # Example usage
# grid =          [[1, 1, 1, 1, 1],
#                 [1, 0, 1, 1, 1],
#                 [1, 1, 0, 1, 1],
#                 [1, 1, 1, 0, 1]]
#
#
# routing_table = generate_routing_table(grid)
# print(routing_table[(0,2)][(3,2)]   )

# from collections import deque
from utils import collections
import collections

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


# Example usage
grid = [['P', 'P', 'P', 'P', 'P'],
        ['P', 'I', 'P', 'G', 'P'],
        ['P', 'P', 'I', 'P', 'P'],
        ['P', 'P', 'P', 'I', 'P']]
# for i in range(len(grid)):
#     for j in range(len(grid[0])):
#         if grid[i][j] in ["G", "P"]:
#             grid[i][j] = 1
#         else:
#             grid[i][j] = 0
# print(grid)
# routingTables = createRoutingTables(grid)
# print(routingTables[(0, 2)][(3, 2)])
# li = [("dana")]
# sorted(li,key=lambda sl: (-sl[0],sl[1]))

initial = {
        'optimal': False,
        "turns to go": 50,
        'map': [['P', 'P', 'P', 'P', 'P'],
                ['P', 'I', 'P', 'P', 'P'],
                ['P', 'P', 'I', 'P', 'P'],
                ['P', 'P', 'P', 'I', 'P'],
                ['P', 'P', 'P', 'G', 'P']],
        'taxis': {'taxi 1': {'location': (1, 2), 'fuel': 18, 'capacity': 1}},
        'passengers': {'Freyja': {'location': (2, 0), 'destination': (4, 2),
                                  'possible_goals': ((4, 2), (2, 0)), 'prob_change_goal': 0.2},
                       'Wolfgang': {'location': (2, 1), 'destination': (1, 4),
                                    'possible_goals': ((1, 4), (0, 0)), 'prob_change_goal': 0.8},
                       'Jacob': {'location': (3, 4), 'destination': (3, 2),
                                 'possible_goals': ((3, 2), (0, 0)), 'prob_change_goal': 0.2}},
    }

passengers_list = list(initial["passengers"].keys())
priority_passengers = []
for passenger in passengers_list:
    pass_prob = initial["passengers"][passenger]["prob_change_goal"]
    num_goals = len(initial["passengers"][passenger]["possible_goals"])
    priority_passengers.append((passenger, pass_prob, num_goals))
sorted_elements = sorted(priority_passengers, key=lambda x: (x[1],x[2]), reverse= True)
print(sorted_elements)

# def value_iteration(states_dict, initial, dests_combined):
#     ##initialize
#     for hash_state in states_dict.keys():
#         states_dict[hash_state]["reward"] = 0
#         states_dict[hash_state]["value"] = 0
#
#     # rounds
#     max_iter = 100  # Maximum number of iterations
#     epsilon = 0.01  # Error tolerance
#
#     for i in range(max_iter):
#         for hash_value in states_dict.keys():
#             state = states_dict[hash_value]
#             actions_tup = actions(state, initial)
#             max_val = float('-inf')
#             reward = 0
#             if len(initial["taxis"].keys()) == 1:
#                 for act in actions_tup:
#                     sigma = 0
#                     res = result(initial, state, act)
#                     stoch_res = turn_to_stoch(res, dests_combined)
#                     for s_res in stoch_res:
#                         V = states_dict[s_res]["value"]
#                         P = stoch_res[s_res]
#                         sigma += V * P
#                     reward = 0
#                     if act == "reset":
#                         reward -= 50
#                     elif act == "terminate":
#                         reward -= 10000
#                     elif act[0] == "refuel":
#                         reward -= 10
#                     elif act[0] == "drop off":
#                         reward += 100
#                     elif act[0] == "wait":
#                         reward -= 100
#                     if sigma + reward >= max_val:
#                         states_dict[hash_value]["action"] = act
#                         states_dict[hash_value]["value"] = sigma + reward
#                     max_val = max(max_val, sigma + reward)
#             else:
#                 for act in actions_tup:
#                     sigma = 0
#                     res = result(initial, state, act)
#                     stoch_res = turn_to_stoch(res, dests_combined)
#                     reward = 0
#                     for s_res in stoch_res:
#                         V = states_dict[s_res]["value"]
#                         P = stoch_res[s_res]
#                         sigma += V * P
#                     for taxi_act in act:
#                         if taxi_act == "reset":
#                             reward -= 50
#                         elif taxi_act == "terminate":
#                             reward -= 10000
#                         elif taxi_act[0] == "refuel":
#                             reward -= 10
#                         elif taxi_act[0] == "drop off":
#                             reward += 100
#                         elif taxi_act[0] == "wait":
#                             reward -= 100
#                     if sigma + reward >= max_val:
#                         states_dict[hash_value]["action"] = act
#                         states_dict[hash_value]["value"] = sigma + reward
#                     max_val = max(max_val, sigma + reward)
#
#     return states_dict
# for i in range(1, 101):
#     print(i)
# x = [0]* 101
# print(len(x))
x =[0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.14025, 8.116474999999998, 11.945077499999998, 15.640819749999995, 75.98442130312498, 77.20400729781247, 81.78623875173433, 83.33708187342282, 85.10557008363979, 89.1728633972154, 90.90650762599658, 94.80958015688434, 98.39661714701786, 102.19591035214077, 105.69383985886805, 114.11441807010813, 117.53488347280147, 121.420719402804, 124.80792465521334, 128.38491477745512, 131.93340623177284, 135.4273221414209, 139.0802489562769, 142.64625475530397, 146.3047874412136, 149.9574040906245, 153.98901899269643, 157.64795144571727, 161.53964360635615, 165.19974789216886, 168.89899540137668, 172.58455621554333, 176.2838542694525, 179.9860852213937, 183.69044388134148, 187.40445250575405, 191.11814220203496, 194.83853554252906, 198.561014491822, 202.2996874416069, 206.02705188108214, 209.76626573598188, 213.49868003837116, 217.23493772847237, 220.97200264616393, 224.71093488761377, 228.45116922719757, 232.19258394756022, 235.9353737345926, 239.67904282666254, 243.42380937001155, 247.16933309100864, 250.9161462818004, 254.6630840347793, 258.4110329163561, 262.159158932909, 265.90784208250886, 269.6568761987429, 273.40625778059075, 277.1559141206116, 280.9057952061472, 284.655865721072, 288.40606603176815, 292.1563691023713, 295.9067252168419, 299.6571263621925, 303.4074983800066, 307.15785243748206, 310.90813182013665, 314.65833236338943, 318.4084271664953, 322.1584010669333, 325.90823788033725, 329.6579244346305, 333.4074499828831, 337.15680455948177, 340.905981174941, 344.65497330185485, 348.40377761837686, 352.15238937241907, 355.9008084187119, 359.64903288682046, 363.3970640275946, 367.1449029745716, 370.8925521540764, 374.6400146153501, 378.38729413369833, 382.13439510269393, 385.88132239715037, 389.628081394482, 393.3746778027403, 397.1211177218302, 400.8674073941324, 404.61355339878486, 408.35956234678315, 412.10544103657577]
print(x[100])