import numpy as np
# This MDP will start at the given state, and explore the tree of possible states and actions to a depth of 2. At each level, it will use the heuristic function to evaluate the value of each state, and then choose the action that leads to the state with the highest value.
# shahar128@gmail.com
# code in python for mdp that given a state opens a tree in depth of 2 calculate hureistic value and decide what action to do
def mdp(state, depth):
    if depth == 0:
        # base case: return heuristic value of state
        return heuristic(state)

    # get all possible actions for the current state
    actions = get_actions(state)

    values = []
    for action in actions:
        # compute the value of taking the action and transitioning to the next state
        next_state = transition(state, action)
        value = reward(state, action) + mdp(next_state, depth - 1)
        values.append(value)

    # return the maximum value among all possible actions
    return max(values)


def heuristic(state):
    # implement your heuristic function here
    pass


def get_actions(state):
    # return a list of all possible actions for the given state
    pass


def transition(state, action):
    # return the next state given the current state and action
    pass


def reward(state, action):
    # return the reward for taking the given action in the given state
    pass
