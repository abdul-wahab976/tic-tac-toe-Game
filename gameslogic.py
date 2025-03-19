# tictactoe.py

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """Returns the initial empty board (a 3x3 grid)."""
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """Returns the player who has the next turn (X or O)."""
    x_count = sum([row.count(X) for row in board])
    o_count = sum([row.count(O) for row in board])
    return X if x_count <= o_count else O

def terminal(board):
    """Returns True if the game is over (win, loss, or draw)."""
    return winner(board) is not None or all(all(cell is not EMPTY for cell in row) for row in board)

def winner(board):
    """Returns the winner of the game (X, O, or None)."""
    # Check rows, columns, and diagonals
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not EMPTY:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]
    return None

def result(board, action):
    """Returns the board resulting from making move 'action' on 'board'."""
    i, j = action
    if board[i][j] is not EMPTY:
        raise ValueError("Invalid move.")
    new_board = [row.copy() for row in board]
    new_board[i][j] = player(board)
    return new_board

def minimax(board):
    """Returns the best move for the AI using the minimax algorithm."""
    def max_value(board):
        if terminal(board):
            return utility(board)
        v = float('-inf')
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

    def min_value(board):
        if terminal(board):
            return utility(board)
        v = float('inf')
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v

    def utility(board):
        """Returns +1 if X wins, -1 if O wins, and 0 for a tie."""
        win = winner(board)
        if win == X:
            return 1
        elif win == O:
            return -1
        return 0

    def actions(board):
        """Returns all possible actions (empty positions)."""
        return [(i, j) for i in range(3) for j in range(3) if board[i][j] is EMPTY]

    best_move = None
    if player(board) == X:
        best_value = float('-inf')
        for action in actions(board):
            move_value = min_value(result(board, action))
            if move_value > best_value:
                best_value = move_value
                best_move = action
    else:
        best_value = float('inf')
        for action in actions(board):
            move_value = max_value(result(board, action))
            if move_value < best_value:
                best_value = move_value
                best_move = action
    return best_move
