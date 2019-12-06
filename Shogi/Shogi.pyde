from state import State

bPieces, wPieces = [None], [None]
def setup():
    global particles
    size(640, 480)
    for i in range(1, 16):
        bPieces.append(loadImage('b{}.png'.format(i)))
        wPieces.append(loadImage('w{}.png'.format(i)))
    textSize(20)
    textAlign(CENTER, CENTER)
    particles = [[random(width), random(height)] for i in range(1000)]
    
def draw():
    background(0)
    drawParticles()
    drawBoard()
    drawPieces()
    drawHands()
    if drop or prevI != None:
        drawTargets()
    if dialog[0]:
        drawDialog()
    if result != None:
        fill(255, 255, 0)
        textSize(100)
        text(['YOU WIN', 'YOU LOSE'][result], width/2, height/2)
        noLoop()
        
        
particles = []
def drawParticles():
    for i, (x, y) in enumerate(particles):
        particles[i][0] += random(-1, 1)
        particles[i][1] += random(3)
        if y > 1000:
            particles[i][1] = 0
        strokeWeight(random(5))
        stroke(512*abs(.5-x/width), 512*abs(.5-y/height), 256*i/len(particles))
        point(x, y)
        
def drawBoard():
    noStroke()
    fill(255, 192, 64)
    rect(0, 0, 100, 350)
    rect(540, 130, 100, 350)
    rect(122, 24, 396, 432)
    

def drawPieces():
    for i in range(9):
        for j in range(9):
            for piece in range(1, 16):
                if state.board[i][j] == piece:
                    image(bPieces[piece], 131+j*42, 33+i*46)
                elif state.board[i][j] == -piece:
                    image(wPieces[piece], 131+j*42, 33+i*46)
    stroke(0)
    noFill()
    for i in range(9):
        for j in range(9):
            strokeWeight(1)
            rect(131+j*42, 33+i*46, 42, 46)
            if (i==3 or i==6) and (j==3 or j==6):
                strokeWeight(5)
                point(131+j*42, 33+i*46)
                

def drawHands():
    fill(0, 64, 128)
    for piece in range(1, 8):
        if state.hand.count(piece) != 0:
            image(bPieces[piece], 550, 80+piece*50)
            text('x{}'.format(state.hand.count(piece)), 615, 105+piece*50)
        if state.hand.count(-piece) != 0:
            image(wPieces[piece], 10, 350-piece*50)
            text('x{}'.format(state.hand.count(-piece)), 75, 375-piece*50)
            

def mousePressed():
    global drop, nextI, nextJ, prevI, prevJ
    i = (mouseY-33) // 46
    j = (mouseX-131) // 42
    if dialog[0]:
        renewState(0<mouseX-dialog[0]<84 and 0<mouseY-dialog[1]<46, 0, mouseX-dialog[0]<42, nextI, nextJ, prevI, prevJ)
    elif drop or prevI != None:
        if 0<=i<=8 and 0<=j<=8 and targets[i][j]:
            if drop:
                renewState(True, drop, 0, i, j)
            else:
                prevPiece = state.board[prevI][prevJ]
                if (prevPiece in (1, 2) and i==0) or (prevPiece==3 and i<2):
                    renewState(True, 0, 1, i, j, prevI, prevJ)
                elif prevPiece<8 and (prevI<3 or i<3):
                    nextI, nextJ = i, j
                    dialog[0], dialog[1] = mouseX, mouseY
                else:
                    renewState(True, 0, 0, i, j, prevI, prevJ)
        else:
            renewState(False)
    elif 0<=i<=8 and 0<=j<=8 and state.board[i][j] > 0:
        for move in legalMoves:
            if len(move) > 4 and move[4]==i and move[5]==j:
                targets[move[2]][move[3]] = True
        prevI, prevJ = i, j
    elif mouseX>540 and (mouseY-80)//50 in state.hand:
        drop = (mouseY-80) // 50
        for move in legalMoves:
            if move[0]:
                targets[move[2]][move[3]] = True
            

targets = [[False]*9 for i in range(9)]
def drawTargets():
    fill(0, 0, 255, 32)
    noStroke()
    if drop:
        rect(540, 80+drop*50, 100, 50)
    else:
        rect(131+prevJ*42, 33+prevI*46, 42, 46)
    for i in range(9):
        for j in range(9):
            if targets[i][j]:
                rect(147+j*42, 51+i*46, 10, 10)
                

dialog = [None, None]
def drawDialog():
    rect(dialog[0], dialog[1], 84, 46)
    image(bPieces[state.board[prevI][prevJ]+7], dialog[0], dialog[1])
    image(bPieces[state.board[prevI][prevJ]], dialog[0]+42, dialog[1])
    

state = State()
legalMoves = state.legal_moves()
drop = nextI = nextJ = prevI = prevJ = result = None
def renewState(renew, dr=None, pr=None, ni=None, nj=None, pi=None, pj=None):
    global state, legalMoves, drop, nextI, nextJ, prevI, prevJ, targets, result
    if renew:
        state = state.child(dr, pr, ni, nj, pi, pj)
        if not any(bool(state.child(*move).legal_moves()) for move in state.legal_moves()):
            result = 1
        else:
            state = state.child(*state.negamax()[1])
            legalMoves = state.legal_moves()
            if not legalMoves:
                result = 0
    drop = nextI = nextJ = prevI = prevJ = dialog[0] = dialog[1] = None
    targets = [[False]*9 for i in range(9)]
