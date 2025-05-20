# MAJOR AND MINOR PROJECT FOR AIML
## Overview
Two AI-powered projects in one package:
1. **Stock Market Prediction**: Uses LSTM neural networks to forecast stock prices
2. **Chess AI Engine**: Implements Minimax algorithm with Alpha-Beta pruning for chess gameplay

---

## 1. Stock Market Price Prediction

### Features
- Time-series forecasting using historical closing prices
- Data preprocessing with MinMax scaling
- LSTM neural network architecture
- Visualization of predictions vs actual prices

### Requirements
- CSV dataset with 'Date' and 'Close' columns in ZIP archive
- Python libraries: pandas, numpy, matplotlib, scikit-learn, tensorflow

### Usage

Simply run the script to start the stock price prediction:

```bash
python Stock_Market_Price_Prediction.py
```


---

## 2. Chess AI Engine

### Features
- Complete chess rule implementation
- AI opponent using Minimax with Alpha-Beta pruning
- Board visualization in terminal
- UCI-compliant move input
- Game termination detection

### Requirements
- `python-chess` library

### Usage
1. Select option 2 from the main menu
2. AI plays as White, user plays as Black
3. Input moves in UCI format (e.g., `e7e5` for pawn move)
4. Game continues until checkmate or draw

---

## Installation
1. Install required packages:
```bash
pip install -r requirements.txt
