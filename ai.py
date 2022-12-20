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
print(grid)
routingTables = createRoutingTables(grid)
print(routingTables[(0, 2)][(3, 2)])
