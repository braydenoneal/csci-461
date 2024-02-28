"""
action.py
Actions and related code for goal-oriented behavior modeling.
Created: Chris Branton, 2023-03-07.

Preconditions must be satisfied in the world before an action can be
applied. Applying an action
"""


class Action:
    def __init__(self, action_dict):
        self.name = action_dict["name"]
        self.requires = action_dict.get("precondition", [])
        self.results = action_dict.get("satisfies", [])
        self.cost = action_dict.get("cost", 0)
        self.duration = action_dict.get("duration", 0)

    @property
    def get_duration(self):
        return self.duration

    @property
    def get_cost(self):
        return self.cost
