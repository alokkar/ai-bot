import sys
import random
import signal
import time
import copy


class Alok:
    def __init__(self):
        self.nextmove=(0,0,0)
        self.depth=2

    def flagtonum(self,flag):
        if flag=='x':
            return 1
        else:
            return -1

    def numtoflag(self,flag):
        if flag==1:
            return 'x'
        else:
            return 'o'

    def count(self,cell,arr):
        if cell=='x':
            arr[0]+=1
        if cell=='o':
            arr[1]+=1
        if cell=='d':
            arr[2]+=1
        if cell=='-':
            arr[3]+=1
        return arr

    def returnValEval(self,arr):
        if (arr[0]==3 and arr[1]==0 and arr[3]==0):
            return 10000
        if (arr[0]==0 and arr[1]==3 and arr[3]==0):
            return -10000
        if (arr[0]==2 and arr[1]==0 and arr[3]==1):
            return 1000
        if (arr[0]==0 and arr[1]==2 and arr[3]==1):
            return -1000
        if (arr[0]==1 and arr[1]==0 and arr[3]==2):
            return 100
        if (arr[0]==0 and arr[1]==1 and arr[3]==3):
            return -100
        if (arr[0]==2 and arr[1]==1 and arr[3]==0):
            return -200
        if (arr[0]==1 and arr[1]==2 and arr[3]==0):
            return 200
        return 0
        

    def checkRows(self, array):
        val = 0
        for i in range(3):
            arr = [0, 0, 0, 0]
            for j in range(3):
                arr = self.count(array[i][j], arr)
            val += self.returnValEval(arr)
        return val

    def checkColumns(self, array):
        val = 0
        for j in range(3):
            arr = [0, 0, 0, 0]
            for i in range(3):
                arr = self.count(array[i][j], arr)
            val += self.returnValEval(arr)
        return val

    def checkDiagonal(self, array):
        val = 0
        arr=[0,0,0,0]
        arr = self.count(array[0][0],arr)
        arr = self.count(array[1][1],arr)
        arr = self.count(array[2][2],arr)
        val+=self.returnValEval(arr)
        arr=[0,0,0,0]
        arr = self.count(array[0][2],arr)
        arr = self.count(array[1][1],arr)
        arr = self.count(array[2][0],arr)
        val+=self.returnValEval(arr)
        return val


    def evaluate(self,board,old_move):
        blokval = 0

        blokval += self.checkRows(board.small_boards_status[0]) + self.checkColumns(board.small_boards_status[0]) + self.checkDiagonal(board.small_boards_status[0])
        blokval += self.checkRows(board.small_boards_status[1]) + self.checkColumns(board.small_boards_status[1]) + self.checkDiagonal(board.small_boards_status[1])

        return blokval


    def finish(self,old_move,board,depth,flag):
        check = board.find_terminal_state()
        if check[0]=='WON':
            return (1,flag*10000)
        if depth==self.depth or check[0]!='CONTINUE':
            return (1,flag*self.evaluate(board,old_move))
        return(0,0)

    def move(self,board,old_move,flag):
        self.flag = self.flagtonum(flag)
        curr_board = copy.deepcopy(board)
        self.minimax(curr_board,old_move,-999999999,999999999,self.flag,0)
        return self.nextmove

    def minimax(self,board,old_move,alpha,beta,flag,depth):
        fin = self.finish(old_move,board,depth,flag)
        if fin[0]==1:
            return fin[1]

        play_moves = board.find_valid_move_cells(old_move)
        random.shuffle(play_moves)

        if flag > 0:
            best = -999999999

            for move in play_moves:
                board.update(old_move, move, self.numtoflag(flag))
                child = self.minimax(board,move,alpha,beta,-flag,depth+1)
                if child>best:
                    best = child
                    if depth==0:
                        self.nextmove = copy.deepcopy(move)
                alpha = max(best,alpha)
                if alpha>=beta:
                    break
            return best
        else:
            best = 999999999

            for move in play_moves:

                board.update(old_move, move, self.numtoflag(flag))

                child = self.minimax(board,move,alpha,beta,-flag,depth+1)
                if child<best:
                    best = child
                    if depth==0:
                        self.nextmove = copy.deepcopy(move)
                beta = min(best,beta)

                if alpha>=beta:
                    break
            return best