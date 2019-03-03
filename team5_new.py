import sys
import random
import time
import copy

class Team5_new:
    def __init__(self):
        self.flag = 1
        self.next_move = (0, 0, 0)
        self.maxdepth = 4

    def flagtonum(self, flag):
        #Function to convert the string flag to num to use in evals (Instead of using if conditions everywhere)
        if flag == 'x':
            return 1
        else:
            return -1

    def numtoflag(self, num):
        #Function to convert the num flag to string to use in updates (Instead of using if conditions everywhere)
        if num == 1:
            return 'x'
        else:
            return 'o'

    def heuristic(self, arr):
        # arr[0] => 'x' ... arr[1] => 'o' ... arr[2] => 'd' ... arr[3] => '-'
        heuristic = 0
        #Give High value if all three points are your and give the exact negetive of that if they're opponent's
        if(arr[0] == 3 and arr[3] == 0 and arr[1] == 0):
            heuristic = 2048
        if(arr[1] == 3 and arr[3] == 0 and arr[0] == 0):
            heuristic = -2048
        #Give Lower value if only two points are your and give the exact negetive of that if they're opponent's
        if(arr[0] == 2 and arr[3] == 1 and arr[1] == 0):
            heuristic = 512
        if(arr[1] == 2 and arr[3] == 1 and arr[0] == 0):
            heuristic = -512
        #Give very low value if only points are your and give the exact negetive of that if they're opponent's
        if(arr[0] == 1 and arr[3] == 2 and arr[1] == 0):
            heuristic = 64
        if(arr[1] == 1 and arr[3] == 2 and arr[0] == 0):
            heuristic = -64
        #Give extremely low value if none three points are your or your opponent's
        if(arr[0] == 0 and arr[3] == 3 and arr[1] == 0):
            heuristic = 2

        #Give High value if you're blocking opponent's win and negetive if opponent is blocking your win
        if(arr[0] == 1 and arr[1] == 2):
            heuristic = 1024
        if(arr[1] == 1 and arr[0] == 2):
            heuristic = -1024

        return heuristic

    def countnum(self, cell, arr):
        # arr[0] => 'x' ... arr[1] => 'o' ... arr[2] => 'd' ... arr[3] => '-'
        #Increase count based on whatever the element on the board is.
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
        #Go through all three rows in the 3x3 matrice given.
        val = 0
        for i in range(3):
            arr = [0, 0, 0, 0]
            for j in range(3):
                arr = self.countnum(array[i][j], arr)
            val += self.heuristic(arr)
        return val

    def checkColumns(self, array):
        #Go through all three columns in the 3x3 matrice given.
        val = 0
        for j in range(3):
            arr = [0, 0, 0, 0]
            for i in range(3):
                arr = self.countnum(array[i][j], arr)
            val += self.heuristic(arr)
        return val

    def checkDiagonal(self, array):
        #((0,0),(1,1),(2,2)) and ((0,2),(1,1),(2,0)) are the only two diagonals in a 3x3 matrice.
        val = 0
        arr=[0,0,0,0]
        arr = self.countnum(array[0][0],arr)
        arr = self.countnum(array[1][1],arr)
        arr = self.countnum(array[2][2],arr)
        val+=self.heuristic(arr)
        arr=[0,0,0,0]
        arr = self.countnum(array[0][2],arr)
        arr = self.countnum(array[1][1],arr)
        arr = self.countnum(array[2][0],arr)
        val+=self.heuristic(arr)
        return val

    def localheuristic(self, board):
        #Go through each block and calculate value
        localheuristic = 0
        for k in range(2):
            for i in range(0, 9, 3):
                for j in range(0, 9, 3):
                    arr = []
                    for x in range(3):
                        temp = []
                        for y in range(3):
                            temp.append(board.big_boards_status[k][i + x][j + y])
                        arr.append(list(temp))
                    localheuristic += self.checkRows(arr) + self.checkColumns(arr) + self.checkDiagonal(arr)
        return localheuristic

    def weightedVal(self, board):
        #Give more weights to corner blocks
        weight = [[6, 4, 6], [4, 3, 4], [6, 4, 6]]
        val = 0
        for k in range(2):
            for i in range(3):
                for j in range(3):
                    if board.small_boards_status[k][i][j] == 'x':
                        val += 100 * weight[i][j]
                    if board.small_boards_status[k][i][j] == 'o':
                        val += -100 * weight[i][j]
        return val


    def evaluation(self, board, old_move,flag):
        heuristicboard = 0
        heuristicweighted = 0
        #Calculating larger board heuristic
        #Calculates Status of small board and checks if winnig
        heuristicboard += self.checkRows(board.small_boards_status[0]) + self.checkColumns(board.small_boards_status[0]) + self.checkDiagonal(board.small_boards_status[0])
        heuristicboard += self.checkRows(board.small_boards_status[1]) + self.checkColumns(board.small_boards_status[1]) + self.checkDiagonal(board.small_boards_status[1])
        #Calculates status of all the blocks and checks which ones are won.
        heuristiclocal = self.localheuristic(board)
        #Gets weighted values from the small board status
        heuristicweighted = self.weightedVal(board)

        final_value = 18*heuristicboard + heuristiclocal + heuristicweighted
        #If the move gives the next player free move then reduce heuristic value
        if board.small_boards_status[0][old_move[1]/3][old_move[2]/3] != '-' and board.small_boards_status[1][old_move[1]/3][old_move[2]/3] != '-':
            return final_value - 10000
        else:
            return final_value


    def move(self, board, old_move, flag):
        self.flag = self.flagtonum(flag)
        val=self.minimax(board, old_move, 0, -999999999, 999999999, True, self.numtoflag(self.flag))
        return (self.next_move[0], self.next_move[1],self.next_move[2])

    def finished(self, board, old_move, depth):
        check = board.find_terminal_state()
        #If final depth or game done then stop
        if depth == self.maxdepth or check[0] != 'CONTINUE':
            return (1, (self.flag) * self.evaluation(board, old_move,self.flag))
        else:
            return (0, 0)

    def minimax(self, board, old_move, depth, alpha, beta, ismaxplayer, flag):
        #check if the search should be stopped or not
        iffinished = self.finished(board, old_move, depth)
        if iffinished[0] == 1:
            return iffinished[1]
        best_value = ismaxplayer * -999999999 + (1 - ismaxplayer) * 999999999
        #Find valid moves and shuffle them
        valid_moves = board.find_valid_move_cells(old_move)
        random.shuffle(valid_moves)

        #Run a DFS
        for move in valid_moves:
            board.update(old_move, move, flag)
            nextp = 1 - ismaxplayer
            #Bonus move
            if board.big_boards_status[old_move[0]][old_move[1]][old_move[2]] != flag and board.small_boards_status[move[0]][move[1] / 3][move[2] / 3] == flag:
                nextp = ismaxplayer
                flag = self.numtoflag(0 - self.flagtonum(flag))
            child = self.minimax(board, move, depth + 1, alpha, beta, nextp, self.numtoflag(0 - self.flagtonum(flag)))
            #Reset the board
            board.big_boards_status[move[0]][move[1]][move[2]] = '-'
            board.small_boards_status[move[0]][move[1] / 3][move[2] / 3] = '-'
            #Alpha-Beta Pruning
            if ismaxplayer:
                if child > best_value:
                    best_value = child
                    if depth == 0:
                        self.next_move = copy.deepcopy(move)
                alpha = max(alpha, best_value)
            else:
                if child < best_value:
                    best_value = child
                    if depth == 0:
                        self.next_move = copy.deepcopy(move)
                beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value
