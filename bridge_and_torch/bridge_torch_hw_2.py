east = 1  # to change sides, multiply current side by -1
west = -1
torch = 0
a = 1  # state list will be a list of sides (east or west) in the order
b = 2  # torch, person a, person b, person c, person d
c = 3
d = 4

class Node:
    def __init__(self, state, parent, action, cost):
        self.state = state  # a state is a list of four values, each either east or west
        self.parent = parent  # this is the pointer to the previous state
        self.action = action  # what action is performed on parent to get this state
        self.cost = cost  # length of path from initial state to this one

def actionList(state):
    currentSide = state[torch]
    mylist = [[]]
    for item in [a, b, c]:
        if state[item] == currentSide:
            mylist.append([torch, item])
            for item2 in range(item + 1, d + 1):
                if state[item2] == currentSide:
                    mylist.append([torch, item, item2])
    return (mylist)

def isValid(node):
    return node.cost <= 15

def makeNewState(currentState, action):
    if action == []: return currentState
    newState = []
    return newState

def getActionCost(action):
    return max

def findAnswer():
    initial = [west, west, west, west, west]
    goal = [east, east, east, east, east]
    initialNode = Node(initial, None, None, 0)
    openNodes = [initialNode]
    exploredStates = []
    return (None)

def getItems(action):
    items = ["Torch", "Person A", "Person B", "Person C", "Person D"]
    return items[action]

def printAnswer(node):
    if node.parent != None:
        printAnswer(node.parent)
        message = " move "
        i = 0
        length = len(node.action)
        while (i < length):
            message += getItems(node.action[i])
            if i < length - 1:
                message += ", "
            i += 1
        if node.state[0] == east:
            message = message + " west to east"
        else:
            message = message + " east to west"
        print(node.action, node.state, message)
    else:  # We have recursed back to the initial state
        print(node.state, "Everyone is on the east bank.")

def main():
    finalNode, numExploredStates = findAnswer()
    printAnswer(finalNode)
    print("Number of minutes spent = ", finalNode.cost)
    print("Number of explored states = ", numExploredStates)
