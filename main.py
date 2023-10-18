import numpy as np

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


if __name__ == "__main__":
    print("Welcome to the Stochastic Oscillator Trading script by Pascal U. Foerster!")