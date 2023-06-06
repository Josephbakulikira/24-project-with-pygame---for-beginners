import pygame
import math
from position import Position
from fen import FEN
from pieces import *

class Board:
    def __init__(self):
        # 0 -> white, 1 -> black
        self.player = 0
        self.historic = []
        self.move_index = 1
        self.font = pygame.font.SysFont("Consolas", 18, bold=True)
        self.grid = FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

        self.WhiteKing = None
        self.BlackKing = None
        
        # Initialize our kings
        for pieces in self.grid:
            for piece in pieces:
                if piece != None and piece.code == 'k':
                    if piece.color == 0:
                        self.WhiteKing = piece
                    elif piece.color == 1:
                        self.BlackKing = piece

        self.checkWhiteKing = False
        self.checkBlackKing = False

        self.winner = None
        self.pieceToPromote = None

        # Promotions -> Queen, Rook, Bishop, Knight
        self.whitePromotions = [Queen(Position(0, 0), 0), Bishop(Position(0, 1), 0), Knight(Position(0, 2), 0), Rook(Position(0, 3), 0)]
        self.blackPromotions = [Rook(Position(0, 7), 1), Knight(Position(0, 6), 1), Bishop(Position(0, 5), 1), Queen(Position(0, 4), 1)]
    
    def GetPiece(self, position):
        return self.grid[position.x][position.y]
    
    def SetPiece(self, position, piece):
        self.grid[position.x][position.y] = piece
    
    def SwitchTurn(self):
        # switch turn between 0 and 1
        # ( 0 + 1) * -1 + 2 = 1
        # ( 2 + 1) * -1 + 2 = 0
        self.player = (self.player + 1) * -1 + 2
        # Check if the player lost or not
        self.IsCheckmate()
    
    def RecentMove(self):
        return None if not self.historic else self.historic[-1]
    
    def RecentMovePositions(self):
        if not self.historic or len(self.historic) <= 1:
            return None, None
        pos = self.historic[-1][3]
        oldPos = self.historic[-1][4]

        return pos.GetCopy(), oldPos.GetCopy()
    
    def AllowedMoveList(self, piece, moves):
        allowed_moves = []
        for move in moves:
            if self.VerifyMove(piece, move.GetCopy()):
                allowed_moves.append(move.GetCopy())
        return allowed_moves
    
    def GetAllowedMoves(self, piece):
        moves, captures = piece.GetMoves(self)
        allowed_moves = self.AllowedMoveList(piece, moves)
        allowed_captures = self.AllowedMoveList(piece, captures)
        return allowed_moves, allowed_captures
    
    def Move(self, piece, position):
        if position != None:
            position = position.GetCopy()
            # print(position)
            if self.isCastling(piece, position.GetCopy()):
                self.castleKing(piece, position.GetCopy())
            elif self.isEnPassant(piece, position.GetCopy()):
                self.grid[position.x][piece.position.y] = None
                self.MovePiece(piece, position)
                self.historic[-1][2] = piece.code + " EP"
            else:
                self.MovePiece(piece, position)
            # Check for promotion
            if type(piece) == Pawn and (piece.position.y == 0 or piece.position.y == 7):
                self.pieceToPromote = piece
            else:
                self.SwitchTurn()
            self.Check()
        
    def MovePiece(self, piece, position):
        position = position.GetCopy()
        self.grid[piece.position.x][piece.position.y] = None
        oldPosition = piece.position.GetCopy()
        piece.updatePosition(position)
        self.grid[position.x][position.y] = piece
        self.historic.append([self.move_index, piece.color, piece.code, oldPosition, piece.position, piece])
        piece.previousMove = self.move_index
        self.move_index = self.move_index
        self.move_index += 1
        self.checkBlackKing = False
        self.checkWhiteKing = False
    
    def VerifyMove(self, piece, move):
        # verify the move by going through all the possible outcomes
        # This function will return False if the opponent will reply by capturing the king
        position = move.GetCopy()
        oldPosition = piece.position.GetCopy()
        captureEnPassant = None
        # print(f"new: {move}, old: {oldPosition}")
        capturedPiece = self.grid[position.x][position.y]
        if self.isEnPassant(piece, position):
            captureEnPassant = self.grid[position.x][oldPosition.y]
            self.grid[position.x][oldPosition.y] = None

        self.grid[oldPosition.x][oldPosition.y] = None
        self.grid[position.x][position.y] = piece
        # print(f"pos: {position}, old: {oldPosition}")
        piece.updatePosition(move)
        EnemyCaptures = self.GetEnemyCaptures(self.player)
        if self.isCastling(piece, oldPosition):
            if math.fabs(position.x - oldPosition.x) == 2 and not self.VerifyMove(piece, Position(5, position.y)) \
                or math.fabs(position.x - oldPosition.x) == 3 and not self.VerifyMove(piece, Position(3, position.y)) \
                or self.IsInCheck(piece):
                self.UndoMove(piece, capturedPiece, oldPosition, position)
                return False

        for pos in EnemyCaptures:
            if (self.WhiteKing.position == pos and piece.color == 0) \
                or (self.BlackKing.position == pos and piece.color == 1):
                self.UndoMove(piece, capturedPiece, oldPosition, position)
                if captureEnPassant != None:
                    self.grid[position.x][oldPosition.y] = captureEnPassant
                return False
        self.UndoMove(piece, capturedPiece, oldPosition, position)
        if captureEnPassant != None:
            self.grid[position.x][oldPosition.y] = captureEnPassant
        return True
    
    def UndoMove(self, piece, captured, oldPos, pos):
        self.grid[oldPos.x][oldPos.y] = piece
        self.grid[pos.x][pos.y] = captured
        piece.updatePosition(oldPos)
    
    def GetEnemyCaptures(self, player):
        captures = []
        for pieces in self.grid:
            for piece in pieces:
                if piece != None and piece.color != player:
                    _ , pieceCaptures = piece.GetMoves(self)
                    captures = captures + pieceCaptures
        return captures
    
    def isCastling(self, king, position):
        return type(king) == King and abs(king.position.x - position.x) > 1
    
    def isEnPassant(self, piece, newPos):
        if type(piece) != Pawn:
            return False
        moves = None
        if piece.color == 0:
            moves = piece.EnPassant(self, -1)
        else:
            moves = piece.EnPassant(self, 1)
        return newPos in moves
    
    def IsInCheck(self, piece):
        return type(piece) == King and \
            ((piece.color == 0 and self.checkWhiteKing) or (piece.color == 1 and self.checkBlackKing))

    def castleKing(self, king, position):
        position = position.GetCopy()
        if position.x == 2 or position.x == 6:
            if position.x == 2:
                rook = self.grid[0][king.position.y]
                self.MovePiece(king, position)
                self.grid[0][rook.position.y] = None
                rook.position.x = 3
            else:
                rook = self.grid[7][king.position.y]
                self.MovePiece(king, position)
                self.grid[7][rook.position.y] = None
                rook.position.x = 5
            
            rook.previousMove = self.move_index - 1
            self.grid[rook.position.x][rook.position.y] = rook
            self.historic[-1][2] = king.code + " C"
            # Play castle sound here
    
    def PromotePawn(self, pawn, choice):
        if choice == 0:
            self.grid[pawn.position.x][pawn.position.y] = Queen(pawn.position.GetCopy(), pawn.color)
        elif choice == 1:
            self.grid[pawn.position.x][pawn.position.y] = Bishop(pawn.position.GetCopy(), pawn.color)
        elif choice == 2:
            self.grid[pawn.position.x][pawn.position.y] = Knight(pawn.position.GetCopy(), pawn.color)
        elif choice == 3:
            self.grid[pawn.position.x][pawn.position.y] = Rook(pawn.position.GetCopy(), pawn.color)
        
        self.SwitchTurn()
        self.Check()
        self.pieceToPromote = None
    
    def Check(self):
        if self.player == 0:
            king = self.WhiteKing
        else:
            king = self.BlackKing
        
        for pieces in self.grid:
            for piece in pieces:
                if piece != None and piece.color != self.player:
                    moves, captures = self.GetAllowedMoves(piece)
                    if king.position in captures:
                        if self.player == 1:
                            self.checkBlackKing = True
                            return
                        else:
                            self.checkWhiteKing = True
                            return
    
    def IsCheckmate(self):
        for pieces in self.grid:
            for piece in pieces:
                if piece != None and piece.color == self.player:
                    moves, captures = self.GetAllowedMoves(piece)
                    # If there's still a legal move left
                    # Then it's not checkmate
                    if moves or captures:
                        return False
        self.Check()
        if self.checkWhiteKing:
            self.winner = 1
        elif self.checkBlackKing:
            self.winner = 0
        else:
            self.winner = -1
        return True







        