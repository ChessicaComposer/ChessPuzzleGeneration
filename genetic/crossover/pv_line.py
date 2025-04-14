from genetic.crossover.singlepoint import SinglePoint
from .. chromosome import IntBoard
from genetic.utility import chess_int_to_board
import chess

# Take another input when initializing to save the pv-line
# Get the pv-line from chess engine by either making a function or setting a retrievable field in the file
# Looks like changes in Genetic are necessary in order to pass the moves into this class (ugly checks might be necessary too)
class PvLine(SinglePoint):
    def __init__(self):
        super().__init__()
    
    def _mate(self, parent1: IntBoard, parent2: IntBoard) -> list[IntBoard]:
        
        # Find the pieces and 
        parent1_pieces, parent1_squares = self._find_pieces(parent1.board,parent1.moves)
        parent2_pieces, parent2_squares = self._find_pieces(parent2.board,parent2.moves)
        
        # Swap the pieces of each parents PV-line
        for piece, square in zip(parent2_pieces, parent1_squares):
            if self.test_insertion(piece, square, parent1.body[::]): 
                parent1.body[square] = piece
        for piece, square in zip(parent1_pieces, parent2_squares):
            if self.test_insertion(piece, square, parent2.body[::]): 
                parent2.body[square] = piece
        # Return the parents after the modifications
        return [IntBoard(parent1.body[::]), IntBoard(parent2.body[::])]
    
    def _find_pieces(self, board, moves) -> tuple[set[chess.Piece], set[chess.square]]:
        board_copy = chess.Board(board)
        pieces = set()
        replacement_squares = set()
        for move in moves:
            moved_piece = board_copy.piece_at(move.from_square)
            # Do not crossover kings DANGER
            if not moved_piece.piece_type == chess.KING and moved_piece.color == chess.WHITE:
                pieces.add(moved_piece.piece_type)
                replacement_squares.add(move.from_square)
            board_copy.push(move)
        return pieces, replacement_squares
    
    # This check is pretty expensive ngl (luckily our longest line is going to be 5 in the worst case)
    def test_insertion(self, piece, square, parent_int_board: IntBoard) -> bool:
        parent_int_board[square] = piece
        board = chess_int_to_board(parent_int_board)
        return board.is_valid()