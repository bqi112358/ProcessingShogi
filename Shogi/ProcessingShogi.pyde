from state import State

state = State()
legalMoves = list(state.legal_moves(state.board, state.hand, state.nonp))
dialog = [None, None]
targets = [False] * 81
n = n1 = nj = n0 = p = pawn = result = None  
LV = 1
f = -10

def setup():
    global particles, bPieces, wPieces
    size(1280, 960)
    frameRate(30)
    particles = [[random(width), random(height)] for i in range(255)]
    bPieces = [loadImage('b{}.png'.format(i)) for i in range(16)]
    wPieces = [loadImage('w{}.png'.format(i)) for i in range(16)]
    
def draw():
    background(0)
    drawParticles()
    drawLevel()
    scale(2)
    drawBoard()
    drawPieces()
    drawHands()
    if n1 != None:
        drawTargets()
        if dialog[0]:
            drawDialog()
    elif result != None:
        scale(0.5)
        drawResult()
    else:
        fill(255)
        textSize(12)
        if frameCount == f + 1:
            text("CPU THINKING...", 0, 360)
        else:
            if frameCount == f + 2:
                cpu_move()
            text("YOUR TURN", 540, 130)
    
def drawParticles():
    for i, (x, y) in enumerate(particles):
        strokeWeight(random(5))
        stroke(1024*abs(.5-x/width), 1024*abs(.5-y/height), i)
        point(x, y)
        particles[i][0] += random(-3, 3)
        particles[i][1] += random(5)
        if y > height:
            particles[i][1] = 0
        
def drawLevel():
    fill(255)
    textSize(40)
    textAlign(CENTER)
    text('CPU LEVEL:{} (up/down key to change)'.format(LV), width/2, 40)
        
def drawBoard():
    noStroke()
    fill(255, 192, 64)
    rect(0, 0, 100, 350)
    rect(540, 130, 100, 350)
    rect(122, 24, 396, 432)
    
def drawPieces():
    for i in range(9):
        for j in range(9):
            piece = state.board[9*i+j]
            if piece > 0:
                image(bPieces[piece], 131+j*42, 33+i*46)
            elif piece:
                image(wPieces[-piece], 131+j*42, 33+i*46)
    stroke(0)
    noFill()
    for i in range(9):
        for j in range(9):
            strokeWeight(1)
            rect(131+j*42, 33+i*46, 42, 46)
            if i and j and i%3 == j%3 == 0:
                strokeWeight(5)
                point(131+j*42, 33+i*46)
                
def drawHands():
    fill(0, 64, 128)
    textSize(20)
    textAlign(LEFT)
    for piece in range(1, 8):
        if state.hand[piece]:
            image(bPieces[piece], 550, 80+piece*50)
            text('x{}'.format(state.hand[piece]), 600, 105+piece*50)
        if state.hand[-1-piece]:
            image(wPieces[piece], 10, 350-piece*50)
            text('x{}'.format(state.hand[-1-piece]), 50, 375-piece*50)
            
def drawTargets():
    fill(0, 0, 255, 32)
    noStroke()
    if n1 != None and p == None:
        rect(540, 80+n1*50, 100, 50)
    else:
        rect(131+p%9*42, 33+p//9*46, 42, 46)
    for i in range(9):
        for j in range(9):
            if targets[9*i+j]:
                rect(147+j*42, 51+i*46, 10, 10)
                
def drawDialog():
    rect(dialog[0], dialog[1], 84, 46)
    image(bPieces[state.board[p]], dialog[0], dialog[1])
    image(bPieces[state.board[p]+8], dialog[0]+42, dialog[1])

def renewState(move=None):
    global state, legalMoves, result, n, n1, nj, n0, p, pawn, targets, f
    if move:
        state.act(move)
        state.board, state.hand = [-piece for piece in state.board[::-1]], state.hand[::-1]
        f = frameCount
    n = n1 = nj = n0 = p = pawn = dialog[0] = dialog[1] = None
    targets = [False] * 81
    
def cpu_move():
    global state, result, legalMoves, f
    state.board, state.hand = [-piece for piece in state.board[::-1]], state.hand[::-1]
    score, bestmove = state.search(LV)
    if score == -1000:
        state.board, state.hand = [-piece for piece in state.board[::-1]], state.hand[::-1]
        result = 0
    else:
        state.act(bestmove)
        legalMoves = list(state.legal_moves(state.board, state.hand, state.nonp))
        if state.search()[0] == -1000:
            result = 1
    
def drawResult():
    fill(255*(1-result), 0, 255*result, 128)
    textSize(100)
    textAlign(CENTER)
    text(['YOU WIN', 'YOU LOSE'][result], width/2, height/2)
    noLoop()
    
def mousePressed():
    global n, n1, nj, n0, p, pawn, dialog
    i = (mouseY/2-33) // 46
    j = (mouseX/2-131) // 42
    pos = 9 * i + j
    if dialog[0]:
        if 0<mouseX/2-dialog[0]<84 and 0<mouseY/2-dialog[1]<46:
            prom = n1+8*(mouseX/2-dialog[0]>42)
            renewState((n, prom, nj, n0, p, pawn and prom))
        else:
            renewState()
    elif n1 != None:
        if 0<=i<=8 and 0<=j<=8 and targets[pos]:
            if p == None:
                renewState((pos, n1))
            else:
                n0 = -state.board[pos]
                if ((n1==1 or n1==2) and i==0) or (n1==3 and i<2):
                    renewState((pos, n1+8, j, n0, p, n1==1))
                elif n1<=7 and (p<27 or pos<27):
                    n, nj, n0, pawn = pos, j, n0, n1==1
                    dialog[0], dialog[1] = mouseX/2, mouseY/2
                else:
                    renewState((pos, n1, j, n0, p))
        else:
            renewState()
    elif 0<=i<=8 and 0<=j<=8 and state.board[pos] > 0:
        for move in legalMoves:
            if len(move) > 2 and move[4] == pos:
                targets[move[0]] = True
        n1, p = state.board[pos], pos
    elif mouseX/2>540 and state.hand[(mouseY/2-80)//50]:
        n1 = (mouseY/2-80) // 50
        for move in legalMoves:
            if len(move) == 2 and move[1] == n1:
                targets[move[0]] = True
              
def keyPressed():
    global LV
    if keyCode == UP:
        LV = min(3, LV+1)
    elif keyCode == DOWN:
        LV = max(1, LV-1)
