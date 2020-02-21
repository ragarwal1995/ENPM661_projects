# importing the required libraries

import random
import itertools
import collections
import copy


# class node has four attributes

class Node:
    def __init__(self, puzzle, index, parent=None, action=None):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action
        self.index = index
        if (self.parent != None):
            self.G = parent.G + 1
        else:
            self.G = 0

    # calculating the score for cost function
    @property
    def score(self):
        return (self.G + self.h)

    @property
    def state(self):
        return str(self)

    # path gives us the nodes being formed and appends all the nodes in p.We reverse the list p so that we have the
    # parent node in the start followed by the child nodes.
    @property
    def path(self):
        node, p = self, []
        while node:
            p.append(node.puzzle.board)
            node = node.parent
        return list(reversed(p))

    # checking if the provided node is equivalent to the goal node
    @property
    def check_solved(self):
        goal = [[1, 2, 3],
                [4, 5, 6],
                [7, 8, 0]]
        for i in range(3):
            for j in range(3):
                if self.puzzle.board[i][j] != goal[i][j]:
                    return False
        return True

    @property
    def actions(self):
        return self.puzzle.moves

    @property
    def h(self):
        return self.puzzle.Manhattan


# class solver creates a deque to store the seen nodes and unseen nodes and appends it to the deque.
class Solver:

    def __init__(self, start):
        self.start = start

    def solve(self):
        index = 1
        # creating a deque data structure.
        queue = collections.deque([Node(self.start, index)])
        index += 1
        self.queue = collections.deque()
        self.queue.append(Node(self.start, index))
        seen = set()
        seen.add(queue[0].state)
        while queue:
            # sorting the deque and then popping the list from left to remove the node from the data structure.
            queue = collections.deque(sorted(list(queue), key=lambda node: node.score))
            node = queue.popleft()
            # checking if the obtained node is the goal node
            if node.check_solved:
                return node.path
            # checking the moves that can be done and the child nodes being created
            for move in node.puzzle.shuffle(node.action):
                child = Node(node.puzzle.moves(move), index, node, move)
                # running an if loop to check if the child node obtained is already in the deque or not. If not we will
                # append it to the queue.
                if child.state not in seen:
                    self.queue.append(Node(node.puzzle.moves(move), index, node, move))
                    index += 1
                    queue.appendleft(child)
                    seen.add(child.state)


class Puzzle:
    def __init__(self, board):

        self.board = board

    # function Manhattan is used to calculate the manhattan distance by comparing the goal node with the current node.
    # The path with least Manhattan distance is considered to be the optimal path.
    @property
    def Manhattan(self):
        goal = [[1, 2, 3],
                [4, 5, 6],
                [7, 8, 0]]

        distance = 0
        for i in range(3):
            for j in range(3):
                # Comparing value at each index of the current node with the goal node to obtain the Manhattan distance.
                x, y = self.coordinate(goal[i][j])
                # The formula used to calculate the Manhattan distance.
                distance += abs(x - i) + abs(y - j)

        return distance

    # coordinate function compares the value it get from the goal node with that in the current node and returns the
    # coordinate of the value being compared.
    def coordinate(self, val):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is val:
                    return i, j
    # This function returns a list of possible actions that can be taken based on the location of zero.
    # D stands for down.
    # U stands for up.
    # R stands for right.
    # L stands for left.
    def shuffle(self, dir):
        p, q = self.coordinate(0)
        possibleActions = []
        if (p == 0) and (q == 0):
            possibleActions = ['D', 'R']
        elif (p == 0) and (q == 1):
            possibleActions = ['L', 'R', 'D']
        elif (p == 0) and (q == 2):
            possibleActions = ['D', 'L']
        elif (p == 1) and (q == 0):
            possibleActions = ['U', 'D', 'R']
        elif (p == 1) and (q == 1):
            possibleActions = ['U', 'D', 'R', 'L']
        elif (p == 1) and (q == 2):
            possibleActions = ['U', 'D', 'L']
        elif (p == 2) and (q == 0):
            possibleActions = ['R', 'U']
        elif (p == 2) and (q == 1):
            possibleActions = ['U', 'R', 'L']
        else:
            possibleActions = ['U', 'L']
        # Here we check the moves being taken . We will remove the opposite moves because if we don't do that we will
        # end up getting the node where we started from.
        if dir == 'U':
            possibleActions.remove('D')
        elif dir == 'D':
            possibleActions.remove('U')
        elif dir == 'L':
            possibleActions.remove('R')
        elif dir == 'R':
            possibleActions.remove('L')

        return possibleActions
        # Based on the possible actions that can be taken we now need to swap the values in the two indices.
        # This function swaps the two values.
    def moves(self, direction):
        # creating a deep copy of the board
        copy_array = copy.deepcopy(self)
        # Determining the coordinates of zero in board.
        x, y = copy_array.coordinate(0)
        # if the possible moves is up we will swap the value in that index with the value in the index above it.
        if direction == 'U':
            copy_array.board[x][y], copy_array.board[x - 1][y] = copy_array.board[x - 1][y], copy_array.board[x][y]
        # if the possible moves is down we will swap the value in that index with the value in the index below it.
        elif direction == 'D':
            copy_array.board[x][y], copy_array.board[x + 1][y] = copy_array.board[x + 1][y], copy_array.board[x][y]
        # if the possible moves is left we will swap the value in that index with the value in the index left of it.
        elif direction == 'L':
            copy_array.board[x][y], copy_array.board[x][y - 1] = copy_array.board[x][y - 1], copy_array.board[x][y]
        # if the possible moves is right we will swap the value in that index with the value in the index right of it.
        elif direction == 'R':
            copy_array.board[x][y], copy_array.board[x][y + 1] = copy_array.board[x][y + 1], copy_array.board[x][y]
        return copy_array

# This function calculates the number of inversions for the given board.
def inversion(arr):
    n = len(arr)
    initial = 0
    for i in range(n):
        for j in range(i, n):
            if (arr[i] > arr[j]):
                initial += 1

    return initial

# Initial set of matrix given to the algorithm. The values at each index can be changed as desired by the user.
board = [[1, 3, 5], [7, 4, 0], [8, 6, 2]]

# For checking inversion we remove zero from the list of numbers and create a new list from 1 to 8.
board_1 = []
for i in board:
    for j in range(len(i)):
        if i[j] != 0:
            board_1.append(i[j])

inv_c = inversion(board_1)
# We use the if statement to check if the number of inversions are odd or even.
# If the number of inversions are even then the case is solvable else the case is unsolvable.
if inv_c % 2 == 0:
    # if the number of inversions are even the case is solvable and we pass the board to Puzzle.
    print("Solution Exists")
    puzzle = Puzzle(board)
    # The attributes are then passed to Solver
    solved_puzzle = Solver(puzzle)
    # Obtaining the list of nodes
    solved = solved_puzzle.solve()
    # Creating a file nodePath to show the path created.
    file1 = open("nodePath.txt", "w")
    for i in solved:
        tlist = list(zip(*i))
        file1.write(str(tlist).replace('(','').replace(')','').replace(',', '').replace('[', '').replace(']', '') + "\n")
    file1.close()
    # Creating two more files to create Nodes and NodeInfo
    file2 = open("Nodes.txt", "w")
    file3 = open("NodesInfo.txt", "w")
    while solved_puzzle.queue:
        node = solved_puzzle.queue.popleft()
        tlist = list(zip(*node.puzzle.board))
        file2.write(str(tlist).replace('(','').replace(')','').replace(',', '').replace('[', '').replace(']', '') + "\n")
        if node.parent == None:
            file3.write(str(node.index) + " 0\n")
        else:
            file3.write(str(node.index) + " " + str(node.parent.index) + "\n")
    file2.close()
    file3.close()
    # If number of inversions are odd the given case is unsolvable and we will exit the program.
else:
    print("Unsolvable case")
