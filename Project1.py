import random
import itertools
import collections
import copy


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

    @property
    def score(self):
        return (self.G + self.h)

    @property
    def state(self):
        return str(self)

    @property
    def path(self):
        node, p = self, []
        while node:
            p.append(node.puzzle.board)
            node = node.parent
        return list(reversed(p))

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


class Solver:

    def __init__(self, start):
        self.start = start

    def solve(self):
        index = 1
        queue = collections.deque([Node(self.start, index)])
        index += 1
        self.queue = collections.deque()
        self.queue.append(Node(self.start, index))
        seen = set()
        seen.add(queue[0].state)
        while queue:
            queue = collections.deque(sorted(list(queue), key=lambda node: node.score))
            node = queue.popleft()
            if node.check_solved:
                return node.path

            for move in node.puzzle.shuffle(node.action):
                child = Node(node.puzzle.moves(move), index, node, move)

                if child.state not in seen:
                    self.queue.append(Node(node.puzzle.moves(move), index, node, move))
                    index += 1
                    queue.appendleft(child)
                    seen.add(child.state)


class Puzzle:
    def __init__(self, board):

        self.board = board

    @property
    def Manhattan(self):
        goal = [[1, 2, 3],
                [4, 5, 6],
                [7, 8, 0]]

        distance = 0
        for i in range(3):
            for j in range(3):
                x, y = self.coordinate(goal[i][j])
                distance += abs(x - i) + abs(y - j)

        return distance

    def coordinate(self, val):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is val:
                    return i, j

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

        if dir == 'U':
            possibleActions.remove('D')
        elif dir == 'D':
            possibleActions.remove('U')
        elif dir == 'L':
            possibleActions.remove('R')
        elif dir == 'R':
            possibleActions.remove('L')

        return possibleActions

    def moves(self, direction):
        copy_array = copy.deepcopy(self)
        x, y = copy_array.coordinate(0)
        if direction == 'U':
            copy_array.board[x][y], copy_array.board[x - 1][y] = copy_array.board[x - 1][y], copy_array.board[x][y]
        elif direction == 'D':
            copy_array.board[x][y], copy_array.board[x + 1][y] = copy_array.board[x + 1][y], copy_array.board[x][y]
        elif direction == 'L':
            copy_array.board[x][y], copy_array.board[x][y - 1] = copy_array.board[x][y - 1], copy_array.board[x][y]
        elif direction == 'R':
            copy_array.board[x][y], copy_array.board[x][y + 1] = copy_array.board[x][y + 1], copy_array.board[x][y]
        return copy_array


def inversion(arr):
    n = len(arr)
    initial = 0
    for i in range(n):
        for j in range(i, n):
            if (arr[i] > arr[j]):
                initial += 1

    return initial


board = [[1, 3, 5], [7, 4, 0], [8, 6, 2]]

board_1 = []
for i in board:
    for j in range(len(i)):
        if i[j] != 0:
            board_1.append(i[j])

inv_c = inversion(board_1)

if inv_c % 2 == 0:
    print("Solution Exists")
    puzzle = Puzzle(board)
    solved_puzzle = Solver(puzzle)
    solved = solved_puzzle.solve()
    file1 = open("nodePath.txt", "w")
    for i in solved:
        file1.write(str(i).replace(',', '').replace('[', '').replace(']', '')+"\n")
    file1.close()
    file2 = open("Nodes.txt", "w")
    file3 = open("NodesInfo.txt", "w")
    while solved_puzzle.queue:
        node = solved_puzzle.queue.popleft()
        file2.write(str(node.puzzle.board).replace(',', '').replace('[', '').replace(']','')+"\n")
        if node.parent == None:
            file3.write(str(node.index)+" 0\n")
        else:
            file3.write(str(node.index)+" "+str(node.parent.index)+"\n")
    file2.close()
    file3.close()
else:
    print("Unsolvable case")



