import copy


# helper class for decision tree nodes
class DecisionNode:
    def __init__(self):
        self.test_value = None
        self.child_nodes = []


# class implementing an ID3 decision tree
class DecisionTree:
    def __init__(self):
        self.root = DecisionNode()

    # TODO: implement
    def train(self, training_set, attributes):
        print("Training...")

        # Indirection allows us to shield caller from DecisionNode details
        self.make_tree(training_set, attributes, self.root)

    # TODO: implement
    def test(self, test_set):
        print("Testing...")

    # Recursively build the tree based on maximum information gain
    def make_tree(self, examples, attributes, decision_node):
        # Calculate initial entropy
        initial_entropy = self.entropy(examples)

        # if entropy is 0, nothing else to do
        # let's talk about single points of entry and exit in class
        if initial_entropy > 0.0:
            example_count = len(examples)

            # keep the best result
            best_information_gain = 0
            best_split_attribute = None
            best_sets = None

            # calculate information gain for each attribute
            for attr in attributes:
                sets = self.split_by_attribute(examples, attr)
                overall_entropy = self.entropy_of_sets(sets, example_count)
                information_gain = initial_entropy - overall_entropy

                # if this one is better, keep it
                if information_gain > best_information_gain:
                    best_information_gain = information_gain
                    best_split_attribute = attr
                    best_sets = sets

            # set the decision node to this attribute
            decision_node.test_value = best_split_attribute

            # remove the best attribute from the set we will pass down the tree
            new_attributes = copy.deepcopy(attributes)
            new_attributes -= best_split_attribute

            # TODO: create the child nodes
            for set in best_sets:
                print("Create child node for set " + set)

    # Calculate the information entropy of an example set
    # TODO: implement
    def entropy(self, examples):
        return 0

    # Divide a set of examples based on an attribute value
    # TODO: implement
    def split_by_attribute(self, examples, attribute):
        print("Splitting on " + attribute)

    # Find the entropy of a list of sets
    # TODO: implement
    def entropy_of_sets(self, sets, count):
        return 0
