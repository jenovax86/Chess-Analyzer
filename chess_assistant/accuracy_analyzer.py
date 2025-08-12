from io import StringIO
import chess.engine
import chess.pgn
import pandas as pd
import chess

CSV = pd.read_csv("../data/data.csv")
CENTI_PAWN_LOSS_THRESHOLD = 50
ANALYZE_DEPTH = 23
ENGINE_PATH = r"../stockfish/stockfish-windows-x86-64-avx2.exe"

Engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)


def calculate_centi_pawn_loss(analyze, target_color):
    return (
        analyze["score"].white().score(mate_score=1000)
        if target_color == "white"
        else analyze["score"].black().score(mate_score=1000)
    )


def adapt_turn(turn):
    if turn:
        return "white"
    return "black"


def is_pgn_valid(pgn):
    return isinstance(pgn, str) or len(pgn.strip()) == 0


def is_correct_move(centi_pawn_loss):
    return centi_pawn_loss <= CENTI_PAWN_LOSS_THRESHOLD


def get_accuracy_by_time_class(time_class, dataFrame, target_username):
    games = dataFrame[dataFrame["time_class"] == time_class]
    accuracies = []
    mean = 0
    for _, row in games.iterrows():
        if not is_pgn_valid(row["pgn"]):
            continue
        target_color = "white" if row["white"] == target_username else "black"
        current_game = chess.pgn.read_game(StringIO(row["pgn"]))
        if current_game is None:
            continue
        result = analyze_game(current_game, target_color)
        print(f"Result: {row['result']} | Accuracy: {result}")
        accuracies.append(result)
    for accuracy in accuracies:
        mean += accuracy

    return mean / len(accuracies)


def analyze_game(game, target_color):
    current_board = game.board()
    moves = game.mainline_moves()
    correct_moves = 0
    total_moves = 0
    last_analyze = Engine.analyse(
        current_board, chess.engine.Limit(depth=ANALYZE_DEPTH)
    )
    for _, move in enumerate(moves):
        if adapt_turn(current_board.turn) != target_color:
            current_board.push(move)
            continue

        total_moves += 1
        centi_pawn_loss_before = calculate_centi_pawn_loss(last_analyze, target_color)
        current_board.push(move)
        last_analyze = Engine.analyse(current_board, chess.engine.Limit(depth=15))
        centi_pawn_loss_after = calculate_centi_pawn_loss(last_analyze, target_color)
        centi_pawn_loss = centi_pawn_loss_before - centi_pawn_loss_after
        if is_correct_move(abs(centi_pawn_loss)):
            correct_moves += 1

    return (correct_moves / total_moves) * 100


def get_head_to_head_games(dataframe, target_player, opponent):
    if not opponent:
        return "There is no opponent specified"

    return dataframe[
        ((dataframe["white"] == target_player) & (dataframe["black"] == opponent))
        | ((dataframe["black"] == target_player) & (dataframe["white"] == opponent))
    ]


def get_accuracy_per_game(dataframe, target_player, opponent):
    target_player_game = get_head_to_head_games(dataframe, target_player, opponent)

    if target_player_game.empty:
        raise ValueError("No games found between these players.")

    white_player = target_player_game["white"].values[0].strip().lower()
    black_player = target_player_game["black"].values[0].strip().lower()
    requested_opponent = opponent.strip().lower()

    if requested_opponent == white_player or requested_opponent == black_player:
        target_color = "white" if white_player == target_player else "black"
        current_game = chess.pgn.read_game(
            StringIO(target_player_game["pgn"].values[0])
        )
        result = analyze_game(current_game, target_color)
        return result
    else:
        raise ValueError("There is no opponent with this name")

