# SmaQuant: Simple Moving Average Crossover Strategy

This is a simple quantitative backtesting project using Python.
It implements a basic SMA (Simple Moving Average) crossover strategy and compares it against the Buy & Hold benchmark.

## Features

- Data download via Yahoo Finance (`yfinance`)
- Strategy logic: SMA 20 / SMA 50 crossover
- Signal visualization (buy/sell points)
- Strategy backtest & performance analysis
- Comparison with Buy & Hold
- Modular and extendable code

## Strategy Overview

The SMA crossover strategy works as follows:
- **Buy Signal**: When SMA 20 crosses above SMA 50
- **Sell Signal**: When SMA 20 crosses below SMA 50
- **Position**: Long when SMA 20 > SMA 50, otherwise cash

## Requirements

- Python 3.7+
- See `requirements.txt` for all dependencies

## How to Run

1. Clone this repo
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the backtest:
   ```bash
   python sma_backtest.py
   ```

## Output

The script will generate:
1. **Trading Signals Chart**: Shows price, SMA lines, and buy/sell signals
2. **Performance Comparison Chart**: Strategy vs Buy & Hold performance
3. **Performance Metrics**: Including returns, volatility, Sharpe ratio, and max drawdown

## Performance Metrics

The script calculates and displays:
- **Cumulative Return**: Total return over the period
- **Annualized Return**: Return per year
- **Annualized Volatility**: Standard deviation of returns
- **Sharpe Ratio**: Risk-adjusted return measure
- **Max Drawdown**: Maximum peak-to-trough decline

## Configuration

Currently configured for:
- **Symbol**: AAPL (Apple Inc.)
- **Period**: 2020-01-01 to 2024-12-31
- **SMA Periods**: 20 and 50 days

You can easily modify these parameters in the `sma_backtest.py` file.

## File Structure

```
SmaQuant/
├── sma_backtest.py      # Main backtesting script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Dependencies

Key libraries used:
- `yfinance`: Yahoo Finance data download
- `pandas`: Data manipulation and analysis
- `matplotlib`: Plotting and visualization
- `numpy`: Numerical computations

## Future Enhancements

Potential improvements:
- [ ] Add more technical indicators
- [ ] Implement multiple timeframes
- [ ] Add transaction costs
- [ ] Portfolio optimization
- [ ] Risk management features
- [ ] Export results to CSV/Excel

## License

This project is open source and available under the MIT License.

## Disclaimer

This is for educational purposes only. Past performance does not guarantee future results. Always do your own research before making investment decisions.
# SimQuant
