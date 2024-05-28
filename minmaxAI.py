import random

pieceScore = {"K": 0, "Q": 10, "R":5, "B":3, "N":3, "p":1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2#Number of moves the algo checks ahead

def findBestMoveMinMax(gs, validMoves):
    turnMultiplier = 1 if gs.whiteTomove else -1
    oppMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMoves(playerMove)
        oppMoves = gs.getValidMoves()
        oppMaxScore = -CHECKMATE
        for opp_move in oppMoves:
            gs.makeMoves(opp_move)
            if gs.checkMate:
                score = -turnMultiplier*CHECKMATE
            elif gs.staleMate:
                score=STALEMATE
            else:
                score = -turnMultiplier*scoreMaterial(gs.board)
            if score > oppMaxScore:
                oppMaxScore = score
            gs.undoMoves()
        if oppMaxScore < oppMinMaxScore:
            oppMinMaxScore = oppMaxScore
            bestPlayerMove = playerMove
        gs.undoMoves()
    
    return bestPlayerMove

#This method makes the first recursive call
def findBestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None
    counter=0
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteTomove)
    #findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteTomove else -1)
    #findMoveAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteTomove else -1) 
    print(counter)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteTomove):
    global nextMove, counter
    counter+=1
    if depth==0:
        return scoreMaterial(gs.board)
    
    if whiteTomove:
        maxScore = -CHECKMATE
        random.shuffle(validMoves)
        for move in validMoves:
            gs.makeMoves(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMoves()
        return maxScore


    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMoves(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMoves()
        return minScore
    
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMoves(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move

        gs.undoMoves()
    return maxScore

def findMoveAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    #move ordering
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMoves(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move

        gs.undoMoves()
        if maxScore > alpha:#Pruning
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

'''
A positive score is good for white whereas, a negative score is good for black
'''
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteTomove:
            return -CHECKMATE#Black Wins
        else:
            return CHECKMATE#White Wins
    elif gs.staleMate:
        return STALEMATE
    
    score=0
    for row in gs.board:
        for square in row:
            if square[0]=='w':
                score += pieceScore[square[1]]
            elif square[0]=='b':
                score -= pieceScore[square[1]]

    return score

#Scoring the board on the material
def scoreMaterial(board):
    score=0
    for row in board:
        for square in row:
            if square[0]=='w':
                score += pieceScore[square[1]]
            elif square[0]=='b':
                score -= pieceScore[square[1]]

    return score
           

