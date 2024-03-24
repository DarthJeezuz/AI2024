import sys
from Game_Logic import ConnectFour
from Agent_Logic import uniform_random_move, pmcgs_move, uct_move

def read_game_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        algorithm = lines[0].strip()
        current_player = lines[1].strip()
        board = [list(line.strip()) for line in lines[2:8]]

    return algorithm, current_player, board

def execute_algorithm(algorithm, board, player, num_simulations, verbose):
    game = ConnectFour(board)
    
    if algorithm == 'UR':
        move = uniform_random_move(game, player)
    elif algorithm.startswith('PMCGS'):
        move = pmcgs_move(game, player, int(num_simulations), verbose)
    elif algorithm.startswith('UCT'):
        move = uct_move(game, player, int(num_simulations), verbose)
    else:
        raise ValueError("Unknown algorithm")

    return move


def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <file_path> <verbosity> <num_simulations>")
        return
    
    file_path = sys.argv[1]
    verbosity = sys.argv[2]
    num_simulations = sys.argv[3]
    verbose = verbosity == "Verbose"
    algorithm, player, board = read_game_file(file_path)
    move = execute_algorithm(algorithm, board, player, num_simulations, verbose)
    
    if verbose:
        print(f"Move selected: {move}")

if __name__ == "__main__":
    main()