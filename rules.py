SIZE = 8


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end

    piece = board[sr][sc]

    # Normal piece: moves only forward
    if piece == player:
        direction = -1 if player == "R" else 1

        return (
            board[er][ec] == "." and
            abs(er - sr) == 1 and
            abs(ec - sc) == 1 and
            er - sr == direction
        )

    # King: moves in both directions
    if piece == player + "K":
        return (
            board[er][ec] == "." and
            abs(er - sr) == 1 and
            abs(ec - sc) == 1
        )

    return False


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end

    piece = board[sr][sc]
    mr = (sr + er) // 2
    mc = (sc + ec) // 2

    # Normal piece: captures only forward
    if piece == player:
        direction = -1 if player == "R" else 1

        return (
            board[er][ec] == "." and
            abs(er - sr) == 2 and
            abs(ec - sc) == 2 and
            er - sr == 2 * direction and
            board[mr][mc] not in (".", player, player + "K")
        )

    # King: captures in both directions
    if piece == player + "K":
        return (
            board[er][ec] == "." and
            abs(er - sr) == 2 and
            abs(ec - sc) == 2 and
            board[mr][mc] not in (".", player, player + "K")
        )

    return False


def promote(board):
    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"

        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"