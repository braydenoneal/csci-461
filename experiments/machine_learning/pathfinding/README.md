# Pathfinding with a Neural Network

The goal of this experiment is to test whether a neural network can be used as an alternative to pathfinding algorithms
such as A*.

An A* maze solver was used to train a linear neural network. Each step of the A* algorithm was encoded into an image and
combined into one large image with the rest of the pathfinding process on one random maze.

This process was largely ineffective using a standard linear neural network. The primary issue is likely that the number
of available actions that can be taken at each step is variable. The neural network likely does not generalize very well
either.

Further research would need to be done on different types of neural networks and finding a way to generalize the
pathfinding problem.
