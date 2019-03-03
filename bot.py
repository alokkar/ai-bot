import sys
import random
import signal
import time
import copy

class Bot:

    def __init__(self):
        self.flag = 1
        self.depth = 7
        self.next_move = (0, 0, 0)

    def flagtonum(self, flag):
        if flag == 'x':
            return 1
        if flag == 'o':
            return -1

    def numtoflag(self, flag):
        if flag == 1:
            return 'x'
        if flag == -1:
            return 'o'

    def move(self, board, old_move, flg):
        self.flag = self.flagtonum(flg)
        
        alpha = -999999999 
        beta = -alpha

        curr_board = copy.deepcopy(board)
        self.minimax(curr_board, old_move, self.flag, alpha, beta, 1)

        return self.next_move

    def returnValEval(self, arr, los):
        # arr[0] => 'x' ... arr[1] => 'o' ... arr[2] => 'd' ... arr[3] => '-'
        heuristic = 0
        if(arr[0] == 3 and arr[3] == 0 and arr[1] == 0 and los !=0 ):
            heuristic = 10000
        if(arr[1] == 3 and arr[3] == 0 and arr[0] == 0 and los !=0 ):
            heuristic = -10000

        # if(arr[0] == 2 and arr[3] == 1 and arr[1] == 0 and los != 0):
        #     heuristic = 2
        # if(arr[1] == 2 and arr[3] == 1 and arr[0] == 0 and los != 0):
        #     heuristic = -2

        # if(arr[0] == 2 and arr[3] == 1 and arr[1] == 0):
        #     heuristic = 2
        # if(arr[1] == 2 and arr[3] == 1 and arr[0] == 0):
        #     heuristic = -2

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

    def checkRows(self, array,los):
        val = 0
        for i in range(3):
            arr = [0, 0, 0, 0]
            for j in range(3):
                arr = self.returnCount(array[i][j], arr)
            val += self.returnValEval(arr, los)
        return val

    def checkColumns(self, array, los):
        val = 0
        for j in range(3):
            arr = [0, 0, 0, 0]
            for i in range(3):
                arr = self.returnCount(array[i][j], arr)
            val += self.returnValEval(arr, los)
        return val
 
    def checkDiagonal(self, array, los):
        val = 0
        arr=[0,0,0,0]
        arr = self.returnCount(array[0][0],arr)
        arr = self.returnCount(array[1][1],arr)
        arr = self.returnCount(array[2][2],arr)
        val+=self.returnValEval(arr, los)
        arr=[0,0,0,0]
        arr = self.returnCount(array[0][2],arr)
        arr = self.returnCount(array[1][1],arr)
        arr = self.returnCount(array[2][0],arr)
        val+=self.returnValEval(arr, los)
        return val

    def weightedEval(self, board):
        weight = [[8, 5, 8], [5, 15, 5], [8, 5, 8]]
        val = 0
        for k in range(2):
            for i in range(3):
                for j in range(3):
                    if board.small_boards_status[k][i][j] == 'x':
                        val += 1
                    if board.small_boards_status[k][i][j] == 'o':
                        val -= 1

        return val

    def localeval(self, board):
        localheuristic = 0
        for k in range(2):
            for i in range(0, 9, 3):
                for j in range(0, 9, 3):
                    if board.big_boards_status[k][i + 1][j + 1] == 'x':
                        localheuristic += 3
                    if board.big_boards_status[k][i + 1][j + 1] == 'o':
                        localheuristic -= 3
                
        for k in range(2):
            for i in range(0, 3):
                for j in range(0, 3):
                    if board.big_boards_status[k][i + 3][j + 3] == 'x':
                        localheuristic += 3
                    if board.big_boards_status[k][i + 3][j + 3] == 'o':
                        localheuristic -= 3

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
                    localheuristic += self.checkRows(arr,0) + self.checkColumns(arr,0) + self.checkDiagonal(arr,0)  

        return localheuristic

    def evaluate(self, board, old_move):
        smallboard = 0
        bigboard = 0
        wincheck = 0

        wincheck += self.checkRows(board.small_boards_status[0],1) + self.checkColumns(board.small_boards_status[0],1) + self.checkDiagonal(board.small_boards_status[0],1)
        wincheck += self.checkRows(board.small_boards_status[1],1) + self.checkColumns(board.small_boards_status[1],1) + self.checkDiagonal(board.small_boards_status[1],1)
        
        bigboard += self.weightedEval(board)

        smallboard += self.localeval(board)
        return bigboard + wincheck + smallboard

    def terminate(self, old_move, board, depth, flag):

        check = board.find_terminal_state()

        if check[0]=='WON':
        	return(1,flag*10000)

        if depth == self.depth or check[0] != 'CONTINUE':
            return (1, flag*self.evaluate(board, old_move))


        return (0,0)

    def minimax(self, board, old_move, flag, alpha, beta, depth):

        term = self.terminate(old_move, board, depth, flag)

        if term[0] == 1:
            return term[1]

        valid_moves = board.find_valid_move_cells(old_move)
        random.shuffle(valid_moves)
        # print(flag)


        if flag > 0:

            best = -999999999

            for move in valid_moves:

                board.update(old_move, move, self.numtoflag(flag))

                child = self.minimax(board, move, -flag, alpha, beta, depth + 1)

                if child > best:
                    best = child
                    if(depth==1):
                        self.next_move = copy.deepcopy(move)

                alpha = max(best, alpha)

                if beta <= alpha:
                    break
            
            return best
        
        else:

            best = 999999999

            for move in valid_moves:

                board.update(old_move, move, self.numtoflag(flag))

                child = self.minimax(board, move, -flag, alpha, beta, depth + 1)

                if(child < best):
                    best = child
                    if(depth==1):
                        self.next_move = copy.deepcopy(move)

                beta = min(best, beta)

                if beta <= alpha:
                    break
            
            return best

            