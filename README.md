# Chess Analyzer
## A Simple Chess Analyzer tool that analyzes your chess.com profile and gives you insights about your progress.

# Getting Started
## This app analyzes your chess.com profile and gives a full analysis like your:
 Win and loss estimation
 Your performance based on the time class
 Your rating over time
 Your rating over time based on time class
 The strongest opponent you've beaten
 Show accuracy in all ofthe  time classes and show which time class you have a better accuracy

## Prerequisites
### You need [StockFish](https://stockfishchess.org/download/) engine. 
Download the suitable version for your operating system.

### You need some libraries for the project to run, so install the libraries with this
```bash
pip install -r requirements.txt
```

## Installation
## 1. Clone the project in your system
```bash
git clone https://github.com/jenovax86/Chess-Analyzer.git
```
## 2. Create a .env file and like .env.example in the project, and place the executable file of the Stockfish that you've downloaded.


# Usage
## If you want to just get your accuracy game based on the time class, just run
```bash
python -m src 
```
## If you want the full analysis with plots that show your progress run
```bash
jupyter lab
```
or 
```bash
jupyter notebook
```
