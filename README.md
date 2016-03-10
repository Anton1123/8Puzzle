# 8Puzzle
Two working solution to the 8 puzzle.

---------------
TileSearch.py--
---------------
This is a breadth first search implementation of the 8-puzzle problem.
It comes with a command line user interface where the user can decide 
to input their own state or generate a random one. The data structure 
is a minHeap priority queue which orders the nodes by the path-cost 
(i.e. the number of moves it took to get to the current state from the 
initial state). 

I use a set containter to hold the nodes that have been visited already
so that we dont waste the resources when revisiting them. I check if a 
state is final before I insert it into any containers for 
optimization purposes. This solution is my fastest one even though it
is not the most efficient. 

------------------------
TileSearchManhattan.py--
------------------------
This solution is almost the same as the BFS solution but it also uses
a heuristic, called Manhattan Distance. So instead of just ordering the
states by their path-cost, it combines the ordering with this Manhattan
distance heuristic. The lower the Manhattan distance the closer the
current state is to the goal state. Through extensive testing of
various starting states, this solution takes about 2x - 5x times longer to solve and only searches about 10% less states on average. 

