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
    def __init__(self, state = None, parent = None, action = None, path_cost = None): #state is the array of tile integers
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

    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return self.path_cost < other.path_cost

    def __hash__(self):
        return hash(str(self.state))

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
            return True
        else:
            print "Puzzle is not solvable. Exiting."
            return False


    #checks if current state is a goal state
    def checkState(self):
        goal = []
        for i in range(1, len(self.state)):
            goal.append(i)
        goal.append(0)
        if self.state == goal:
            return True
        return False

    #The following function yields all the possible states after going left/up/right/down
    #in my movements, I am concerned about moving the blank space to a certain position, not the piece that it is touching for my error checking
    def getPossibleMoves(self, moves):
        index = self.state.index(0) #finding where the blank piece is located
        length = int(len(self.state) ** 0.5) #saving the length of the square tile (e.g. Upper Right corner will be at index length - 1)

        #moving left (The direction that I put higher up is likely the one that the program choses next)
        if index % length != 0: #checking if we can move left (e.g. blank tile cant be on the left-most column)
            new_state = self.state[:]
            new_state[index], new_state[index - 1] = new_state[index - 1], new_state[index]
            yield State(new_state, self, "l", moves)

        #moving up
        if index > length - 1: #blank tile cant be on the top row
            new_state = self.state[:]
            new_state[index], new_state[index - length] = new_state[index - length], new_state[index]
            yield State(new_state, self, "u", moves)

        #moving right
        if index % length < length - 1: #blank tile cant on the right-most column
            new_state = self.state[:]
            new_state[index], new_state[index + 1] = new_state[index + 1], new_state[index]
            yield State(new_state, self, "r", moves)

        #moving down
        if index < len(self.state) - length: #blank tile cant be on the bottom row
            new_state = self.state[:]
            new_state[index], new_state[index + length] = new_state[index + length], new_state[index]
            yield State(new_state, self, "d", moves)


#the container for our solution
class minHeap(object):

    def __init__(self):
        self.heap = []

    def add(self, item):
        heappush(self.heap, item)

    def poll(self):
        return heappop(self.heap)

    def __len__(self):
        return len(self.heap)

#The solving agent/algorithm of the 8-Puzzle problem
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
        puzzle = our_set.heap[0]
        print "Your puzzle is:"
        puzzle.displayTile()
        if not puzzle.solvable(): #check if puzzle is solvable here
            return
        if puzzle.checkState(): #check if puzzle is already a solution
            print "Puzzle already a solution"
            return
        letter_solution = ""
        explored_states = 0
        start = time.time()
        while our_set:
            current_state = our_set.poll()
            for state in current_state.getPossibleMoves(moves):
                if state not in used_set:
                    if state.checkState(): #if current state is final state
                        end = time.time()
                        path = self.get_parentStates(state)
                        for state in reversed(path):
                            print state.action
                            letter_solution += state.action
                            state.displayTile()
                        print "The solving agent took %d moves." % len(path)
                        print "The puzzle took %0.2f seconds to solve." % float(end - start)
                        print "Explored %d states." % explored_states
                        print "The size of the explored set %d" % len(our_set)
                        print "The size of the closed set %d" % len(used_set)
                        print "The letter solution is %s\n" % letter_solution
                        return
                    our_set.add(state)
                    explored_states += 1
            used_set.add(current_state)
            moves += 1

#board = [1,2,3,4,5,6,7,8,0]
#board = [1, 7, 4, 6, 8, 3, 2, 5, 0] #24 moves 4 seconds
#board = [11,12,13,14,15,6,7,8,9,0,1,2,3,4,5,10] #interrupted the process afer 2 min (computer started freezing up)
#board = [1,2,3,4,5,6,7,8,9,10,15,14,13,12,11,0] #14 moves 1 second
#board = [1,2,3,4,5,6,7,8,9,10,15,14,13,12,11,0] #14 moves 1 second
#board = [1,2,3,4,5,6,7,9,8,15,10,14,13,12,11,0] # interrupted
#solver = SolvingAgent(board)
#solver.solve()



def main():
    initState = []
    while(True):
        selection = 0
        print "*Enter the size of your puzzle or type 'x' and hit Enter to exit"
        size = raw_input("*E.g. Type 8 and hit Enter for an 8-Puzzle or 15 and hit Enter for a 15-Puzzle\n")
        if size == 'x' or size == 'X':
            print "Exiting"
            return
        while size != '8' and size != '15':
            size = raw_input("Enter an 8 or 15 only\n")
        size = int(size)
        size += 1
        while selection != '1' and selection != '2':
            print "*Type 1 and hit Enter to input your own initial state."
            print "*Type 2 and hit Enter for a random initial state."
            selection = raw_input("Your selection:\n")
            if selection == '1':
                print "Enter the desired initial state of the tile-sliding domain problem as a string with no spaces."
                initState = raw_input("E.g. 174683250\n")
                while len(initState) != size:
                    initState = raw_input("Incorrect length. Try again.\n")
                initState = [int(i) for i in initState] #converting the input string to a list of integers
            elif selection == '2':
                initState = random.sample(range(0,size), size) #generates a random state of ints. No duplicates!
        print "The initial state is: ", initState
        solver = SolvingAgent(initState)
        solver.solve()

if __name__ == "__main__":
    main()
