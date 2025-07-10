import streamlit as st
import pandas as pd
from datetime import date
import quantstats as qs
from sma_backtest import (
    get_data,
    calculate_signals,
    calculate_returns,
    plot_signals,
    plot_performance,
    get_performance_report
)

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="SmaQuant: SMA Crossover Strategy Backtester",
    page_icon="📈",
    layout="wide"
)

# --- Sidebar for User Inputs ---
st.sidebar.header('⚙️ Backtest Parameters')

# Input fields in the sidebar
ticker = st.sidebar.text_input('Ticker Symbol', 'AAPL').upper()
start_date = st.sidebar.date_input('Start Date', date(2020, 1, 1))
end_date = st.sidebar.date_input('End Date', date.today())
short_window = st.sidebar.slider('Short-term SMA Window', 5, 100, 20)
long_window = st.sidebar.slider('Long-term SMA Window', 10, 200, 50)

# Validate window sizes
if short_window >= long_window:
    st.sidebar.error('Short-term window must be smaller than long-term window.')
    st.stop()

# --- Main Dashboard ---
st.title('📈 SmaQuant: SMA Crossover Strategy Backtester')
st.write("""
This tool performs a backtest using a simple **Simple Moving Average (SMA) Crossover Strategy**.
Enter your parameters in the sidebar on the left and click 'Start Backtest' to see the results.
""")

# Button to start the backtest
if st.sidebar.button('🚀 Start Backtest'):
    with st.spinner(f'Loading data for {ticker} and running backtest...'):
        # 1. Get Data
        df = get_data(ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

        if df is None or df.empty:
            st.error(f'Could not download data for ticker "{ticker}". Please check the ticker and the time range.')
        else:
            # 2. Calculate Signals and Returns
            df = calculate_signals(df, short_window, long_window)
            df = calculate_returns(df)

            st.success(f'Backtest for {ticker} completed successfully!')

            # --- Display Results ---
            st.header('📊 Backtest Results')

            # 3. Visualize Signals
            st.subheader('Buy/Sell Signals on Chart')
            fig_signals = plot_signals(df, ticker, short_window, long_window)
            st.pyplot(fig_signals)

            # 4. Visualize Performance
            st.subheader('Performance Comparison: Strategy vs. Buy & Hold')
            fig_performance = plot_performance(df)
            st.pyplot(fig_performance)

            # 5. Display Performance Report
            st.subheader('Detailed Performance Report')
            col1, col2 = st.columns(2)
            with col1:
                report_buy_hold = get_performance_report(df['Daily Return'], name='Buy & Hold')
                st.text(report_buy_hold)
            with col2:
                report_strategy = get_performance_report(df['Strategy Return'], name=f'SMA ({short_window}/{long_window}) Strategy')
                st.text(report_strategy)

            # 7. Auto-generate Strategy Analysis Summary
            st.subheader('📝 Strategy Analysis Summary')

            # Helper function to safely get metrics, as names can vary
            def get_metric(metrics, keys, default=0.0):
                """Safely retrieve a metric by trying multiple possible keys and return a float."""
                for key in keys:
                    if key in metrics.index:
                        # Ensure we return a float, not a Series
                        return metrics.loc[key].iloc[0] if isinstance(metrics.loc[key], pd.Series) else metrics.loc[key]
                st.warning(f"Could not find metrics for: {keys}. Using default value: {default}.")
                return default

            # Extract key metrics for analysis
            metrics_bh = qs.reports.metrics(df['Daily Return'], display=False, mode='full')
            metrics_strategy = qs.reports.metrics(df['Strategy Return'], display=False, mode='full')

            # Define possible keys for each metric
            cum_return_keys = ['Cumulative Return', 'Cumulative Returns']
            volatility_keys = ['Annualized Volatility', 'Volatility (ann.)']
            sharpe_keys = ['Sharpe Ratio', 'Sharpe']
            mdd_keys = ['Max Drawdown', 'Maximum Drawdown']

            # Safely extract metrics using the helper function
            cum_return_bh = get_metric(metrics_bh, cum_return_keys)
            cum_return_strategy = get_metric(metrics_strategy, cum_return_keys)
            vol_bh = get_metric(metrics_bh, volatility_keys)
            vol_strategy = get_metric(metrics_strategy, volatility_keys)
            sharpe_bh = get_metric(metrics_bh, sharpe_keys)
            sharpe_strategy = get_metric(metrics_strategy, sharpe_keys)
            mdd_bh = get_metric(metrics_bh, mdd_keys)
            mdd_strategy = get_metric(metrics_strategy, mdd_keys)

            # Generate analysis text
            analysis_text = f"""
            In this backtest, the **SMA ({short_window}/{long_window}) Strategy** is compared against a **Buy & Hold** strategy:

            1.  **Cumulative Return**:
                *   SMA Strategy: `{cum_return_strategy:.2%}`
                *   Buy & Hold: `{cum_return_bh:.2%}`
            """

            if cum_return_strategy > cum_return_bh:
                analysis_text += "    *   **Conclusion**: Your strategy **outperformed** the benchmark.\n"
            else:
                analysis_text += "    *   **Conclusion**: Your strategy **did not outperform** the benchmark.\n"

            analysis_text += f"""
            2.  **Risk & Stability (Annualized Volatility)**:
                *   SMA Strategy: `{vol_strategy:.2%}`
                *   Buy & Hold: `{vol_bh:.2%}`
            """

            if vol_strategy < vol_bh:
                analysis_text += "    *   **Conclusion**: Your strategy showed **lower volatility**, suggesting a smoother investment journey with better risk control.\n"
            else:
                analysis_text += "    *   **Conclusion**: Your strategy showed **higher volatility**, indicating greater investment risk than the benchmark.\n"

            analysis_text += f"""
            3.  **Risk-Adjusted Return (Sharpe Ratio)**:
                *   SMA Strategy: `{sharpe_strategy:.2f}`
                *   Buy & Hold: `{sharpe_bh:.2f}`
            """
            if sharpe_strategy > sharpe_bh:
                analysis_text += "    *   **Conclusion**: After adjusting for risk, your strategy is **superior**. A higher Sharpe Ratio means more return per unit of risk.\n"
            else:
                analysis_text += "    *   **Conclusion**: After adjusting for risk, your strategy's performance is **inferior** to the benchmark.\n"

            analysis_text += f"""
            4.  **Max Drawdown (Worst-Case Loss)**:
                *   SMA Strategy: `{mdd_strategy:.2%}`
                *   Buy & Hold: `{mdd_bh:.2%}`
            """
            if mdd_strategy > mdd_bh: # Note: Max Drawdown is negative, so a value closer to 0 is better.
                analysis_text += "    *   **Conclusion**: Your strategy demonstrated **better loss control** during extreme market downturns.\n"
            else:
                analysis_text += "    *   **Conclusion**: Your strategy's loss control during extreme downturns was **not better** than the benchmark.\n"

            st.markdown(analysis_text)


            # 6. Display Data Table (optional)
            with st.expander("Show Raw Data and Signals"):
                st.dataframe(df.tail())
else:
    st.info('Please configure the parameters in the sidebar and start the backtest.')
