from chess_assistant.fetch_games import get_player_info
from chess_assistant.accuracy_analyzer import get_accuracy_by_time_class

CHESS_DOT_COM_USERNAME = "Invalid_dude"
CHESS_TIME_CLASS = "bullet"

def main():
    get_player_games = get_player_info(CHESS_DOT_COM_USERNAME)
    get_accuracy = get_accuracy_by_time_class(CHESS_TIME_CLASS, get_player_games, CHESS_DOT_COM_USERNAME)
    print(f"Your overall accuracy in {CHESS_TIME_CLASS} is: ", get_accuracy)



if __name__ == "__main__":
    main()