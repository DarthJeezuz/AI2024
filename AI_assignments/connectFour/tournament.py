from Game_Logic import ConnectFour
from Agent_Logic import uniform_random_move, pmcgs_move, uct_move

# Function to simulate a game between two algorithms
def play_game(algo1, algo2, num_simulations1, num_simulations2):
    game = ConnectFour()  # Create an empty board by default
    current_algo = algo1
    current_sims = num_simulations1
    player = 'Y'  # Player 'Y' always starts

    while not game.is_terminal_state():
        # Select the move based on the current algorithm and its parameters
        move = current_algo(game, player, current_sims) if current_algo != uniform_random_move else current_algo(game, player)

        # Apply the move to the game state
        if move is not None and game.is_valid_move(move):
            game.make_move(move, player)
            if game.check_win(player):  # Efficient win check focused on last move
                game.undo_move()
                return 1 if player == 'Y' else -1
            game.undo_move()  # Revert the move after checking
        else:
            print("Invalid move detected")
            break

        # Switch player and algorithm for the next turn
        player = 'R' if player == 'Y' else 'Y'
        current_algo, current_sims = (algo2, num_simulations2) if current_algo == algo1 else (algo1, num_simulations1)

    return 0  # If the game ends in a draw

def update_results(results, name1, name2, outcome):
    if outcome == 1:  # algo1 wins
        results[name1][name2]['wins'] += 1
        results[name2][name1]['losses'] += 1
    elif outcome == -1:  # algo2 wins
        results[name1][name2]['losses'] += 1
        results[name2][name1]['wins'] += 1
    else:  # draw
        results[name1][name2]['draws'] += 1
        results[name2][name1]['draws'] += 1

def run_tournament():
    algorithms = [
        ('UR', uniform_random_move, 0),
        ('PMCGS-500', pmcgs_move, 500),
        ('PMCGS-10000', pmcgs_move, 10000),
        ('UCT-500', uct_move, 500),
        ('UCT-10000', uct_move, 10000),
    ]

    results = {algo[0]: {other_algo[0]: {'wins': 0, 'losses': 0, 'draws': 0} for other_algo in algorithms} for algo in algorithms}

    for i, (name1, algo1, sims1) in enumerate(algorithms):
        for j, (name2, algo2, sims2) in enumerate(algorithms):
            if i != j:
                for _ in range(100):  # Range = number of games
                    result = play_game(algo1, algo2, sims1, sims2)
                    update_results(results, name1, name2, result) # Update results based on the outcome

    # Calculate and print winning percentages
    for algo in results:
        total_wins = sum(match['wins'] for match in results[algo].values())
        total_losses = sum(match['losses'] for match in results[algo].values())
        total_draws = sum(match['draws'] for match in results[algo].values())
        total_games = total_wins + total_losses + total_draws
        win_rate = total_wins / total_games * 100 if total_games > 0 else 0
        print(f"{algo} - Win rate: {win_rate:.2f}%, Wins: {total_wins}, Losses: {total_losses}, Draws: {total_draws}")


if __name__ == "__main__":
    run_tournament()
