from pieces.base import Piece
from loader import GetSprite

class Rook(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.code = 'r'
        self.value = 50 if color == 0 else -50
        self.sprite = GetSprite(self)
        self.previousMove = None
    
    def GetMoves(self, board):
        moves, captures = self.VertHorzMoves(board)
        return moves, captures
    
    def VertHorzMoves(self, board):
        patterns = ((-1, 0), (1, 0), (0, 1), (0, -1))
        return self.GetPatterMoves(board, patterns)