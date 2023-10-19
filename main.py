import numpy as np

import pandas as pd
import yfinance as yf

import matplotlib as mpl
import matplotlib.pyplot as plt

def min_Ndays(rates, Ndays=14):
    minNdays = np.min(rates[-Ndays:]) if len(rates) > Ndays else np.min(rates)
    return minNdays

def max_Ndays(rates, Ndays=14):
    maxNdays = np.max(rates[-Ndays:]) if len(rates) > Ndays else np.max(rates)
    return maxNdays

def current_market_rate(recentC, min14, max14):
    return 100 * (recentC - min14) / (max14 - min14)

def moving_average_market_rate(rates, n_avg=3):
    avg = np.average(rates[-n_avg:]) if len(rates) > n_avg else np.average(rates)
    return avg



def plot_market_rate(ticker, period):
    history = ticker.history(period=period)
    currency = ticker.info["currency"]

    dates = history.index

    open_rate = history["Open"]
    close_rate = history["Close"]
    high_rate = history["High"]
    low_rate = history["Low"]

    open_to_close_growth = close_rate - open_rate
    net_change = close_rate - close_rate.shift(-1)
    print(net_change)

    mpl.use('MacOSX')
    fig, ax = plt.subplots(
        3, 1,
        figsize=(9, 9),
        height_ratios=(2, 1, 1),
        layout='constrained',
        sharex=True,
    )

    # rates in upper subplot
    ax[0].fill_between(dates, high_rate, low_rate, alpha=0.7, color='xkcd:light pink', label="Daily high-low")
    ax[0].plot(dates, open_rate, color='xkcd:pink', label="Opening rate")
    ax[0].plot(dates, close_rate, color='xkcd:dark pink', label="Closing rate")

    # daily growth (closing - opening rates)
    growth_colors = np.where((open_to_close_growth > 0), 'xkcd:pink', 'xkcd:light pink')
    ax[1].bar(dates, open_to_close_growth, color=growth_colors)
    # ax[1].plot(dates, open_to_close_growth, color='xkcd:pink')
    ax[1].axhline(0, color='xkcd:dark pink', ls='--')

    # net change (closing rate - closing rate previous day)
    netchange_colors = np.where((net_change > 0), 'xkcd:pink', 'xkcd:light pink')
    ax[2].bar(dates, net_change, color=netchange_colors)
    ax[2].axhline(0, color='xkcd:dark pink', ls='--')

    # cosmetics
    ax[0].legend()

    ax[0].set_ylabel(f"Rates ({currency})")
    ax[1].set_ylabel(f"Daily growth ({currency})")
    ax[2].set_ylabel(f"Net change ({currency})")

    ax[-1].set_xlabel("Date")

    fig.savefig("plots/marketrates.png", dpi=300)



if __name__ == "__main__":
    print("Welcome to the Stochastic Oscillator Trading script by Pascal U. Foerster!")

    # TEST: get some stock information
    get_META_info = yf.Ticker("META")
    period = '6mo'

    plot_market_rate(get_META_info, period)