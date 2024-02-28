"""
worldmodel.py
Simple shared state model used to track conditions in the world.
NOTE: for the GOAP implementation we will use this to model the
    agent's belief about the world and how it will change due to
    certain actions. It will likely contain only a subset of the
    overall world state and will include some differences.
Created: Chris Branton, 2023-03-08.
"""
import uuid
from goal import Goal
from action import Action


class WorldModel:
    def __init__(self, start_state, goal_list=[], action_list=[], depth=0):
        self.current_state = start_state
        self.goal_list = []
        for curr_goal in goal_list:
            self.goal_list.append(Goal(curr_goal))
        self.action_list = []
        for curr_action in action_list:
            act = Action(curr_action)
            self.action_list.append(act)
        self.id = self.generate_id()
        self.current_depth = depth
        self.best_plan = []
        self.current_action_index = -1

    @property
    def num_actions(self):
        return len(self.action_list)

    # return the value of the named variable
    def get_state(self, var_name):
        if var_name in self.current_state:
            return self.current_state[var_name]
        return False

    # calculate the total cost of actions in our list
    def get_total_cost(self):
        cost = 0
        for action in self.action_list:
            cost += action.get_cost
        return cost

    # select the next action that applies
    def next_action(self):
        self.current_action_index += 1
        for a in self.action_list:
            if not a.requires:
                return a
            for precondition in a.requires:
                if precondition in self.current_state:
                    return a
        return None

    # Remove an action from our action list
    def remove_action(self, act):
        for a in self.action_list:
            if a.name == act.name:
                self.action_list.remove(a)

    # Apply an action to the world state and remove it from the list
    # TODO: generalize action effects
    def apply_action(self, action):
        if action.results:
            for r in action.results:
                # Assume all state variables are Boolean and all actions make them true
                self.current_state[r] = True
        self.remove_action(action)

    # generate a unique ID for this model
    @staticmethod
    def generate_id():
        return uuid.uuid4()
