small_inputs = [
{
        "optimal": False,
        "map": [['P', 'P', 'G'],
                ['P', 'P', 'P'],
                ['G', 'P', 'P']],
        "taxis": {'taxi 1': {"location": (0, 0), "fuel": 3, "capacity": 1},
                  'taxi 2': {"location": (0, 1), "fuel": 3, "capacity": 1}},
        "passengers": {'Dana': {"location": (0, 2), "destination": (2, 2),
                                "possible_goals": ((2, 2),), "prob_change_goal": 0.1},
                       'Dan': {"location": (2, 0), "destination": (2, 2),
                               "possible_goals": ((2, 2),), "prob_change_goal": 0.1}
                       },
        "turns to go": 100
    },
# additionals

# only omer alone
    # {
    #     'optimal': False,
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


    # לא מצליחים כי אין פתרון?
    # {
    #     'optimal': False,
    #     "turns to go": 50,
    #     'map': [['P', 'P', 'P', 'I', 'P', 'P', 'P'],
    #             ['P', 'I', 'P', 'P', 'P', 'P', 'I'],
    #             ['P', 'P', 'I', 'P', 'P', 'I', 'P'],
    #             ['P', 'G', 'P', 'I', 'P', 'G', 'P'],
    #             ['P', 'P', 'P', 'P', 'P', 'I', 'P'],
    #             ['P', 'P', 'G', 'I', 'P', 'P', 'P']],
    #     'taxis': {'taxi 1': {'location': (1, 0), 'fuel': 6, 'capacity': 2}},
    #     'passengers': {'Yael': {'location': (5, 4), 'destination': (1, 6),
    #                             'possible_goals': ((1, 6), (3, 6), (4, 6)), 'prob_change_goal': 0.2},
    #                    'Janet': {'location': (5, 5), 'destination': (3, 6),
    #                              'possible_goals': ((1, 6), (3, 6), (4, 6)), 'prob_change_goal': 0.5},
    #                    'Francois': {'location': (5, 0), 'destination': (4, 6),
    #                                 'possible_goals': ((1, 6), (3, 6), (4, 6)), 'prob_change_goal': 0.2}},
    # },
    #
    # only one taxi got it ok
    # {
    #     'optimal': False,
    #     "turns to go": 100,
    #     'map': [['P', 'P', 'P', 'P', 'P'],
    #             ['P', 'I', 'P', 'P', 'P'],
    #             ['P', 'P', 'I', 'P', 'P'],
    #             ['P', 'P', 'P', 'I', 'P'],
    #             ['P', 'P', 'P', 'G', 'P']],
    #     'taxis': {'taxi 1': {'location': (4, 4), 'fuel': 17, 'capacity': 1},
    #               'taxi 2': {'location': (2, 1), 'fuel': 18, 'capacity': 3}},
    #     'passengers': {'Freyja': {'location': (4, 2), 'destination': (4, 4),
    #                               'possible_goals': ((4, 4), (4, 2), (0, 0)), 'prob_change_goal': 0.2},
    #                    'Dave': {'location': (0, 0), 'destination': (3, 3),
    #                             'possible_goals': ((3, 3), (4, 2), (0, 0)), 'prob_change_goal': 0.2},
    #                    'Janet': {'location': (1, 4), 'destination': (3, 3),
    #                              'possible_goals': ((3, 3), (1, 4), (3, 1)), 'prob_change_goal': 0.2},
    #                    'Francois': {'location': (3, 1), 'destination': (0, 3),
    #                                 'possible_goals': ((0, 3), (4, 4), (2, 1)), 'prob_change_goal': 0.2}},
    # },
    #


]


