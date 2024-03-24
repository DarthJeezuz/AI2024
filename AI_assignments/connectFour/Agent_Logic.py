import random
import math

#_________________Uniform Random (UR)___________________________________
def uniform_random_move(game, player):
    valid_moves = [col for col in range(game.columns) if game.is_valid_move(col)]
    if not valid_moves:
        return None  # No valid moves available
    return random.choice(valid_moves)

#_________________Pure Monte Carlo Game Search (PMCGS)_______________________
def pmcgs_move(game, player, num_simulations, verbose=False):
    outcomes = {col: {'wins': 0, 'sims': 0} for col in range(game.columns)}

    for col in range(game.columns):
        if game.is_valid_move(col):
            for _ in range(num_simulations):
                simulation_game = game.copy()
                simulation_game.make_move(col, player)
                result = simulate_random_game(simulation_game, player)

                # Update wins and simulations count
                outcomes[col]['wins'] += result if player == 'Y' else -result
                outcomes[col]['sims'] += 1

                if verbose:
                    print(f"Move: {col+1}, wi: {outcomes[col]['wins']}, ni: {outcomes[col]['sims']}, NODE ADDED")

                    # Assuming the game has a method to determine if it's in a terminal state
                    if simulation_game.is_terminal_state():
                        terminal_value = 1 if simulation_game.check_win(player) else -1 if simulation_game.check_win(game.opposite_player(player)) else 0
                        print(f"TERMINAL NODE VALUE: {terminal_value}")
                        print(f"Updated values: wi: {outcomes[col]['wins']}, ni: {outcomes[col]['sims']}")

    # Choose the best move
    best_move, best_avg_outcome = max(outcomes.items(), key=lambda x: x[1]['wins'] / x[1]['sims'] if x[1]['sims'] > 0 else float('-inf'))

    # Output the values for each move if in verbose mode
    if verbose:
        for col, outcome in outcomes.items():
            avg_outcome = outcome['wins'] / outcome['sims'] if outcome['sims'] > 0 else None
            print(f"Column {col + 1}: {'Null' if avg_outcome is None else avg_outcome}")

    return best_move if outcomes[best_move]['sims'] > 0 else None

def simulate_random_game(game, player):
    current_player = player
    while not game.is_terminal_state():
        valid_moves = [col for col in range(game.columns) if game.is_valid_move(col)]
        if not valid_moves:  # No valid moves
            break
        move = random.choice(valid_moves)
        game.make_move(move, current_player)
        current_player = game.opposite_player(current_player)

    # Game outcome from the perspective of the 'player'
    if game.check_win(player):
        return 1
    elif game.check_win(game.opposite_player(player)):
        return -1
    else:
        return 0


#________________Upper Confidence Bound for Trees (UCT)__________________
class UCTNode:
    def __init__(self, game, move=None, parent=None, player='Y'):
        self.game = game
        self.move = move  # The move that led to this node
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = [col for col in range(game.columns) if game.is_valid_move(col)]
        self.player = player  # The player who will move in this node

    def is_terminal(self):
        # Check if the game state is a terminal state
        return self.game.check_win('Y') or self.game.check_win('R') or self.game.is_draw()

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def ucb1(self, explore_param=1.41):
        # Avoid division by zero and log of zero by treating unvisited nodes with high exploration value
        if self.visits == 0:
            return float('inf')
        if self.parent is None or self.parent.visits == 0:
            # Just in case, though parent visits should never be 0 if this node has been visited.
            return float('inf')
        return self.wins / self.visits + explore_param * math.sqrt(math.log(self.parent.visits) / self.visits)

    def select_child(self):
        # Select a child node with the highest UCB1 value
        return max(self.children, key=lambda c: c.ucb1())

    def add_child(self, move):
        # Assume new_game_state is correctly updated with the move
        new_game_state = self.game.copy()
        new_game_state.make_move(move, self.game.opposite_player(self.player))
        child_node = UCTNode(new_game_state, move, self, self.game.opposite_player(self.player))
        self.children.append(child_node)
        self.untried_moves.remove(move)
        return child_node

    def update(self, result):
        # Update this node's data from the simulation result
        self.visits += 1
        self.wins += result if self.player == 'Y' else -result

    def best_move(self):
        # Select the child with the highest win rate
        # Give default value if visits are zero
        best_child = max(self.children, key=lambda c: c.wins / c.visits if c.visits > 0 else float('-inf'))
        return best_child.move, best_child.wins / best_child.visits if best_child.visits > 0 else float('-inf')

def uct_move(game, player, num_simulations, verbose=False):
    root = UCTNode(game, None, None, player)

    for _ in range(num_simulations):
        node = root
        # Selection
        path = []  # To keep track of the path for verbose output
        while not node.is_terminal() and node.is_fully_expanded():
            node = node.select_child()
            path.append(node)
            if verbose:
                print(f"wi: {node.wins}, \nni: {node.visits}")

        # Expansion
        if not node.is_fully_expanded():
            move = random.choice(node.untried_moves)
            node = node.add_child(move)
            if verbose:
                print(f"Expanded node with move: {move + 1} (0-index corrected to 1-index for display)")
                print("NODE ADDED")

        # Simulation
        result = simulate_random_game(node.game, player)
        if verbose:
            print(f"Simulation result: {result}")

        # Backpropagation
        for node in reversed(path):  # Go back through the path
            node.update(result)
            if verbose:
                print(f"Backpropagated node: {node}, Updated wins: {node.wins}, Updated visits: {node.visits}")

    # Determine the best move
    best_move, best_value = root.best_move()
    if verbose:
        print("Final Values:")
        for child in root.children:
            print(f"wi: {child.wins}, \nni: {child.visits}, \nValue: {child.wins / child.visits if child.visits > 0 else 'Null'}, \nMove selected: {child.move + 1}\n")
        print(f"FINAL Move selected: {best_move + 1}")

    return best_move
