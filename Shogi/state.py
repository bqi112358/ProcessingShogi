import random

class State:
    def __init__(self):
        startpos = [-2, -3, -4, -5, -8, -5, -4, -3, -2,
                     0, -7,  0,  0,  0,  0,  0, -6,  0,
                    -1, -1, -1, -1, -1, -1, -1, -1, -1,
                     0,  0,  0,  0,  0,  0,  0,  0,  0,
                     0,  0,  0,  0,  0,  0,  0,  0,  0,
                     0,  0,  0,  0,  0,  0,  0,  0,  0,
                     1,  1,  1,  1,  1,  1,  1,  1,  1,
                     0,  6,  0,  0,  0,  0,  0,  7,  0,
                     2,  3,  4,  5,  8,  5,  4,  3,  2]
        self.weights = 0, 2, 4, 6, 8, 10, 12, 14, 100, -100, -14, -12, -10, -8, -6, -4, -2, 0
        self.major = dict((piece, [None]*81) for piece in (2, 6, 7, 14, 15))
        self.minor = dict((piece, [None]*81) for piece in (1, 3, 4, 5, 8, 9, 10, 11, 12, 14, 15))
        ds = ((1, -1, 8), (1, 1, 10), (-1, -1, -10), (-1, 1, -8), (-1, 0, -9), (0, -1, -1), (0, 1, 1), (1, 0, 9))
        for p in range(81):
            (i, j), raid = divmod(p, 9), p<27
            ctrl = [[(n, n<27, n%9) for n in range(p-10, p-10*(1+min(i,   j)), -10)],
                    [(n, n<27, n%9) for n in range(p- 8, p- 8*(1+min(i, 8-j)), - 8)],
                    [(n, raid, n%9) for n in range(p+10, p+10*(9-max(i,   j)),  10)],
                    [(n, raid, n%9) for n in range(p+ 8, p+ 8*(9-max(i, 8-j)),   8)]]
            self.major[ 6][p] = [[(n, (6, 14)[prom], nj) for n, prom, nj in ns] for ns in ctrl]
            self.major[14][p] = [[(n,     14       , nj) for n, prom, nj in ns] for ns in ctrl]
            ctrl = [[(n, n<27,   j) for n in range(p-9,    -1, -9)],
                    [(n, raid,   j) for n in range(p+9,    81,  9)],
                    [(n, raid, n%9) for n in range(p-1, p-j-1, -1)],
                    [(n, raid, n%9) for n in range(p+1, p-j+9,  1)]]
            self.major[ 2][p] = [[(n, (2,  9)[prom], nj) for n, prom, nj in ctrl[0]]]
            self.major[ 7][p] = [[(n, (7, 15)[prom], nj) for n, prom, nj in ns] for ns in ctrl]
            self.major[15][p] = [[(n,     15       , nj) for n, prom, nj in ns] for ns in ctrl]
            self.minor[ 1][p] = [[p-9, (1, 9)[i<=3], j, i<=3]] if i else []
            self.minor[ 3][p] = [[p+dj-18, (3, 11)[i<=4], j+dj, None] for dj in (-1, 1) if 0<=j+dj<=8] if i>=2 else []
            c = [(p+d, j+dj, 0<=i+di<=8 and 0<=j+dj<=8) for di, dj, d in ds]
            for piece, ctrl in (4,c[:5]), (5,c[2:]), (8,c), (9,c[2:]), (10,c[2:]), (11,c[2:]), (12,c[2:]), (14,c[4:]), (15,c[:4]):
                self.minor[piece][p] = [[n, piece, nj, None] for n, nj, on_board in ctrl if on_board]
        self.board = startpos
        self.hand = [0] * 18
        self.nonp = [False] * 18

    def legal_moves(self, board, hand, nonp):
        for p, p0 in enumerate(board):
            if not p0:
                for n1 in 7, 6, 5, 4:
                    if hand[n1]:
                        yield p, n1
                if p >= 9:
                    if p >= 18:
                        if hand[3]:
                            yield p, 3
                    if hand[2]:
                        yield p, 2
                    if nonp[p%9] and hand[1]:
                        yield p, 1
            else:
                if p0 in self.major:
                    for ns in self.major[p0][p]:
                        for n, n1, nj in ns:
                            n0 = -board[n]
                            if n0 >= 0:
                                yield n, n1, nj, n0, p
                            if n0:
                                break
                if p0 in self.minor:
                    for n, n1, nj, pp in self.minor[p0][p]:
                        n0 = -board[n]
                        if n0 >= 0:
                            yield n, n1, nj, n0, p, pp

    def do(self, board, hand, nonp, n, n1, nj=None, n0=None, p=None, pp=None):
        board, hand, nonp = [-piece for piece in board[::-1]], hand[::-1], nonp[::-1]
        board[80-n] = -n1
        if nj == None:
            hand[-1-n1] -= 1
            if n1 == 1:
                nonp[-1-n%9] = False
        else:
            board[80-p] = 0
            if n0 >= 9:
                hand[7-n0] += 1
            elif n0:
                hand[-1-n0] += 1
                if n0 == 1:
                    nonp[8-nj] = True
            if pp:
                nonp[-1-nj] = True
        return board, hand, nonp

    def act(self, move):
        self.board, self.hand, self.nonp = self.do(self.board, self.hand, self.nonp, *move)
    
    def negamax(self, depth, alpha, beta, board, hand, nonp):
        if hand[9]:
            return -1000
        if not depth:
            return sum(board) + sum(w*p for w, p in zip(self.weights, hand))
        for move in list(self.legal_moves(board, hand, nonp)):
            alpha = max(alpha, -self.negamax(depth-1, -beta, -alpha, *self.do(board, hand, nonp, *move)))
            if alpha >= beta:
                return alpha
        return alpha
        
    def search(self, depth=1):
        alpha, bestmove = -1000, None
        moves = list(self.legal_moves(self.board, self.hand, self.nonp))
        random.shuffle(moves)
        for move in moves:
            score = -self.negamax(depth, -1000, -alpha, *self.do(self.board, self.hand, self.nonp, *move))
            if score > alpha:
                alpha = score
                bestmove = move
        return alpha, bestmove
