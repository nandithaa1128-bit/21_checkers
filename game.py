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

    def has_capture(self, player):
        for sr in range(SIZE):
            for sc in range(SIZE):
                if self.board[sr][sc] not in (player, player + "K"):
                    continue

                for er in range(SIZE):
                    for ec in range(SIZE):
                        if capture_move(
                            self.board,
                            player,
                            (sr, sc),
                            (er, ec)
                        ):
                            return True

        return False

    def has_legal_move(self, player):
        for sr in range(SIZE):
            for sc in range(SIZE):
                if self.board[sr][sc] not in (player, player + "K"):
                    continue

                for er in range(SIZE):
                    for ec in range(SIZE):
                        if capture_move(
                            self.board,
                            player,
                            (sr, sc),
                            (er, ec)
                        ):
                            return True

                        if simple_move(
                            self.board,
                            player,
                            (sr, sc),
                            (er, ec)
                        ):
                            return True

        return False

    def has_piece_capture(self, player, position):
        sr, sc = position

        for er in range(SIZE):
            for ec in range(SIZE):
                if capture_move(
                    self.board,
                    player,
                    (sr, sc),
                    (er, ec)
                ):
                    return True

        return False

    def make_capture(self, start, end):
        sr, sc = start
        er, ec = end

        move_piece(self.board, start, end)

        # Remove the jumped opponent piece.
        mr = (sr + er) // 2
        mc = (sc + ec) // 2
        self.board[mr][mc] = "."

    def check_promotion(self, player, position):
        r, c = position

        before = self.board[r][c]

        promote(self.board)

        after = self.board[r][c]

        return before == player and after == player + "K"

    def run(self):
        print("Checkers — move: sr sc er ec")

        while True:
            self.print_board()

            raw = input(
                f"{self.player}> "
            ).strip().lower().split()

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

            if not all(
                0 <= x < SIZE
                for x in (sr, sc, er, ec)
            ):
                print("Outside board.")
                continue

            if self.board[sr][sc] not in (
                self.player,
                self.player + "K"
            ):
                print("That is not your piece.")
                continue

            start = (sr, sc)
            end = (er, ec)

            # Check whether any capture is available.
            must_capture = self.has_capture(self.player)

            # -------------------------------------------------
            # CAPTURE
            # -------------------------------------------------
            if capture_move(
                self.board,
                self.player,
                start,
                end
            ):
                self.make_capture(start, end)

                print(
                    f"{self.player} captured from "
                    f"({sr}, {sc}) to ({er}, {ec})."
                )

                # Check promotion after capture.
                was_promoted = self.check_promotion(
                    self.player,
                    end
                )

                if was_promoted:
                    print(
                        f"{self.player} piece promoted to king."
                    )

                current_position = end

                # -------------------------------------------------
                # MULTIPLE CAPTURE
                # -------------------------------------------------
                while self.has_piece_capture(
                    self.player,
                    current_position
                ):
                    self.print_board()

                    raw = input(
                        f"{self.player} must continue capturing "
                        f"(sr sc er ec)> "
                    ).strip().lower().split()

                    if raw == ["q"]:
                        return

                    if len(raw) != 4:
                        print("Enter four coordinates.")
                        continue

                    try:
                        nsr, nsc, ner, nec = map(int, raw)
                    except ValueError:
                        print("Coordinates must be numbers.")
                        continue

                    if not all(
                        0 <= x < SIZE
                        for x in (nsr, nsc, ner, nec)
                    ):
                        print("Outside board.")
                        continue

                    if (nsr, nsc) != current_position:
                        print(
                            "You must continue with the same piece."
                        )
                        continue

                    next_start = (nsr, nsc)
                    next_end = (ner, nec)

                    if not capture_move(
                        self.board,
                        self.player,
                        next_start,
                        next_end
                    ):
                        print(
                            "Another capture is available. "
                            "You must capture."
                        )
                        continue

                    self.make_capture(
                        next_start,
                        next_end
                    )

                    print(
                        f"{self.player} captured from "
                        f"({nsr}, {nsc}) to "
                        f"({ner}, {nec})."
                    )

                    was_promoted = self.check_promotion(
                        self.player,
                        next_end
                    )

                    if was_promoted:
                        print(
                            f"{self.player} piece promoted to king."
                        )

                    current_position = next_end

            # -------------------------------------------------
            # NORMAL MOVE
            # -------------------------------------------------
            elif simple_move(
                self.board,
                self.player,
                start,
                end
            ):
                if must_capture:
                    print(
                        "A capture is available. "
                        "You must capture."
                    )
                    continue

                move_piece(
                    self.board,
                    start,
                    end
                )

                print(
                    f"{self.player} moved from "
                    f"({sr}, {sc}) to ({er}, {ec})."
                )

                was_promoted = self.check_promotion(
                    self.player,
                    end
                )

                if was_promoted:
                    print(
                        f"{self.player} piece promoted to king."
                    )

            # -------------------------------------------------
            # INVALID MOVE
            # -------------------------------------------------
            else:
                print("Invalid move.")
                continue

            # -------------------------------------------------
            # CHECK GAME END
            # -------------------------------------------------

            opponent = (
                "B"
                if self.player == "R"
                else "R"
            )

            if not self.has_pieces(opponent):
                self.print_board()
                print(
                    f"{self.player} wins! "
                    f"{opponent} has no pieces."
                )
                return

            if not self.has_legal_move(opponent):
                self.print_board()
                print(
                    f"{self.player} wins! "
                    f"{opponent} has no legal moves."
                )
                return

            # Switch turn only after the complete
            # capture sequence is finished.
            self.player = opponent