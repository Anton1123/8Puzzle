#A* search description (Best-First) https://www.cs.princeton.edu/courses/archive/fall12/cos226/assignments/8puzzle.html

# this class will act as our node
# it will have 4 componenets
# 1. STATE : the state in the state space to which the node corresponds;
# 2. PARENT : the node in the search tree that generated this node;
# 3. ACTION : the action that was applied to the parent to generate the node;
# 4. PATH_COST : the cost, traditionally denoted by g(n), of the path from the initial state
#    to the node, as indicated by the parent pointers.

import random
import time
from heapq import heappush, heappop

class State(object):
    def __init__(self, state = None, parent = None, action = None, path_cost = 0): #state is the array of tile integers
        if not state:
            state = []
        self.state = state
        if not parent:
             parent = []
        self.parent = parent
        if not action:
            action = ""
        self.action = action #the action to the parent that got it to this state
        if not path_cost:
            path_cost = 0
        self.path_cost = path_cost

        self.goal = range(1,9)
        self.goal.append(0)

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))

    def __lt__(self, other):
        return self.path_cost < other.path_cost


    # def score(self):
    #     return self._h() + self._g()
    #
    # def _h(self):
    #     return sum([1 if self.state[i] != self.goal[i] else 0 for i in xrange(8)])
    #
    # def _g(self):
    #     return self.path_cost
    #
    # def __cmp__(self, other):
    #     return self.state == other.state
    #
    # def __eq__(self, other):
    #     return self.__cmp__(other)
    #
    # def __hash__(self):
    #     return hash(str(self.state))
    #
    # def __lt__(self, other):
    #     return self.score() > other.score()



    #Nice display of puzzle. Could imporve display with padding (when dealing with 4X4 size and up)
    def displayTile(self):
        length = int(len(self.state) ** 0.5)
        i = 0
        while i < len(self.state) - length + 1:
            for j in range(length):
                print self.state[i+j],
            print
            i += length
        print
        return

     #a puzzle is solvable if it has a even number of inversions
    def solvable(self):
        inverses = 0
        for number in range(0, len(self.state) - 1):
            if self.state[number] == 0:
                continue
            for current in range (number, len(self.state)):
                if self.state[current] == 0:
                    continue
                if self.state[number] > self.state[current]:
                    inverses += 1
        if inverses % 2 == 0:
            #print "Puzzle is solvable"
            #print
            return True
        else:
            #print "Puzzle is not solvable. Exiting."
            #print
            return False


    #checks if current state is a goal state
    def checkState(self):
        goal = []
        for i in range(1, len(self.state)):
            goal.append(i)
        goal.append(0)
        if self.state == goal:
            print "Reached the goal state."
            return True
        return False

    #The following function yields all the possible states after going left/up/right/down
    #in my movements, I am concerned about moving the blank space to a certain position, not the piece that it is touching for my error checking
    def getPossibleMoves(self, moves):
        index = self.state.index(0) #finding where the blank piece is located
        length = int(len(self.state) ** 0.5) #saving the length of the square tile (e.g. Upper Right corner will be at index length - 1)

        #moving left (The direction that I put higher up is likely the one that the program choses next)
        if index % length != 0: #checking if we can move left
            new_state = self.state[:] #is the [:] necessary here?
            new_state[index], new_state[index - 1] = new_state[index - 1], new_state[index]
            yield State(new_state, self, "l", moves)

        #moving up
        if index > length - 1:
            new_state = self.state[:] #is the [:] necessary here?
            new_state[index], new_state[index - length] = new_state[index - length], new_state[index]
            yield State(new_state, self, "u", moves)

        #moving right
        if index % length < length - 1: #blank tile cant on the right-most column
            new_state = self.state[:] #is the [:] necessary here?
            new_state[index], new_state[index + 1] = new_state[index + 1], new_state[index]
            yield State(new_state, self, "r", moves)

        #moving down
        if index < len(self.state) - length: #blank tile cant be on the bottom row
            new_state = self.state[:] #is the [:] necessary here?
            new_state[index], new_state[index + length] = new_state[index + length], new_state[index]
            yield State(new_state, self, "d", moves)


#the container for our solution
class minHeap(object):

    def __init__(self):
        self.heap = []

    def __len__(self):
        return len(self.heap)

    def add(self, item):
        heappush(self.heap, item)

    def poll(self):
        return heappop(self.heap)

    def peek(self):
        return self.heap[0]


class SolvingAgent(object):

    def __init__(self, start_state = None):
        if not start_state:
            start_state = []
        self.start_state = State(start_state)

    def get_parentStates(self, latest): #returns all the parent states in reverse order
        our_solution = [latest]
        state = latest.parent
        while state.parent:
            our_solution.append(state)
            state = state.parent
        return our_solution

    def solve(self):
        our_set = minHeap()
        our_set.add(self.start_state)
        used_set = set() #will hold the states we already visited so to not visit them again
        moves = 0
        puzzle = our_set.peek()
        print "Your puzzle is:"
        puzzle.displayTile()
        if not puzzle.solvable(): #check if puzzle is solvable here
            return

        letter_solution = ""
        explored_states = 0
        start = time.time()
        while our_set:
            current_state = our_set.poll()

            if current_state.checkState(): #if current state is final state
                end = time.time()
                if moves != 0: #just to make sure that we werent given a puzzle that is already a solution
                    path = self.get_parentStates(current_state)
                    for state in reversed(path):
                        print state.action
                        letter_solution += state.action
                        state.displayTile()
                    print "The solving agent took %d moves." % len(path)
                    print "The puzzle took %2.f seconds to solve." % float(end - start)
                    print "Explored %d states." % explored_states
                    print "The letter solution is %s" % letter_solution
                else:
                    print "Puzzle already a solution"
                return

            for state in current_state.getPossibleMoves(moves):
                if state not in used_set:
                    our_set.add(state)
                    explored_states += 1
            used_set.add(current_state)
            moves += 1
            #print moves


board = [1, 7, 4, 6, 8, 3, 2, 5, 0] #24 moves 5 seconds
#board = [11,12,13,14,15,6,7,8,9,0,1,2,3,4,5,10] #interrupted the process afer 2 min (computer started freezing up)
#board = [1,2,3,4,5,6,7,8,9,10,15,14,13,12,11,0] #14 moves 1 second
#board = [1,2,3,4,5,6,7,8,9,10,15,14,13,12,11,0] #14 moves 1 second
#board = [1,2,3,4,5,6,7,9,8,15,10,14,13,12,11,0] # interrupted
solver = SolvingAgent(board)
solver.solve()



"""
#initializes the state of the tile
#creates a size^2 state that will represent the tile sliding state
#0 depicts empty location
def initializeState(size):
    state = random.sample(range(0,size**2), size**2) #generates a random state of ints. No duplicates!
    print state

def getUserInput():
    pass

def getInput():
    selection = 0
    initState = []
    while selection != 1 and selection != 2:
        print "Type 1 and hit Enter to input your own initial state."
        print "Or Type 2 and hit Enter for a random initial state."
        print "Selection: "
        initState = raw_input("Enter the desired initial state of the tile-sliding domain problem: ")

    print("You entered: ", initState)

initializeState(3)
"""
