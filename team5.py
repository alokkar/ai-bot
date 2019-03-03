import sys
import random
import signal
import time
import copy

class Team5:
    def __init__(self):
        self.flag = 1
        self.next_move = (0 , 0, 0)
        self.maxdepth = 4

    def returnValEval(self, arr):
        # arr[0] => 'x' ... arr[1] => 'o' ... arr[2] => 'd' ... arr[3] => '-'
        heuristic = 0
        if(arr[0] == 3 and arr[3] == 0 and arr[1] == 0):
            heuristic = 1024
        if(arr[1] == 3 and arr[3] == 0 and arr[0] == 0):
            heuristic = -1024

        if(arr[0] == 2 and arr[3] == 1 and arr[1] == 0):
            heuristic = 256
        if(arr[1] == 2 and arr[3] == 1 and arr[0] == 0):
            heuristic = -256

        if(arr[0] == 1 and arr[3] == 2 and arr[1] == 0):
            heuristic = 32
        if(arr[1] == 1 and arr[3] == 2 and arr[0] == 0):
            heuristic = -32

        if(arr[0] == 0 and arr[3] == 3 and arr[1] == 0):
            heuristic = 8
        if(arr[1] == 0 and arr[3] == 3 and arr[0] == 0):
            heuristic = -8

        if(arr[0] == 1 and arr[1] == 2):
            heuristic = 512
        if(arr[1] == 1 and arr[0] == 2):
            heuristic = -512

        return heuristic

    def returnCount(self, cell, arr):
        if cell == 'x':
            arr[0] += 1
        if cell == 'o':
            arr[1] += 1
        if cell == 'd':
            arr[2] += 1
        if cell == '-':
            arr[3] += 1
        return arr

    def checkRows(self, array):
        val = 0
        for i in range(3):
            arr = [0, 0, 0, 0]
            for j in range(3):
                arr = self.returnCount(array[i][j], arr)
            val += self.returnValEval(arr)
        return val

    def checkColumns(self, array):
        val = 0
        for j in range(3):
            arr = [0, 0, 0, 0]
            for i in range(3):
                arr = self.returnCount(array[i][j], arr)
            val += self.returnValEval(arr)
        return val
 
    def checkDiagonal(self, array):
        val = 0
        arr=[0,0,0,0]
        arr = self.returnCount(array[0][0],arr)
        arr = self.returnCount(array[1][1],arr)
        arr = self.returnCount(array[2][2],arr)
        val+=self.returnValEval(arr)
        arr=[0,0,0,0]
        arr = self.returnCount(array[0][2],arr)
        arr = self.returnCount(array[1][1],arr)
        arr = self.returnCount(array[2][0],arr)
        val+=self.returnValEval(arr)
        return val

    def localheuristic(self, board):
        localheuristic = [0,0];
        for k in range(2):
            for i in range(0, 9, 3):
                for j in range(0, 9, 3):
                    arr = []
                    for x in range(3):
                        temp = []
                        for y in range(3):
                            temp.append(board.big_boards_status[k][i + x][j + y])
                        arr.append(list(temp))
                        # print(len(arr))
                    localheuristic[k] += self.checkRows(arr) + self.checkColumns(arr) + self.checkDiagonal(arr)
        if(localheuristic[0]>localheuristic[1]):
	        return 1.05*localheuristic[0]+localheuristic[1]
        if(localheuristic[1]>localheuristic[0]):
	        return localheuristic[0]+1.05*localheuristic[1]
        if(localheuristic[0]==localheuristic[1]):
	        return localheuristic[0]+localheuristic[1]

    def weightedEval(self, board):
        weight = [[8, 6, 8], [6, 4, 6], [8, 6, 8]]
        val = 0
        for k in range(2):
            for i in range(3):
                for j in range(3):
                    if board.small_boards_status[k][i][j] == 'x':
                        val += 100 * weight[i][j]
                    if board.small_boards_status[k][i][j] == 'o':
                        val += -100 * weight[i][j]
        return val

    def weighted(self, board,i,j,k):
        weight = [[8, 6, 8], [6, 4, 6], [8, 6, 8]]
        val = 0
        for x in range(3):
            for y in range(3):
                if board.big_boards_status[k][i+x][j+y] == 'x':
                    val += 50 * weight[i][j]
                if board.big_boards_status[k][i+x][j+y] == 'o':
                    val += -50 * weight[i][j]
        return val

    def evaluation(self, board, old_move):
        heuristicboard = 0
        heuristicboard1 = 0
        heuristicweighted = 0
        heuristiclocal = 0
        # Calculating larger board heuristic
        heuristicboard += self.checkRows(board.small_boards_status[0]) + self.checkColumns(board.small_boards_status[0]) + self.checkDiagonal(board.small_boards_status[0])
        heuristicboard += self.checkRows(board.small_boards_status[1]) + self.checkColumns(board.small_boards_status[1]) + self.checkDiagonal(board.small_boards_status[1])
        heuristiclocal = self.localheuristic(board)

        heuristicboard1 += self.weighted(board,old_move[1]/3,old_move[2]/3,old_move[0])
        heuristicweighted = self.weightedEval(board)

        # print(heuristicboard1)
        # print(heuristicboard)
        # print(heuristicweighted)
        # print(heuristiclocal)

        return 9*heuristicboard + heuristiclocal + heuristicweighted + heuristicboard1

    def flagtonum(self, flag):
        if flag == 'x':
            return 1
        else:
            return 0

    def numtoflag(self, num):
        if num == 1:
            return 'x'
        else:
            return 'o'

    def move(self, board, old_move, flag):
        self.flag = self.flagtonum(flag)
        self.time = time.time()
        curr_board = copy.deepcopy(board);
        val = self.minimax(curr_board, old_move, 0, -999999999, 999999999, self.numtoflag(self.flag))
        print(val)
        return (self.next_move[0], self.next_move[1],self.next_move[2])

    def checkend(self, board, old_move, depth):
        check = board.find_terminal_state()
        if depth == self.maxdepth or check[0] != 'CONTINUE':
            return (1, (self.flag + (self.flag - 1)) * self.evaluation(board, old_move))
        else:
            return (0, 0)

    def minimax(self, board, old_move, depth, alpha, beta, flag):
        ifend = self.checkend(board, old_move, depth)
        if ifend[0] == 1:
            return ifend[1]
        Player = self.flagtonum(flag);
        value = Player * -999999999 + (1 - Player) * 999999999
        possibilities = board.find_valid_move_cells(old_move)
        random.shuffle(possibilities)

        for move in possibilities:
            board.update(old_move, move, flag)
            nextp = 1 - Player
            # if board.big_boards_status[move[0]][move[1]][move[2]] == flag and board.small_boards_status[move[0]][move[1] / 3][move[2] / 3] == flag:
            #     nextp = Player
            # if board.big_boards_status[old_move[0]][old_move[1]][old_move[2]] != flag and board.small_boards_status[move[0]][move[1] / 3][move[2] / 3] == flag:
            #     nextp = Player
            #     flag = self.numtoflag(1 - self.flagtonum(flag))
            child = self.minimax(board, move, depth + 1, alpha, beta, self.numtoflag(1 - self.flagtonum(flag)))
            board.big_boards_status[move[0]][move[1]][move[2]] = '-'
            board.small_boards_status[move[0]][move[1] / 3][move[2] / 3] = '-'
            if Player:
                if child > value:
                    value = child
                    if depth == 0:
                        self.next_move = copy.deepcopy(move)
                alpha = max(alpha, value)
            else:
                if child < value:
                    value = child
                    if depth == 0:
                        self.next_move = copy.deepcopy(move)
                beta = min(beta, value)
            if beta <= alpha:
                break
        return value
