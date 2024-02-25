# Genetic Algorithm for Traveling Salesman Problem

## Demonstration

![traveling_salesman.gif](traveling_salesman.gif)

## Notes

This shows only 25 out of the 1000 chromosomes in the population of each generation.

The optimal distance is typically found in two to three seconds.

A large language model was not used to generate any part of this solution.

The genetic algorithm can occasionally get stuck with a population with a path similar to the following:

![stuck_path.png](stuck_path.png)

It is possible, though extremely rare, for a mutation to change every gene in a chromosome, so it should be possible for
a population to escape the above path and find the optimal distance, given enough time.

## Code

With graphics: [traveling_salesman_genetic_algorithm_graphical.py](traveling_salesman_genetic_algorithm_graphical.py)

Without graphics: [traveling_salesman_genetic_algorithm.py](traveling_salesman_genetic_algorithm.py)
