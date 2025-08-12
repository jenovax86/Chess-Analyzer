import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from chess_utils.accuracy import get_accuracy_by_time_class


TIME_CLASSES = ["bullet", "blitz", "rapid"]

CSV = pd.read_csv("../data/data.csv")

def win_loss_estimation(data_frame):
    plt.figure(figsize= (12, 6))
    chart = sns.countplot(data = data_frame, x = 'result')
    plt.title("result")
    plt.margins(x = 0.1)
    plt.show()

def analyze_match_outcomes_by_time_class(data_frame, time_class):
    result = data_frame[data_frame["time_class"] = time_class]
    plt.figure(figsize= (12, 6))
    chart = sns.countplot(data = result, x = 'result')
    plt.title("result")
    plt.margins(x = 0.1)
    plt.show()

def rating_over_time(username, data_frame):
    sort_values = data_frame.sort_values("end_time")
    player = data_frame[(data_frame["white"] == username) | (data_frame["black"] == username)]
    player["player_rating"] = player.apply(
        lambda row: row["white_rating"] if row["white"] == username else row["black_rating"],
        axis = 1
    )
    plt.figure(figsize = (12, 6))
    player.plot(x = "end_time", y = "player_rating", title = f"{username}'s Rating over time")
    plt.ylabel("Rating")
    plt.show()


def performance_by_time_control(data_frame):
    plt.figure(figsize= (12, 6))
    sns.countplot(data = data_frame, x = "time_class", hue = "result")
    plt.title("Performance")
    plt.show()


def strongest_beaten_opponents(username, data_frame):
    wins = data_frame[data_frame["result"] == "win"].copy()
    wins["opponent"] = wins.apply(
        lambda row: row["black"] if row["white"] == username else row["white"],
        axis = 1
    )
    wins["opponent_rating"] = wins.apply(
        lambda row : row["black_rating"] if row["white"] == username else row["white_rating"],
        axis = 1
    )
    top_opponents = wins.sort_values(by = "opponent_rating", ascending = False).head(20)
    print(top_opponents[["opponent", "opponent_rating"]])

def show_acc_by_time_classes(target_username):
    accuracies = []
    # for time_class in TIME_CLASSES:
        accuracy = get_accuracy_by_time_class("bullet", CSV, target_username)
        # accuracies.append({
        #     "time_class": time_class.capitalize(),
        #     "accuracy": accuracy
        # })
        
    data = pd.DataFrame(accuracies)
    print(data)

    plt.figure(figsize = (12, 6))
    sns.countplot(data = data, x = "time_class")
    plt.title("Accuracy By Time Class")
    plt.ylim(30, 60)
    plt.ylabel("Accuracy (%)")
    plt.xlabel("Time Class")
    plt.show()


