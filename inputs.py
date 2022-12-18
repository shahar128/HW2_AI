small_inputs = [
    # 3x3 1 taxi, 1 passenger w/ 2 possible goals, plenty of fuel

    {
        'optimal': False,
        "turns to go": 100,
        'map': [['P', 'P', 'P', 'I', 'P', 'P', 'P'],
                ['P', 'I', 'P', 'P', 'P', 'P', 'I'],
                ['P', 'P', 'I', 'P', 'P', 'I', 'P'],
                ['P', 'G', 'P', 'I', 'P', 'G', 'P'],
                ['P', 'P', 'P', 'P', 'P', 'I', 'P'],
                ['P', 'P', 'G', 'I', 'P', 'P', 'P']],
        'taxis': {'taxi 1': {'location': (5, 5), 'fuel': 6, 'capacity': 2}},
        'passengers': {'Janet': {'location': (5, 4), 'destination': (1, 4),
                                 'possible_goals': ((1, 4), (5, 0), (3, 4)), 'prob_change_goal': 0.05},
                       'Omer': {'location': (1, 5), 'destination': (5, 0),
                                'possible_goals': ((1, 4), (5, 0), (3, 4)), 'prob_change_goal': 0.4}

    }
    }

    # {
    #     'optimal': False,
    #     "turns to go": 50,
    #     'map': [['P', 'P', 'P', 'P', 'P'],
    #             ['P', 'I', 'P', 'G', 'P'],
    #             ['P', 'P', 'I', 'P', 'P'],
    #             ['P', 'P', 'P', 'I', 'P']],
    #     'taxis': {'taxi 1': {'location': (1, 3), 'fuel': 10, 'capacity': 3}},
    #     'passengers': {'Freyja': {'location': (0, 0), 'destination': (2, 1),
    #                               "possible_goals": ((2, 1), (0, 0)), "prob_change_goal": 0.3},
    #                    }
    # }

    # {
    #     "optimal": False,
    #     "map": [['P', 'P', 'P'],
    #             ['P', 'G', 'P'],
    #             ['P', 'P', 'P']],
    #     "taxis": {'taxi 1': {"location": (0, 0), "fuel": 10, "capacity": 1}},
    #     "passengers": {'Dana': {"location": (2, 2), "destination": (0, 0),
    #                             "possible_goals": ((0, 0),(2,2)), "prob_change_goal": 0.1}},
    #     "turns to go": 100
    # },
# {
#         "optimal": False,
#         "map": [['P', 'P', 'P'],
#                 ['P', 'G', 'P'],
#                 ['P', 'P', 'P']],
#         "taxis": {'taxi 1': {"location": (0, 0), "fuel": 10, "capacity": 1}},
#         "passengers": {'Dana': {"location": (2, 2), "destination": (0, 0),
#                                 "possible_goals": ((0, 0), (2, 2)), "prob_change_goal": 0.1}},
#         "turns to go": 100
#     }
#     {
#         'optimal': False,
#         "turns to go": 50,
#         'map': [['P', 'P', 'P', 'P', 'P'],
#                 ['P', 'I', 'P', 'G', 'P'],
#                 ['P', 'P', 'I', 'P', 'P'],
#                 ['P', 'P', 'P', 'I', 'P']],
#         'taxis': {'taxi 1': {'location': (3, 4), 'fuel': 10, 'capacity': 3}},
#         'passengers': {'Michael': {'location': (3, 4), 'destination': (2, 1),
#                                    "possible_goals": ((2, 1), (3, 4)), "prob_change_goal": 0.1}}
#     },
    # {
    #     'optimal': True,
    #     "turns to go": 100,
    #     'map': [['P', 'P', 'P', 'I', 'P', 'P', 'P'],
    #             ['P', 'I', 'P', 'P', 'P', 'P', 'I'],
    #             ['P', 'P', 'I', 'P', 'P', 'I', 'P'],
    #             ['P', 'G', 'P', 'I', 'P', 'G', 'P'],
    #             ['P', 'P', 'P', 'P', 'P', 'I', 'P'],
    #             ['P', 'P', 'G', 'I', 'P', 'P', 'P']],
    #     'taxis': {'taxi 1': {'location': (5, 6), 'fuel': 21, 'capacity': 3}},
    #     'passengers': {'Omer': {'location': (1, 5), 'destination': (2, 2),
    #                             'possible_goals': ((2, 2), (4, 3)), 'prob_change_goal': 0.2},
    #                    'Roee': {'location': (2, 1), 'destination': (4, 3),
    #                             'possible_goals': ((4, 3), (2, 2)), 'prob_change_goal': 0.5},
    #                    'Dana': {'location': (4, 2), 'destination': (5, 2),
    #                             'possible_goals': ((4, 3), (2, 2), (5, 2)), 'prob_change_goal': 0.2},
    #                    'Efrat': {'location': (5, 6), 'destination': (2, 3),
    #                              'possible_goals': ((2, 3), (2, 2), (4, 3)), 'prob_change_goal': 0.3}},
    # },
    # {
    #     "optimal": True,
    #     "map": [['P', 'P', 'P', 'P'],
    #             ['I', 'I', 'I', 'G'],
    #             ['P', 'P', 'P', 'P']],
    #     "taxis": {'taxi 1': {"location": (0, 0), "fuel": 8, "capacity": 1}},
    #     "passengers": {'Dana': {"location": (2, 0), "destination": (0, 0),
    #                             "possible_goals": ((0, 0), (2, 0)), "prob_change_goal": 0.01}},
    #     "turns to go": 100
    # }
    # {
    #     "optimal": True,
    #     "map": [['P', 'P', 'P'],
    #             ['P', 'G', 'P'],
    #             ['P', 'P', 'P']],
    #     "taxis": {'taxi 1': {"location": (0, 0), "fuel": 10, "capacity": 1}},
    #     "passengers": {'Dana': {"location": (2, 2), "destination": (0, 0),
    #                             "possible_goals": ((0, 0), (2, 2)), "prob_change_goal": 0.1}},
    #     "turns to go": 100
    # },
    # 3x3 1 taxi, 1 passenger w/ 2 possible goals, low fuel
    # {
    #     "optimal": True,
    #     "map": [['P', 'P', 'P'],
    #             ['P', 'G', 'P'],
    #             ['P', 'P', 'P']],
    #     "taxis": {'taxi 1': {"location": (0, 0), "fuel": 4, "capacity": 1}},
    #     "passengers": {'Dana': {"location": (2, 2), "destination": (0, 0),
    #                             "possible_goals": ((0, 0), (2, 2)), "prob_change_goal": 0.1}},
    #     "turns to go": 100
    # },
    # # 3x3 2 taxi, 2 passengers w/ 1 possible goals, low fuel
    # {
    #     "optimal": True,
    #     "map": [['P', 'P', 'G'],
    #             ['P', 'P', 'P'],
    #             ['G', 'P', 'P']],
    #     "taxis": {'taxi 1': {"location": (0, 0), "fuel": 3, "capacity": 1},
    #               'taxi 2': {"location": (0, 0), "fuel": 3, "capacity": 1}},
    #     "passengers": {'Dana': {"location": (0, 2), "destination": (2, 2),
    #                             "possible_goals": ((2, 2),), "prob_change_goal": 0.1},
    #                    'Dan': {"location": (2, 0), "destination": (2, 2),
    #                            "possible_goals": ((2, 2),), "prob_change_goal": 0.1}
    #                    },
    #     "turns to go": 100
    # },
    # # 3x4 1 taxi, 1 passenger w/ 2 possible goals, low fuel
    # {
    #     "optimal": False,
    #     "map": [['P', 'P', 'P', 'P'],
    #             ['I', 'I', 'I', 'G'],
    #             ['P', 'P', 'P', 'P']],
    #     "taxis": {'taxi 1': {"location": (0, 0), "fuel": 8, "capacity": 1}},
    #     "passengers": {'Dana': {"location": (2, 0), "destination": (0, 0),
    #                             "possible_goals": ((0, 0), (2, 0)), "prob_change_goal": 0.01}},
    #     "turns to go": 100
    # },
    # # 4x4 2 taxi, 1 passenger w/ 2 possible goals, no gas station
    # {
    #     "optimal": False,
    #     "map": [['P', 'P', 'P', 'P'],
    #             ['I', 'I', 'I', 'P'],
    #             ['I', 'I', 'I', 'P'],
    #             ['P', 'P', 'P', 'P']],
    #     "taxis": {'taxi 1': {"location": (0, 0), "fuel": 12, "capacity": 1},
    #               'taxi 2': {"location": (3, 0), "fuel": 12, "capacity": 1}},
    #     "passengers": {'Dana': {"location": (3, 0), "destination": (2, 3),
    #                             "possible_goals": ((2, 3), (3, 2)), "prob_change_goal": 0.5}},
    #     "turns to go": 100
    # }
    #addition
# {
#         'optimal': True,
#         "turns to go": 50,
#         'map': [['P', 'P', 'G', 'P', 'P'], ],
#         'taxis': {'taxi 1': {'location': (0, 0), 'fuel': 10, 'capacity': 1}},
#         'passengers': {'Michael': {'location': (0, 0), 'destination': (0, 4),
#                                    "possible_goals": ((0, 0), (0, 4)), "prob_change_goal": 0.2},
#                        }
#     },
]
