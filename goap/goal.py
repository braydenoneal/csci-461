"""
gaal.py
Goals and related code for goal-oriented behavior modeling.
Created: Chris Branton, 2023-03-07.
NOTE: in general, the relation between goals and motives is not quite this
    straightforward. For example, a goal of "eat" may have a name
    of satisfying hunger. We are simplifying for clarity.
"""


class Goal:

    def __init__(self, properties):
        self.name = properties["name"]  # the "goal" of the goal
        self.requires = properties.get("precondition", None)
        self.value = properties.get("value", 1)
        self.change = properties.get("change", 0)

    def get_discontentment(self):
        return self.value * self.value

    def get_value(self):
        return self.value

    def get_change(self):
        return self.change

    def is_fulfilled(self, world_model):
        fulfilled = True
        # first, check for no prereqs
        if self.requires:
            if self.requires not in world_model.current_state:
                fulfilled = False
            elif not world_model.current_state[self.requires]:
                fulfilled = False
        return fulfilled
