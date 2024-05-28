##This class is responsible for storing all info. about the current state of the game.
##Also responsible for determining the valid moves at the current state.
##Maintains the move log.
class GameState():
    def __init__(self):
        #board is an 8x8 2-D lit, each element of the list has 2 chars
        #The first character represents the color of the piece
        #The second character represents the type of the piece
        #"--" represents the empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            [ "--", "--", "--", "--", "--", "--", "--", "--"],
            [ "--", "--", "--", "--", "--", "--", "--", "--"],
            [ "--", "--", "--", "--", "--", "--", "--", "--"],
            [ "--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        
        self.moveFunctions = {'p':self.getPawnMoves, 'R':self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q':self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteTomove = True
        self.moveLog = []
        #Initial King Locations
        self.whiteKinglocation = (7,4)
        self.blackKinglocation = (0,4)
        #Checkmate and stalemate variables
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()
        #self.currentCastlingRight = CastleRights(True, True, True, True)
        #self.CastleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    #Takes the move as a parameter and executes it(except moves like castling, en passant and pawn promotion)
    def makeMoves(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)#Maintains the game history
        self.whiteTomove = not self.whiteTomove#Swap between players after each move
        #Updating the King's Location
        if move.pieceMoved == 'wK':
            self.whiteKinglocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKinglocation = (move.endRow, move.endCol)

        #Pawn Promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] == move.pieceMoved[0] + 'Q'
        
        #Enpassant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'#capturing the pawn
        #update enPassant
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow)==2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()#Resets it

        #castle move
        #if move.isCastleMove:
         #   if move.endCol - move.startCol == 2:#Kingside castle
          #      self.board[move.endRow][move.endCol-1]=self.board[move.endRow][move.endCol+1]#moves the rook
           #     self.board[move.endRow][move.endCol+1]='--'#erase old rook
            #else:#Queenside castle
             #   self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
              #  self.board[move.endRow][move.endCol]='--'

        ##Update the castling rights
        #self.updateCastleRights(move)
        #self.CastleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))


    #Undoes the move made
    def undoMoves(self):
        if len(self.moveLog) != 0 :#Atlease one should be made to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured#Captured piece is brought back
            self.whiteTomove = not self.whiteTomove
            if move.pieceMoved == 'wK':
                self.whiteKinglocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKinglocation = (move.startRow, move.startCol)
            #undo enpassant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol]='--'#leaving landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            #undo a 2 square pawn advance
            if move.pieceMoved[1]=='p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

            self.checkMate = False
            self.staleMate = False
            '''
            #undo castling rights
            self.CastleRightsLog.pop()#get rid of the new castle rights from the move we are undoing
            self.currentCastlingRight = self.CastleRightsLog[-1]#set the current castle rights to the last one in the list
            #undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1]=self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1]='--'
                else:
                    self.board[move.endRow][move.endCol-2]=self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1]='--'

            '''


    ##Update the castle rights given the move
    '''
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol==0:#Left Rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol==7:#Right Rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol==0:#Left Rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol==7:#Right Rook
                    self.currentCastlingRight.bks = False
    '''

    ##All moves considering the checks
    def getValidMoves(self):
        temp_EnpassantPossible = self.enpassantPossible
        #tempCastleRights = CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)
        #Generate all possible moves
        moves = self.getPossibleMoves()
        #if self.whiteTomove:
         #   self.getCastleMoves(self.whiteKinglocation[0], self.whiteKinglocation[1], moves)
        #else:
         #   self.getCastleMoves(self.blackKinglocation[0], self.blackKinglocation[1], moves)
        #For each move make the move
        for i in range(len(moves)-1, -1,-1):#When removing from a list iterate backwards
            self.makeMoves(moves[i])

            self.whiteTomove = not self.whiteTomove
            if self.inCheck():
                moves.remove(moves[i])#If the king is under attack, not a valid move
            self.whiteTomove = not self.whiteTomove
            self.undoMoves()

        if len(moves)==0:#either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.enpassantPossible = temp_EnpassantPossible
        #self.currentCastlingRight = tempCastleRights

        return moves
    
    #Determines if the current player is in check
    def inCheck(self):
        if self.whiteTomove:
            return self.squareUnderAttack(self.whiteKinglocation[0], self.whiteKinglocation[1])
        else:
            return self.squareUnderAttack(self.blackKinglocation[0], self.blackKinglocation[1])
        
    #Determines if the enemy can attack the square r,c
    def squareUnderAttack(self,r,c):
        self.whiteTomove = not self.whiteTomove#Switch to opponent's turn
        oppMoves = self.getPossibleMoves()
        self.whiteTomove = not self.whiteTomove#Switch back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:#Square is under attack
                return True
        return False
            

    ##All moves without considering checks
    def getPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):#No. of columns in a given row
                turn = self.board[r][c][0]
                if (turn=="w" and self.whiteTomove) or (turn=="b" and not self.whiteTomove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)#Calls the appropriate move function

        return moves

    ##Get all the pawn moves for the pawn located at row and col and store these moves in this list
    def getPawnMoves(self,r,c,moves):
        if self.whiteTomove:#White to move
            if self.board[r-1][c] == '--':#Checks if the next pawn sqaure is empty
                moves.append(Move((r,c), (r-1,c), self.board))
                if r==6 and self.board[r-2][c]=='--':#2 sqaure pawn advance
                    moves.append(Move((r,c),(r-2,c), self.board))
            if c-1 >=0:#Captures left
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1,c-1), self.board))
                elif (r-1,c-1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r-1,c-1), self.board, isEnpassantMove=True))
            if c+1<=7:#Captures right
                if self.board[r-1][c+1][0]=='b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1,c+1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r-1,c+1), self.board, isEnpassantMove=True))

        else:#black pawn moves
            if self.board[r+1][c]=='--':#1 sqaure pawn advance
                moves.append(Move((r,c), (r+1,c), self.board))
                if r==1 and self.board[r+2][c]=='--':#2 square pawn advance
                    moves.append(Move((r,c), (r+2,c), self.board))
            if c-1 >= 0:#Captures Right
                if self.board[r+1][c-1][0]=='w':
                    moves.append(Move((r,c),(r+1, c-1), self.board))
                elif (r+1,c-1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r+1,c-1), self.board, isEnpassantMove=True))
            if c+1 <= 7:#Captures Left
                if self.board[r+1][c+1][0]=='w':
                    moves.append(Move((r,c), (r+1, c+1), self.board))
                elif (r+1,c+1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r+1,c+1), self.board, isEnpassantMove=True))

    ##Get all the Rook moves
    def getRookMoves(self,r,c,moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1))#up, left, down, right
        enemyColor = 'b' if self.whiteTomove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #Valid move when empty space
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #Capturing enemy piece
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else: #Invalid friendly piece
                        break
                else:#Out of bounds
                    break


    ##Get all the Knight moves
    def getKnightMoves(self,r,c,moves):
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor = "w" if self.whiteTomove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #enemy Color
                    moves.append(Move((r,c), (endRow, endCol), self.board))

    ##Get all the Bishop moves
    def getBishopMoves(self,r,c,moves):
        directions = ((-1,-1),(-1,1),(1,-1),(1,1))#4 diagonal directions
        allyColor = "w" if self.whiteTomove else "b"
        for d in directions:
            for i in range(1,8):
                endRow = r+d[0]*i
                endCol = c+d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space valid
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] != allyColor:#Captures enemy piece
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:#Friendly piece
                        break
                else:#
                    break
    ##Get all the Queen moves
    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c, moves)

    ##Get all the King moves
    def getKingMoves(self,r,c,moves):
        kingMoves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor = "w" if self.whiteTomove else "b"
        for i in range(8):
            endRow = r+kingMoves[i][0]
            endCol = c+kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c), (endRow, endCol), self.board))
        #self.getCastleMoves(r,c,moves)

    #Generate all valid castle moves for the king at (r,c) and add them to the list of moves
    #def getCastleMoves(self,r,c,moves):
     #   if self.squareUnderAttack(r,c):
      #      return#cannot castle while in check
       # if (self.whiteTomove and self.currentCastlingRight.wks) or (not self.whiteTomove and self.currentCastlingRight.bks):
        #    self.getKingsideCastleMoves(r,c,moves)
        #if (self.whiteTomove and self.currentCastlingRight.wqs) or (not self.whiteTomove and self.currentCastlingRight.bqs):
         #   self.getQueensideCastleMoves(r,c,moves)
        
    #def getKingsideCastleMoves(self,r,c,moves):
     #   if self.board[r][c+1] == '--' and self.board[r][c+2]=='--':
      #      if not self.squareUnderAttack(r,c+1) and not self.squareUnderAttack(r,c+2):
       #         moves.append(Move((r,c), (r,c+2), self.board, isCastleMove=True))

    #def getQueensideCastleMoves(self,r,c,moves):
     #   if self.board[r][c-1]=='--' and self.board[r][c-2]=='--' and self.board[r][c-3]:
      #      if not self.squareUnderAttack(r,c-1) and not self.squareUnderAttack(r,c-2):
       #         moves.append(Move((r,c),(r,c-2), self.board, isCastleMove=True))
'''
class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
'''
class Move():
    #Maps keys to values
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False):#, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        #Pawn Promotion
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved=='bp' and self.endRow==7):
            self.isPawnPromotion = True
        #en passant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        
        #castle move
        #self.isCastleMove = isCastleMove

    
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol

    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]

    def getChessNotation(self):
        ##transition from starting place to the next move
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    