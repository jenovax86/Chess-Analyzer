# ♟️ Chess Analyzer
## A Simple Chess Analyzer tool that analyzes your chess.com profile and gives you insights about your progress.

# Getting Started
### This app analyzes your chess.com profile and gives you a detailed breakdown of your performance, including:
- Win and loss estimation
- Your performance based on the time class
- Your rating over time
- Your rating over time based on time class
- The strongest opponent you've beaten
- Show accuracy in all ofthe  time classes and show which time class you have a better accuracy

## Prerequisites
### You need [StockFish Engine](https://stockfishchess.org/download/) for your operating system.

### Install the required Python libraries:
```bash
pip install -r requirements.txt
```

## Installation
## 1. Clone the project
```bash
git clone https://github.com/jenovax86/Chess-Analyzer.git
```
## 2. Create a .env file (based on .env.example) and specify the path to the Stockfish executable you downloaded.

# Usage
## For accuracy by time control only
```bash
cd src
python __main__.py
```
## For a full analysis with visual plots of your progress
```bash
jupyter lab
```
or 
```bash
jupyter notebook
```
