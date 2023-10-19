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

    mpl.use('MacOSX')
    fig, ax = plt.subplots(
        2, 1,
        figsize=(9, 9),
        layout='constrained',
        sharex=True
    )

    # rates in upper subplot
    ax[0].fill_between(dates, high_rate, low_rate, alpha=0.7, color='xkcd:light pink', label="Daily high-low")
    ax[0].plot(dates, open_rate, color='xkcd:pink', label="Opening rate")
    ax[0].plot(dates, close_rate, color='xkcd:dark pink', label="Closing rate")


    # cosmetics
    ax[0].legend()

    ax[0].set_ylabel(f"Rates ({currency})")
    ax[1].set_ylabel(f"Daily growth ({currency})")

    ax[1].set_xlabel("Date")

    fig.savefig("plots/marketrates.png", dpi=300)



if __name__ == "__main__":
    print("Welcome to the Stochastic Oscillator Trading script by Pascal U. Foerster!")

    # TEST: get some stock information
    get_META_info = yf.Ticker("META")
    period = '6mo'

    plot_market_rate(get_META_info, period)