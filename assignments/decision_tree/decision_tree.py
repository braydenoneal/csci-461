from __future__ import annotations
import copy
import math


class DecisionNode:
    def __init__(self):
        self.test_value: any = None
        self.child_nodes: list[DecisionNode or None] = []


class DecisionTree:
    def __init__(self):
        self.root: DecisionNode = DecisionNode()

    def train(self, training_set, attributes):
        self.make_tree(training_set, attributes, self.root)

    # TODO: implement
    @staticmethod
    def test(test_set):
        print(test_set)

    # Recursively build the tree based on maximum information gain
    def make_tree(self, examples: list[dict], attributes, decision_node):
        # Calculate initial entropy
        new_examples = []

        for example in examples:
            new_examples.append(list(example.values()))

        examples = new_examples

        initial_entropy = entropy(examples)

        # If entropy is 0, nothing else to do
        if initial_entropy > 0:
            example_count = len(examples)

            # Keep the best result
            best_information_gain = 0
            best_split_attribute = None
            best_sets: list[any] = []

            # Calculate information gain for each attribute
            for attribute in attributes:
                sets = split_by_attribute(examples, attribute)
                overall_entropy = entropy_of_sets(sets, example_count)
                information_gain = initial_entropy - overall_entropy

                # If this one is better, keep it
                if information_gain > best_information_gain:
                    best_information_gain = information_gain
                    best_split_attribute = attribute
                    best_sets = sets

            # Set the decision node to this attribute
            decision_node.test_value = best_split_attribute

            # Remove the best attribute from the set we will pass down the tree
            new_attributes = copy.deepcopy(attributes)
            new_attributes -= best_split_attribute

            for best_set in best_sets:
                new_decision_node = DecisionNode()
                decision_node.child_nodes.append(new_decision_node)
                self.make_tree(best_set, new_attributes, new_decision_node)


# Calculate the information entropy of an example set
def entropy(example_sets):
    entropy = 0
    all_values = []

    for example_set in example_sets:
        for example in example_set:
            all_values.append(example)

    unique_values = []

    for value in all_values:
        if value not in unique_values:
            unique_values.append(value)
            proportion = all_values.count(value) / len(all_values)
            entropy -= proportion * math.log2(proportion)

    return entropy


# Divide a set of examples based on an attribute value
def split_by_attribute(examples, value) -> list[any]:
    splits = [[], []]

    for example in examples:
        if type(example) is list:
            for example_value in example:
                if type(example_value) is str:
                    splits[example_value > value].append(example)
                else:
                    splits[0].append(example_value)
        elif type(example) is str:
            splits[example > value].append(example)
        else:
            splits[0].append(example)

    return splits


# Find the entropy of a list of sets
def entropy_of_sets(example_sets, count):
    overall_entropy = 0

    for example_set in example_sets:
        overall_entropy += entropy(example_set)

    return overall_entropy / count
