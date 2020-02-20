import random
import itertools
import collections
import copy

class Node:
    def __init__(self, puzzle, parent=None, action=None):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action
        if(self.parent!=None):
            self.G = parent.G + 1
        else:
            self.G = 0

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
                distance += abs(x-i) + abs(y-j)

        return distance


    def coordinate(self, val):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is val:
                    return i,j

    def shuffle(self, dir):
        p,q = self.coordinate(0)
        possibleActions = []
        if(p == 0) and (q == 0):
            possibleActions = ['D','R']
        elif(p == 0) and (q == 1):
            possibleActions = ['L','R','D']
        elif(p == 0) and (q == 2):
            possibleActions = ['D','L']
        elif (p == 1) and (q == 0):
            possibleActions = ['U','D','R']
        elif (p == 1) and (q == 1):
            possibleActions = ['U','D','R','L']
        elif (p == 1) and (q == 2):
            possibleActions = ['U','D','L']
        elif (p == 2) and (q == 0):
            possibleActions = ['R','U']
        elif (p == 2) and (q == 1):
            possibleActions = ['U','R','L']
        else:
            possibleActions = ['U','L']

        if dir =='U':
            possibleActions.remove('D')
        elif dir =='D':
            possibleActions.remove('U')
        elif dir == 'L':
            possibleActions.remove('R')
        elif dir == 'R':
            possibleActions.remove('L')

        return possibleActions

    def moves(self, direction):
        copy_array = copy.deepcopy(self)
        x,y = copy_array.coordinate(0)
        if direction == 'U':
            copy_array.board[x][y], copy_array.board[x-1][y] = copy_array.board[x-1][y], copy_array.board[x][y]
        elif direction == 'D':
            copy_array.board[x][y], copy_array.board[x+1][y] = copy_array.board[x+1][y], copy_array.board[x][y]
        elif direction == 'L':
            copy_array.board[x][y], copy_array.board[x][y-1] = copy_array.board[x][y-1], copy_array.board[x][y]
        elif direction == 'R':
            copy_array.board[x][y], copy_array.board[x][y+1] = copy_array.board[x][y+1], copy_array.board[x][y]
        return copy_array
