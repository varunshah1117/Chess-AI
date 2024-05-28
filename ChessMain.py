##This class is responsible for handling user inputs and displays the current state of the game.
import pygame as p
import sys
sys.path.append('C:\\Users\\Ayush\\Desktop\\Python\\Chess')

import ChessEngine, RandomAI, minmaxAI

WIDTH = HEIGHT = 512
DIMENSION = 8 #8x8 chess board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #For animations of chess move
IMAGES = {}

def load_images():
    pieces = ["wp","wR","wN","wB","wK","wQ","bp","bR","bN","bB","bK","bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

'''
The main driver for our code. This will handle user input.
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs  = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False#Flag variable for when a move is made
    animate = False#Flag variable for when we should animate a move

    load_images()
    running = True
    sqSelected = ()#Keeps track of the last click of the user (tuple: (row, col))
    playerClicks = []#Keeps track of player clicks(two tuples: [(6,4), (4,4)])
    gameOver = False
    playerOne = True#if a human is playing white, then this will be True. If an AI is playing, then False
    playerTwo = False#Same as above but for black
    #If both are false then both moves are made by the AI

    while running:
        humanTurn = (gs.whiteTomove and playerOne) or (not gs.whiteTomove and playerTwo)
        try:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                #Gets triggered by mouse clicks
                elif e.type == p.MOUSEBUTTONDOWN:#Mouse clicks
                    if not gameOver and humanTurn:
                        location = p.mouse.get_pos()#(x,y) position of the mouse
                        col = location[0]//SQ_SIZE
                        row = location[1]//SQ_SIZE
                        if sqSelected == (row, col):#the user clicked the same sqaure twice
                            sqSelected = ()#Deselect
                            playerClicks = []#clear Player clicks
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)
                        
                        if len(playerClicks) == 2:#after 2nd click
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            print(move.getChessNotation())
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMoves(validMoves[i])
                                    moveMade = True
                                    animate=True
                                    sqSelected = ()#Reserts the user clicks
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]
                #Key Handlers
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z: #Undoes the move when Z is pressed
                        gs.undoMoves()
                        moveMade = True
                        animate=False
                        gameOver=False
                    if e.key == p.K_r:#resets the board
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected=()
                        playerClicks=[]
                        moveMade=False
                        animate=False
                        gameOver=False
        except Exception as e:
         # Handle the exception appropriately
            print("An error occurred while processing events:", e)


        #AI Finder
        if not gameOver and not humanTurn:
            AIMove = minmaxAI.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = RandomAI.findRandomMove(validMoves)
            gs.makeMoves(AIMove)
            moveMade = True
            animate=True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
                validMoves = gs.getValidMoves()
                moveMade = False
                animate=False

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteTomove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')

        clock.tick(MAX_FPS)
        p.display.flip()

'''
Highlight the squares
'''
def highlightSqaures(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r,c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteTomove else 'b'):#selected piece
            #highlighting the square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(200)#transparency value
            s.fill(p.Color('green'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #Higlight possible moves
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) #draw squares on the board
    #add in piece highlighting or move suggestions(later)
    highlightSqaures(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) #drawing pieces on top of the squares


'''
Drawing the squares on the board. The top left square is always light.
'''
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("purple")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color= colors[((row+col)%2)]
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw the pieces on the board using the current GameState.board
'''
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":#not empty space
                screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animateMove(move, screen, board, clock):
    global colors
    coords = []#list of coords that the animation will move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    frames_per_sq = 10#frames to move a single sqaure
    frameCount = (abs(dR)+abs(dC))*frames_per_sq
    for frame in range(frameCount+1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #Erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol)%2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
    
def drawText(screen, text):
    font = p.font.SysFont('Helvitca', 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main()