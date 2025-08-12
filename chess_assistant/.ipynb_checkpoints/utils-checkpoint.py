import json
import os
from io import StringIO
import chess.engine
import chess.pgn
import pandas as pd
import chess

def acc_by_timeclass(time_class):
    MAX_MOVES = 60
    engine_path = r"../stockfish/stockfish-windows-x86-64-avx2.exe"
    cache_file = f"../cache/accuracy_time_class.json"
    
    if os.path.exists(cache_file):
        with open(cache_file) as file:
            data = json.load(file)
            correct_moves = sum([1 for move in data if move["correct_move"]])
            total = len(data)
            accuracy = (total / correct_moves) * 100 if total else 0
    
    data = pd.read_csv("../data/data.csv")
    games = data[data["time_class"] == time_class]["pgn"]
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)
    centipawn_threshload = 50
    moves_result = []

    for index, pgn in enumerate(games):
        if not isinstance(pgn, str) or len(pgn.strip()) == 0:
            continue
            
        game = chess.pgn.read_game(StringIO(pgn))
        board = game.board()

        if game == None:
            continue
        
        for move_num, move in enumerate(game.mainline_moves()):
            if move_num > MAX_MOVES:
                break
            try:
                analysis_before = engine.analyse(board, chess.engine.Limit(depth=20))
                evaluation_before = analysis_before["score"].white().score(mate_score=1000)
                
                board.push(move)
                
                analysis_after = engine.analyse(board, chess.engine.Limit(depth=20))
                evaluation_after = analysis_after["score"].white().score(mate_score=1000)
                
                if evaluation_before is not None and evaluation_after is not None:
                    centipawn_loss = abs(evaluation_before - evaluation_after)
                    if centipawn_loss <= centipawn_threshload:
                        correct_moves += 1
                        moves_result.append({"correct_move": True})
                    else:
                        moves_result.append({"correct_move": False})
            except Exception as error:
                print(f"analysis failed at index{index}: {error}")
                continue
            
      
    engine.quit()
    os.makedirs("../cache", exist_ok = True)
    with open(cache_file, "w") as file:
         json.dump(moves_result, file)


    correct_moves = sum([1 for move in moves_result if move["correct_move"]]) 
    total_moves = len(moves_result)
    accuracy = (correct_moves / total_moves) * 100 if total_moves > 0 else 0
    return accuracy

def accuracy_per_game(desired_game):
    engine_path = r"../stockfish/stockfish-windows-x86-64-avx2.exe"
    data = pd.read_csv("../data/data.csv")
    pgn = data.loc[desired_game, "pgn"]
    game = chess.pgn.read_game(StringIO(pgn))
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)
    board = game.board()
    total_moves = 0
    correct_moves = 0
    centipawn_threshload = 50

    for move in enumerate(game.mainline_moves()):
        try:
            analysis_before = engine.analyse(board, chess.engine.Limit(depth=20))
            evaluation_before = analysis_before["score"].white().score(mate_score=1000)

            board.push(move)

            analysis_after = engine.analyse(board, chess.engine.Limit(depth=20))
            evaluation_after = analysis_after["score"].white().score(mate_score=1000)
            if evaluation_before is not None and evaluation_after is not None:
                centipawn_loss = abs(evaluation_before - evaluation_after)

                if centipawn_loss <= centipawn_threshload:
                    correct_moves += 1

            total_moves += 1
        except Exception as error:
            print(f"analysis failed at move{total_moves}: {error}")
            continue

    engine.quit()
    accuracy = (correct_moves / total_moves) * 100 if total_moves > 0 else 0
    return accuracy


def classify_evaluation(evaluation_before, evaluation_after):
    if evaluation_before is not None and evaluation_after is not None:
        drop = abs(evaluation_before - evaluation_after)

    if drop is not None:
        match True:
            case _ if drop < 30:
                label = "best"
            case _ if drop < 80:
                label = "inaccuracy"
            case _ if drop < 200:
                label = "mistake"
            case _ if drop >= 200:
                label = "blunder"
            case _:
                label = "unknown"
    else:
        label = "unknown"

        print(f"move: {label}")
      

def eval_estimation(desired_game):
    engine_path = r"../stockfish/stockfish-windows-x86-64-avx2.exe"
    data = pd.read_csv("../data/data.csv")
    pgn = data.loc[desired_game, "pgn"]
    game = chess.pgn.read_game(StringIO(pgn))
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)
    board = game.board()
    total_moves = 0
    correct_moves = 0
    blunders = 0
    best_moves = []
    blunders = []

    for move in game.mainline_moves():
        try:
            game_analysis_before = engine.analyse(board, chess.engine.Limit(depth = 20))
            eval_before = game_analysis_before['score'].white().score(mate_score = 1000)
            
            board.push(move)

            game_analysis_after = engine.analyse(board, chess.engine.Limit(depth = 20))
            eval_after = game_analysis_before['score'].white().score(mate_score = 1000)
            print(eval_before, eval_after)
            evalulation = classify_evaluation(eval_before, eval_after)
            print(evalulation)
            
        except Exception as error:
             print(f"analysis failed at move{total_moves}: {error}")
             continue