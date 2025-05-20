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
- GUI to play the game

### Requirements
- `python-chess` library

### Usage
Run this command:
```bash
python chess_gui.py
```
Choose whether you wish to play against AI, or ONE-ON-ONE locally.

---

## Installation
1. Install required packages:
```bash
pip install -r requirements.txt
