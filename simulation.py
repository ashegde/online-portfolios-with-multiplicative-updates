import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from portfolio import previous_best, constant_weights, ExponentiatedGradient, Portfolio
import yfinance as yf

#----------------------------------------------------------------------------------
# loading S&P 500 data

# Note about time convention:
# time t = opening of day t
# (forward) price relative at t = price at t+1 / price at t
#     at time t, we know price relatives from times 0,...,t-1
# thus, at the beginning of day t, the price relative for day t-1 is revealed
# suppose x(t) is the price relative at time t (opening of day)
#         w(t) contains the portfolio weights chosent at time t
# then, w(t) is decided based on x(1),...,x(t-1) -- i.e., all information available at time t

url = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
start_date = "2005-01-01"

table = pd.read_html(url)[0]
tickers = table["Symbol"].tolist()
data = yf.download(tickers, start_date)
data = data["Adj Close"]
# adjusted closing price on day t is the opening price of day t+1, so we must shift forward by 1
data = data.shift(1).iloc[1:,:]
# remove stocks that have NaNs as prices
data = data.dropna(axis = 'columns')
price_relatives = data.shift(-1)/data
price_relatives.drop(price_relatives.tail(1).index, inplace=True)

#-----------------------------------------------------------------------------------

market_size = len(price_relatives.columns)
num_days = len(price_relatives.index)
initial_weights = pd.Series(data = [1.0/market_size for i in range(market_size)], index = price_relatives.columns)
initial_wealth = 1000

exp_grad_lr_0d10 = ExponentiatedGradient(learning_rate = 0.10)
exp_grad_lr_1d00 = ExponentiatedGradient(learning_rate = 1.00)
exp_grad_lr_10d00 = ExponentiatedGradient(learning_rate = 10.00)

portfolios = {
    "previous_best": Portfolio(wealth = initial_wealth, weights = initial_weights, update_rule = previous_best),
    "constant_weights": Portfolio(wealth = initial_wealth, weights = initial_weights, update_rule = constant_weights),
    "exp_grad_lr=0.10": Portfolio(wealth = initial_wealth, weights = initial_weights, update_rule = exp_grad_lr_0d10),
    "exp_grad_lr=1.00": Portfolio(wealth = initial_wealth, weights = initial_weights, update_rule = exp_grad_lr_1d00),
    "exp_grad_lr=10.00": Portfolio(wealth = initial_wealth, weights = initial_weights, update_rule = exp_grad_lr_10d00),
}

wealth_processes = {k: [] for k in portfolios.keys()}
top_five_holdings = {k: [] for k in portfolios.keys()}

for day in range(num_days):
  todays_price_relative = price_relatives.iloc[day,:]

  for k in portfolios.keys():
    portfolios[k].update(todays_price_relative)
    wealth_processes[k].append(portfolios[k].get_current_wealth())

    holdings = portfolios[k].weights.sort_values(ascending=False)
    top_five_holdings[k].append( holdings.iloc[:5] )


# Summarize results by printing wealth factors

print("Strategy  |  wealth factor \n")
for k in portfolios.keys():
  print(f"{k} | {portfolios[k].get_wealth_factor():0.2f} \n")

wealth_processes = pd.DataFrame(data = wealth_processes, index = price_relatives.index)

#--------------------------------------------------------------------------------------

# plot 1: portfolio wealth

fig, ax = plt.subplots()
for k in wealth_processes.columns:
  ax.plot(wealth_processes[k], label=k)

ax.set_xlabel("Year")
ax.set_ylabel("Wealth")
ax.set_yscale("log")
ax.set_title("Portfolio strategies and corresponding wealth")
plt.legend(loc="upper left")
plt.savefig("portfolio_wealth.png")

# plot 2: portfolio holdings

timestamps = price_relatives.index
selected_indices = [(0, 0, 0), (0, 1, 500),
                    (1, 0, 1000), (1, 1, 2000),
                    (2, 0, 3000), (2, 1, 4000),
                    (3, 0, 4500), (3, 1, -1)]

strategy = "exp_grad_lr=10.00"

fig, axs = plt.subplots(4, 2, figsize=(8, 16))

for ii in selected_indices:
  axs[ii[0], ii[1]].barh(top_five_holdings[strategy][ii[2]].index, top_five_holdings[strategy][ii[2]].to_numpy())
  axs[ii[0], ii[1]].set_title(f"{timestamps[ii[2]].strftime('%Y-%m-%d')}", fontsize=11)
  axs[ii[0], ii[1]].set_xscale("log")

fig.suptitle(f"{strategy} (wealth factor {portfolios[strategy].get_wealth_factor():0.2f}): top 5 highest weighted stocks", y=0.92, fontsize = 14)
plt.savefig("holdings_over_time.png")