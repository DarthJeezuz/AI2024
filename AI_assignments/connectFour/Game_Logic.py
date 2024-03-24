# Jesus Oropeza
#
# AI CS 4320
class ConnectFour:
    def __init__(self, board=None):
        self.rows = 6
        self.columns = 7
        self.board = board if board else [['O'] * 7 for _ in range(6)]
        self.last_move = None  # Stores the last move made as a tuple (column, row)


    def is_valid_move(self, column):
        return self.board[0][column] == 'O'

    def make_move(self, column, player):
        for row in range(self.rows):
            if self.board[row][column] == 'O':  # Empty cell
                self.board[row][column] = player
                self.last_move = (column, row)  # Update last_move
                return True  # Move was successful
        return False  # Column is full

    def undo_move(self):
        if self.last_move is None:
            return  # No move to undo

        column, row = self.last_move
        self.board[row][column] = 'O'  # Remove the piece
        self.last_move = None  # Reset last move

    def opposite_player(self, player):
        return 'Y' if player == 'R' else 'R'
    
    def check_win(self, player):
        
        if self.last_move is None:
            return False # No moves have been made yet
        
        # Check horizontal, vertical, and diagonal for a winning line
        col, row = self.last_move
        # Horizontal check
        count = 0
        for c in range(self.columns):
            count = count + 1 if self.board[row][c] == player else 0
            if count >= 4: return True

        # Vertical check
        count = 0
        for r in range(self.rows):
            count = count + 1 if self.board[r][col] == player else 0
            if count >= 4: return True

        # Diagonal checks
        for dr, dc in [(1, 1), (1, -1)]:  # Down-right and down-left
            count = 0
            r, c = row, col
            while 0 <= r < self.rows and 0 <= c < self.columns:
                count = count + 1 if self.board[r][c] == player else 0
                if count >= 4: return True
                r += dr
                c += dc

        return False

    def is_draw(self):
        return all(self.board[0][col] != 'O' for col in range(self.columns))

    def is_terminal_state(self):
        return self.check_win('R') or self.check_win('Y') or self.is_draw()
    
    def copy(self):
        return ConnectFour([row[:] for row in self.board])
