import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_data(ticker, start_date, end_date):
    """下載指定股票的歷史資料"""
    df = yf.download(ticker, start=start_date, end=end_date)
    if df.empty:
        return None
    return df

def calculate_signals(df, short_window=20, long_window=50):
    """計算SMA和交易信號"""
    df[f'SMA{short_window}'] = df['Close'].rolling(window=short_window).mean()
    df[f'SMA{long_window}'] = df['Close'].rolling(window=long_window).mean()
    
    df['Signal'] = 0
    df.loc[df[f'SMA{short_window}'] > df[f'SMA{long_window}'], 'Signal'] = 1
    
    df['Position'] = df['Signal'].replace(to_replace=0, method='ffill')
    df['Position'].fillna(0, inplace=True)
    return df

def plot_signals(df, ticker, short_window=20, long_window=50):
    """繪製價格和交易信號圖"""
    buy_signals = (df['Signal'] == 1) & (df['Signal'].shift(1) == 0)
    sell_signals = (df['Signal'] == 0) & (df['Signal'].shift(1) == 1)

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(df['Close'], label=f'{ticker} Close Price', alpha=0.5)
    ax.plot(df[f'SMA{short_window}'], label=f'SMA {short_window}')
    ax.plot(df[f'SMA{long_window}'], label=f'SMA {long_window}')
    ax.scatter(df[buy_signals].index, df[buy_signals]['Close'], label='Buy Signal', marker='^', color='green', s=100)
    ax.scatter(df[sell_signals].index, df[sell_signals]['Close'], label='Sell Signal', marker='v', color='red', s=100)
    
    ax.set_title(f'{ticker} Strategy: SMA Crossover Buy/Sell Signals')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    return fig

def calculate_returns(df):
    """計算策略和持有的報酬率"""
    df['Daily Return'] = df['Close'].pct_change()
    df['Strategy Return'] = df['Daily Return'] * df['Position']
    return df

def plot_performance(df):
    """繪製績效比較圖"""
    df['BuyHold'] = (1 + df['Daily Return']).cumprod()
    df['Strategy'] = (1 + df['Strategy Return']).cumprod()

    fig, ax = plt.subplots(figsize=(14, 7))
    df['BuyHold'].plot(ax=ax, label='Buy & Hold')
    df['Strategy'].plot(ax=ax, label='SMA Strategy')
    
    ax.set_title('Performance Comparison: Strategy vs Buy & Hold')
    ax.set_ylabel('Growth of $1 Investment')
    ax.set_xlabel('Date')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    return fig

def get_performance_report(daily_returns, name="Strategy"):
    """生成績效報告的字串"""
    daily_returns = daily_returns.dropna()
    if len(daily_returns) < 2: # 需要至少兩個數據點來計算波動率
        return f"Performance Report - {name}\n" + "="*40 + "\nNot enough data for calculation.\n" + "="*40 + "\n"

    cumulative_return = (1 + daily_returns).prod() - 1
    
    # 檢查回測期間是否大於一年
    if len(daily_returns) > 252:
        annualized_return = (1 + cumulative_return) ** (252 / len(daily_returns)) - 1
    else:
        annualized_return = cumulative_return # 如果小於一年，年化報酬率等於累積報酬率

    annualized_volatility = daily_returns.std() * np.sqrt(252)
    
    # 避免除以零
    sharpe_ratio = annualized_return / annualized_volatility if annualized_volatility != 0 else 0
    
    cumulative = (1 + daily_returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()

    report = []
    report.append(f"Performance Report - {name}")
    report.append("=" * 40)
    report.append(f"Cumulative Return     : {cumulative_return:.2%}")
    report.append(f"Annualized Return     : {annualized_return:.2%}")
    report.append(f"Annualized Volatility : {annualized_volatility:.2%}")
    report.append(f"Sharpe Ratio          : {sharpe_ratio:.2f}")
    report.append(f"Max Drawdown          : {max_drawdown:.2%}")
    report.append("=" * 40)
    return "\n".join(report)

def run_backtest(ticker, start_date, end_date, short_window=20, long_window=50):
    """執行完整的回測流程"""
    df = get_data(ticker, start_date, end_date)
    if df is None:
        print(f"Could not download data for {ticker}.")
        return

    df = calculate_signals(df, short_window, long_window)
    df = calculate_returns(df)

    print(f"Running backtest for {ticker} from {start_date} to {end_date}")
    
    # 產生並顯示圖表
    fig_signals = plot_signals(df, ticker, short_window, long_window)
    plt.show()
    
    fig_performance = plot_performance(df)
    plt.show()

    # 產生並顯示績效報告
    report_buy_hold = get_performance_report(df['Daily Return'], name='Buy & Hold')
    report_strategy = get_performance_report(df['Strategy Return'], name='SMA Strategy')
    
    print(report_buy_hold)
    print(report_strategy)

if __name__ == '__main__':
    # 預設參數
    TICKER = 'AAPL'
    START_DATE = '2020-01-01'
    END_DATE = '2024-12-31'
    
    run_backtest(TICKER, START_DATE, END_DATE)
