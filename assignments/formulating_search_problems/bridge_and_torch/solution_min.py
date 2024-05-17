times = [1, 2, 5, 8]
complete_nodes = []


class Node:
    def __init__(self, torch: bool, persons: list[bool], time_elapsed: int, parent):
        self.torch = torch
        self.persons = persons
        self.time_elapsed = time_elapsed
        self.parent = parent

    def propagate(self):
        actions = []
        checked_indices = []
        for index, person in enumerate(self.persons):
            checked_indices.append(index)
            if person == self.torch:
                actions.append([index])
                for second_index, second_person in enumerate(self.persons):
                    if second_index not in checked_indices and second_person == self.torch:
                        actions.append([index, second_index])
        for action in actions:
            new_node = Node(self.torch, self.persons.copy(), self.time_elapsed, self)
            new_node.torch = not new_node.torch
            for index in action:
                new_node.persons[index] = not new_node.persons[index]
            new_node.time_elapsed += max([times[index] for index in action])
            if False not in new_node.persons:
                complete_nodes.append(new_node)
            elif not is_repeat(new_node, new_node.parent):
                new_node.propagate()


def is_repeat(initial_node: Node, parent: Node) -> bool:
    if parent is None: return False
    if initial_node.torch == parent.torch and initial_node.persons == parent.persons: return True
    return is_repeat(initial_node, parent.parent)


first_node = Node(False, [False, False, False, False], 0, None)
first_node.propagate()
for complete_node in complete_nodes:
    if complete_node.time_elapsed <= 15:
        path = [complete_node]
        while complete_node.parent is not None:
            complete_node = complete_node.parent
            path.insert(0, complete_node)
        print('Time  |  Start      |  End\n------+-------------+------------')
        for node in path:
            print(f'{node.time_elapsed:>4}  |  {" " if node.torch else "T"} {" " if node.persons[0] else "A"} '
                  f'{" " if node.persons[1] else "B"} {" " if node.persons[2] else "C"} '
                  f'{" " if node.persons[3] else "D"}  |  {"T" if node.torch else " "} '
                  f'{"A" if node.persons[0] else " "} {"B" if node.persons[1] else " "} '
                  f'{"C" if node.persons[2] else " "} {"D" if node.persons[3] else " "}')
        print(f'\nActions taken: {len(path) - 1}\n')
