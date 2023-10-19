import numpy as np

import pandas as pd
import yfinance as yf

import matplotlib as mpl
import matplotlib.pyplot as plt

def min_Ndays(rates, Ndays=14):
    return rates.rolling(window=Ndays).min()

def max_Ndays(rates, Ndays=14):
    return rates.rolling(window=Ndays).max()

def current_market_rate(recentClosing, min14, max14):
    return 100 * (recentClosing - min14) / (max14 - min14)

def moving_average_market_rate(rates, n_avg=3):
    return rates.rolling(window=n_avg).mean()

# def larger_than_previous(rates):
#     if rates.loc[-1] > rates.loc[-2]:
#         larger = True
#     else:
#         larger = False
#     return larger

def changing_sign(rates):
    """
    Determine whether there is a sign change from the second to last to the last element

    :param rates: numerical values in a numpy array dataframe
    :return: 1 for positive to negative sign change, -1 for negative to positive sign change, 0 for no sign change
    """
    if (rates[-1] > 0) and (rates[-2] < 0):
        change = 1
    elif (rates[-1] < 0) and (rates[-2] > 0):
        change = -1
    else:
        change = 0
    return change

def crossing_down_or_up(rates_1, rates_2):
    """
    Determine where rate_1 crosses down or up across rate_2, and where they do not cross at all

    :param rates_1: numerical values in a pandas dataframe that will do the crossing
    :param rates_2: numerical values in a pandas dataframe that acts as the reference to be crossed
    :return: 1 for rate_1 crossing down across rate_2, -1 for rate_1 crossing up across rate_2, 0 for no crossing
    """
    # rates_comb = pd.concat([rates_1, rates_2], axis=1)
    rates_diff = rates_1 - rates_2
    rates_diff_sign_changes = rates_diff.rolling(window=2).apply(changing_sign, raw=True)

    return rates_diff_sign_changes



def oscillator_buy_sell(ticker, period):
    history = ticker.history(period=period)
    name = ticker.info["shortName"]
    shorthand = ticker.info["symbol"]

    currency = ticker.info["currency"]

    rates = history["Close"]
    dates = rates.index

    min_recent = min_Ndays(rates)
    max_recent = max_Ndays(rates)

    current_market_rates = current_market_rate(rates, min_recent, max_recent)
    moving_avg_current_market_rates = moving_average_market_rate(current_market_rates)

    crossing_market_rates = crossing_down_or_up(current_market_rates, moving_avg_current_market_rates)



    mpl.use('MacOSX')
    fig, ax = plt.subplots(
        2, 1,
        figsize=(9, 4),
        height_ratios=(5, 3),
        layout='constrained',
        sharex=True,
    )


    ax[0].plot(dates, moving_avg_current_market_rates, color='xkcd:light orange')
    ax[0].plot(dates, current_market_rates, color='xkcd:orange')

    ax[1].plot(dates, crossing_market_rates, color='xkcd:orange')


    fig.suptitle(f"{name} ({shorthand})")
    ax[0].set_ylabel(f"Market rate ({currency})")

    ax[-1].set_xlabel("Date")

    fig.savefig(f"plots/marketrates_{shorthand}.png", dpi=300)

    return fig, ax



def plot_market_price(ticker, period):
    history = ticker.history(period=period)
    name = ticker.info["shortName"]
    shorthand = ticker.info["symbol"]

    # for item in ticker.info.items():
    #     print(item)

    currency = ticker.info["currency"]

    dates = history.index

    open_rate = history["Open"]
    close_rate = history["Close"]
    high_rate = history["High"]
    low_rate = history["Low"]

    open_to_close_growth = close_rate - open_rate
    net_change = close_rate - close_rate.shift(1)

    print(close_rate)
    print(close_rate.shift(1))

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
    ax[1].axhline(0, color='xkcd:dark pink', ls='--')

    # net change (closing rate - closing rate previous day)
    netchange_colors = np.where((net_change > 0), 'xkcd:pink', 'xkcd:light pink')
    ax[2].bar(dates, net_change, color=netchange_colors)
    ax[2].axhline(0, color='xkcd:dark pink', ls='--')

    # cosmetics
    fig.suptitle(f"{name} ({shorthand})")

    ax[0].legend(reverse=True)

    ax[0].set_ylabel(f"Price ({currency})")
    ax[1].set_ylabel(f"Daily growth ({currency})")
    ax[2].set_ylabel(f"Net change ({currency})")

    ax[-1].set_xlabel("Date")

    fig.savefig(f"plots/marketprices_{shorthand}.png", dpi=300)

    return fig, ax



if __name__ == "__main__":
    print("Welcome to the Stochastic Oscillator Trading script by Pascal U. Foerster!")

    # TEST: get some stock information
    get_META_info = yf.Ticker("META")
    period = '6mo'

    fig, ax = plot_market_price(
        get_META_info,
        period
    )

    oscillator_buy_sell(
        get_META_info,
        period
    )