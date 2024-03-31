"""
Planning component for goal-oriented AI modeling.
Created: Chris Branton, 2023-03-07.
Adapted from a technique presented in AI for Games, 3rd Edition, by Ian Millington
NOTE: in AI literature, discontent is often called "energy metric"
ALSO NOTE: We are combining the planner and AI agent. This is not usually desirable.
"""
import action
import copy
from dataclasses import dataclass

from worldmodel import WorldModel

no_action = action.Action({"name": "No action", "cost": 1})


@dataclass
class Sequence:
    model: WorldModel
    actions: list
    complete: bool
    depth: int
    cost: int


class Planner:
    def __init__(self, world_model):
        self.model = world_model

    def run(self):
        for iteration in range(1):
            # Limit the depth to the number of possible actions.
            action_plan = self.plan_action(self.model, 4)
            if action_plan:
                print("Best plan is")
                for a in action_plan:
                    if a:
                        print(f'{a.name} {a.cost}')
            else:
                print("No plan found")
            print()

    # This method is intentionally small to facilitate different
    # search methods
    def plan_action(self, model, max_depth=4):
        current_goal = self.choose_goal()

        # get all viable action sequences
        sequences = self.optimal_search(model, current_goal, max_depth)
        # sort viable action sequences by their cost
        sequences = sorted(sequences, key=lambda x: x.cost)

        # if we have an action, return the one with the lowest cost
        return sequences[0].actions

    # Find all viable action sequences with a depth limit
    @staticmethod
    def optimal_search(model, current_goal, max_depth) -> list[Sequence]:
        sequences: list[Sequence] = [Sequence(model, [], False, 0, 0)]

        all_complete = False

        while not all_complete:
            all_complete = True

            for sequence in sequences:
                if sequence.depth >= max_depth:
                    sequences.remove(sequence)
                    sequence.complete = True

                if current_goal.is_fulfilled(sequence.model):
                    sequence.complete = True

                if not sequence.complete:
                    all_complete = False

                    for action in sequence.model.get_available_actions():
                        new_sequence = copy.deepcopy(sequence)
                        new_sequence.actions.append(action)
                        new_sequence.model.apply_action(action)
                        new_sequence.depth += 1
                        new_sequence.cost += action.get_cost

                        sequences.append(new_sequence)

                    sequences.remove(sequence)

        return sequences

    # Chooses a goal to pursue based on
    def choose_goal(self):
        # check for empty list
        if not self.model.goal_list:
            return None
        top_goal = self.model.goal_list[0]
        for candidate in self.model.goal_list[1:]:
            if candidate.get_value() > top_goal.get_value():
                top_goal = candidate
        return top_goal
