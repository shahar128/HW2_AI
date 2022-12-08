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
print(("ofer",))