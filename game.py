from board import initial_board, move_piece, SIZE
from rules import simple_move, capture_move, promote


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"

    def print_board(self):
        print("\n   " + " ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(row))

    def has_pieces(self, player):
        return any(
            cell in (player, player + "K")
            for row in self.board
            for cell in row
        )

    def has_legal_move(self, player):
        for sr in range(SIZE):
            for sc in range(SIZE):
                if self.board[sr][sc] not in (player, player + "K"):
                    continue

                for er in range(SIZE):
                    for ec in range(SIZE):
                        if capture_move(self.board, player, (sr, sc), (er, ec)):
                            return True
                        if simple_move(self.board, player, (sr, sc), (er, ec)):
                            return True

        return False

    def run(self):
        print("Checkers — move: sr sc er ec")
        while True:
            self.print_board()
            raw = input(f"{self.player}> ").strip().lower().split()
            if raw == ["q"]:
                return
            if len(raw) != 4:
                print("Enter four coordinates.")
                continue
            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue
            if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
                print("Outside board.")
                continue
            if self.board[sr][sc] not in (self.player, self.player + "K"):
                print("That is not your piece.")
                continue

            start, end = (sr, sc), (er, ec)
            if capture_move(self.board, self.player, start, end):
                move_piece(self.board, start, end)
                mr = (sr + er) // 2
                mc = (sc + ec) // 2
                self.board[mr][mc] = "."
            elif simple_move(self.board, self.player, start, end):
                move_piece(self.board, start, end)
            else:
                print("Invalid move.")
                continue

            promote(self.board)
            opponent = "B" if self.player == "R" else "R"

            if not self.has_pieces(opponent):
                self.print_board()
                print(f"{self.player} wins! {opponent} has no pieces.")
                return

            if not self.has_legal_move(opponent):
                self.print_board()
                print(f"{self.player} wins! {opponent} has no legal moves.")
                return

            self.player = opponent