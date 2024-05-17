# GOAP Project Part 2

2. Make another enhancement. This could be adding times to the actions, changing the value of the goal, selecting actions first rather than goals, implementing actions using the Agent class you have built, or something else.

The previous searching method chose an action sequence based on the action with the lowest cost at each iteration.

The searching method has been modified to find the action sequence with the lowest total cost among all possible action 
sequences below a certain action sequence length.

The following data class was created in `planner.py` to represent a single action sequence.

```python
@dataclass
class Sequence:
    model: WorldModel
    actions: list
    complete: bool
    depth: int
    cost: int
```

The following method was created in `planner.py` to return all valid action sequences below a given maximum length.

```python
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
```

The following method was created in `worldmodel.py` to return all the valid actions of a world model.

```python
# get all available actions
def get_available_actions(self) -> list[Action]:
    valid_actions: list[Action] = []

    for action in self.action_list:
        preconditions_met_quantity = 0

        for precondition in action.requires:
            if precondition in self.current_state:
                preconditions_met_quantity += 1

        if preconditions_met_quantity >= len(action.requires):
            valid_actions.append(action)

    return valid_actions
```

With a maximum action sequence length of 4, the best plan was found to be:

```
goto_node
goto_target
melee_attack
```

with a total cost of 2, instead of part 1's:

```
goto_target
goto_node
idle
get_axe
melee_attack
```

with a total cost of 5, and the starter code's:

```
get_axe
chop_log
collect_branches
melee_attack
```

with a total cost of 16.
