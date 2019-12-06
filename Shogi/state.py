import random

class State:
    startpos = [[-2, -3, -4, -7,-14, -7, -4, -3, -2],
                [ 0, -6,  0,  0,  0,  0,  0, -5,  0],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
                [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
                [ 0,  5,  0,  0,  0,  0,  0,  6,  0],
                [ 2,  3,  4,  7, 14,  7,  4,  3,  2]]
    
    def __init__(self, board=startpos, hand=[]):
        self.board = board
        self.hand = hand

    def child(self, drop, prom, ni, nj, pi=0, pj=0):
        ni = 8 - ni
        nj = 8 - nj
        board = [[-piece for piece in rank[::-1]] for rank in self.board[::-1]]
        hand = [-piece for piece in self.hand]
        if drop:
            drop *= - 1
            board[ni][nj] = drop
            hand.remove(drop)
        else:
            pi = 8 - pi
            pj = 8 - pj
            piece = board[ni][nj]
            if 7 < piece < 14:
                hand.append(-piece+7)
            elif piece:
                hand.append(-piece)
            if prom:
                board[ni][nj] = board[pi][pj] - 7
            else:
                board[ni][nj] = board[pi][pj]
            board[pi][pj] = 0
        return State(board, hand)

    def legal_moves(self):
        moves = []
        for i in range(9):
            for j in range(9):
                piece = self.board[i][j]
                if piece == 1:
                    ni = i - 1
                    n_piece = self.board[ni][j]
                    if n_piece == -14:
                        return
                    if n_piece <= 0:
                        if i < 4:
                            moves.append((0, 1, ni, j, i, j))
                        else:
                            moves.append((0, 0, ni, j, i, j))
                elif piece == 2:
                    ni = i - 1
                    while ni >= 0:
                        n_piece = self.board[ni][j]
                        if n_piece == -14:
                            return
                        if n_piece > 0:
                            break
                        else:
                            if ni < 3:
                                moves.append((0, 1, ni, j, i, j))
                            if ni > 1:
                                moves.append((0, 0, ni, j, i, j))
                            if n_piece:
                                break
                            else:
                                ni -= 1
                elif piece == 3:
                    ni = i - 2
                    for dj in -1, 1:
                        nj = j + dj
                        if 0 < j < 8:
                            n_piece = self.board[ni][nj]
                            if n_piece <= 0:
                                if n_piece == -14:
                                    return
                                if i < 5:
                                    moves.append((0, 1, ni, nj, i, j))
                                if i > 3:
                                    moves.append((0, 0, ni, nj, i, j))
                elif piece == 4:
                    for di in -1, 1:
                        for dj in -1, 0, 1:
                            ni, nj = i + di, j + dj
                            if 0 <= ni <= 8 and 0 <= nj <= 8:
                                n_piece = self.board[ni][nj]
                                if n_piece <= 0 and (di == -1 or dj):
                                    if n_piece == -14:
                                        return
                                    if i < 3 or ni < 3:
                                        moves.append((0, 1, ni, nj, i, j))
                                    moves.append((0, 0, ni, nj, i, j))
                elif 6 < piece < 12:
                    for di in -1, 0, 1:
                        for dj in -1, 0, 1:
                            ni, nj = i + di, j + dj
                            if 0 <= ni <= 8 and 0 <= nj <= 8:
                                n_piece = self.board[ni][nj]
                                if n_piece <= 0 and (di == -1 or abs(di+dj) == 1):
                                    if n_piece == -14:
                                        return
                                    moves.append((0, 0, ni, nj, i, j))
                elif piece==5 or piece==12:
                    for di in -1, 1:
                        for dj in -1, 1:
                            ni, nj = i + di, j + dj
                            while 0 <= ni <= 8 and 0 <= nj <= 8:
                                n_piece = self.board[ni][nj]
                                if n_piece == -14:
                                    return
                                if n_piece > 0:
                                    break
                                else:
                                    if piece == 5 and (i < 3 or ni < 3):
                                        moves.append((0, 1, ni, nj, i, j))
                                    else:
                                        moves.append((0, 0, ni, nj, i, j))
                                    if n_piece:
                                        break
                                    else:
                                        ni += di
                                        nj += dj
                elif piece==6 or piece==13:
                    for di in -1, 1:
                        ni = i + di
                        while 0 <= ni <= 8:
                            n_piece = self.board[ni][j]
                            if n_piece == -14:
                                return
                            if n_piece > 0:
                                break
                            else:
                                if piece == 6 and (i < 3 or ni < 3):
                                    moves.append((0, 1, ni, j, i, j))
                                else:
                                    moves.append((0, 0, ni, j, i, j))
                                if n_piece:
                                    break
                                else:
                                    ni += di
                    for dj in -1, 1:
                        nj = j + dj
                        while 0 <= nj <= 8:
                            n_piece = self.board[i][nj]
                            if n_piece == -14:
                                return
                            if n_piece > 0:
                                break
                            else:
                                if piece == 6 and i < 3:
                                    moves.append((0, 1, i, nj, i, j))
                                else:
                                    moves.append((0, 0, i, nj, i, j))
                                if n_piece:
                                    break
                                else:
                                    nj += dj
                if piece > 11:
                    for di in -1, 0, 1:
                        for dj in -1, 0, 1:
                            ni, nj = i + di, j + dj
                            if 0 <= ni <= 8 and 0 <= nj <= 8:
                                n_piece = self.board[ni][nj]
                                if n_piece <= 0 and (ni or nj):
                                    if n_piece == -14:
                                        return
                                    moves.append((0, 0, ni, nj, i, j))
        for piece in set(self.hand):
            if piece == 1:
                droppable = set(range(9))
                for j in range(9):
                    for rank in self.board:
                        if rank[j] == 1:
                            droppable.remove(j)
                            break
                for i in range(1, 9):
                    for j in droppable:
                        if not self.board[i][j]:
                            moves.append((1, 0, i, j))
            elif piece > 1:
                for i in range(9):
                    for j in range(9):
                        if not self.board[i][j]:
                            if piece == 2:
                                if i > 0:
                                    moves.append((2, 0, i, j))
                            elif piece == 3:
                                if i > 1:
                                    moves.append((3, 0, i, j))
                            else:
                                moves.append((piece, 0, i, j))
        return moves
    
    def negamax(self, depth=4, a=-10000, b=10000):
        if not depth:
            return (sum(map(sum, self.board))+sum(self.hand)), None
        lm = self.legal_moves()
        if not lm:
            return 10000, None
        bm = random.choice(lm)
        for move in lm:
            score = -self.child(*move).negamax(depth-1, -b, -a)[0]
            if score > a:
                a = score
                bm = move
            if a >= b:
                break
        return a, bm
    
if __name__ == '__main__':
    pass
