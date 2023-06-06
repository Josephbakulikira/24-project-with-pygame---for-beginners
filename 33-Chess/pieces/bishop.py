from pieces.base import Piece
from loader import GetSprite

class Bishop(Piece):
    def __init__(self, position, color):
        super().__init__(position,color)
        self.code = 'b'
        self.value = 30 if color == 0 else -30
        self.sprite = GetSprite(self)
        self.previousMove = None
        self.pieceMap = []

    def GetMoves(self, board):
        moves, captures = self.DiagonalMoves(board)
        return moves, captures
    
    def DiagonalMoves(self, board):
        patterns = ((-1, -1), (1, 1), (1, -1), (-1, 1))
        moves, captures = self.GetPatterMoves(board, patterns)
        return moves, captures
