import copy
from enum import Enum, auto


class Position(Enum):
    START = auto()
    END = auto()


def swap_position(position: Position) -> Position:
    return Position.START if position == Position.END else Position.END


class Person:
    def __init__(self, time: int):
        self.time: int = time
        self.position: Position = Position.START

    def swap_position(self):
        self.position = Position.START if self.position == Position.END else Position.END


class Action:
    def __init__(self, person_indices: list[int]):
        self.person_indices: list[int] = person_indices


class Scenario:
    def __init__(self):
        self.torch_position: Position = Position.START
        self.persons: list[Person] = [Person(1), Person(2), Person(5), Person(8)]
        self.time_elapsed = 0

    def can_person_cross(self, person: Person) -> bool:
        return self.torch_position == person.position

    def get_available_actions(self) -> list[Action]:
        actions: list[Action] = []
        checked_indices = []

        for index, person in enumerate(self.persons):
            checked_indices.append(index)

            if self.can_person_cross(person):
                actions.append(Action([index]))

                for second_index, second_person in enumerate(self.persons):
                    if second_index not in checked_indices and self.can_person_cross(second_person):
                        actions.append(Action([index, second_index]))

        return actions

    def is_complete(self) -> bool:
        return False not in [person.position == Position.END for person in self.persons]

    def perform_action(self, action: Action) -> None:
        self.torch_position = swap_position(self.torch_position)

        for index in action.person_indices:
            self.persons[index].swap_position()

    def check_equality(self, scenario):
        return self.torch_position == scenario.torch_position and False not in [self.persons[index].position == scenario.persons[index].position for index in range(len(self.persons))]


class Node:
    def __init__(self, scenario: Scenario, parent, all_nodes: list):
        self.scenario = scenario
        self.parent = parent
        self.all_nodes = all_nodes

        print(f'Torch: {self.scenario.torch_position}')

        for person in self.scenario.persons:
            print(person.position)

    def propagate(self):
        for action in self.scenario.get_available_actions():
            new_scenario: Scenario = copy.deepcopy(self.scenario)
            new_scenario.perform_action(action)

            if not new_scenario.is_complete() and True not in [new_scenario.check_equality(node.scenario) for node in self.all_nodes]:
                new_all_nodes = copy.deepcopy(self.all_nodes)
                new_node: Node = Node(new_scenario, self, new_all_nodes)
                new_all_nodes.append(new_node)
                new_node.propagate()


node = Node(Scenario(), None, [])
node.propagate()
