from pieces.base import Piece
from pieces.bishop import Bishop
from pieces.rook import Rook
from loader import GetSprite

class Queen(Bishop, Rook, Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.code = 'q'
        self.value = 90 if color ==0 else -90
        self.sprite = GetSprite(self)
        self.previousMove = None
    
    def GetMoves(self, board):
        bishop_moves, bishop_captures = self.DiagonalMoves(board)
        rook_moves, rook_captures = self.VertHorzMoves(board)
        moves = bishop_moves + rook_moves
        captures = bishop_captures + rook_captures
        return moves, captures