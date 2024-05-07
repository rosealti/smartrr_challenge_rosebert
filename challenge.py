import pandas as pd
import matplotlib.pyplot as plt

# Read stock price data from a CSV file
df_raw = pd.read_csv('stock_data.csv')
print("Raw Data", "\n", df_raw, "\n")



# Perform data cleaning and preprocessing
#   Set data types
df_raw['Date'] = pd.to_datetime(df_raw['Date'])
#   Check for duplicates and remove duplicates
df_cleaned = df_raw.copy()
if not df_cleaned[df_cleaned.duplicated() == True].empty:
    df_cleaned = df_cleaned.drop_duplicates()
print("Cleaned Data", "\n", df_raw, "\n")
df = df_cleaned.copy()



# Calculate various metrics and generate insights
# The Open and Close prices over the given time period
open_close_prices = df.loc[:, ['Date', 'Open', 'Close']]
print("Open and Close Prices", "\n", open_close_prices, "\n")

# Average daily return
#   https://www.investopedia.com/terms/a/averagereturn.asp
#   Formula: avg daily return = sum of daily returns / number of days

#   https://www.investopedia.com/terms/i/intraday-return.asp
#   Formula: daily return = close price - open price
#   Formula: daily return per-share gain = (close price - open price) * num_of_shares
#   Formula: daily return percent = ((close price - open price) / open price) * 100
number_of_days = len(df.index)
daily_return = (df["Close"] - df["Open"])
avg_daily_returns = sum(daily_return) / number_of_days
print("Avg Daily Returns", "\n", avg_daily_returns, "\n")

daily_return_per_share = daily_return * df["Volume"]
avg_daily_returns_per_share = sum(daily_return_per_share) / number_of_days
print("Avg Daily Returns per-share gain", "\n", avg_daily_returns_per_share, "\n")

daily_return_percent = (daily_return / df["Open"]) * 100
avg_daily_returns_percent = sum(daily_return_percent) / number_of_days
print("Avg Daily Returns Percent", "\n", avg_daily_returns_percent, "\n")


# Stock volatility
#   https://www.investopedia.com/terms/v/volatility.asp
#   Find the mean of the data set.
#   Calculate the difference between each data value and the mean aka deviation.
#   Square the deviations.
#   Add the squared deviations together.
#   Divide the sum of the squared deviations by the number of data values.
close_mean = df["Close"].mean()
deviation = df["Close"] - close_mean
square_deviations = deviation ** 2
variance = square_deviations.mean()
print("Variance Calculation:", variance)

variance_sum = sum(square_deviations)
variance_ct = len(square_deviations)
variance_manual = variance_sum / variance_ct
print("Variance Manual Calculation:", variance_manual)


# The maximum drawdown
#   https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp
#   Identify Peak Value of Portfolio
#   Identify Trough Value of Portfolio
#   Subtract Trough Value by Peak Value of Portfolio
#   Divide Difference (Trough – Peak) by Peak Value
peak_value = df["Close"].max()
trough_value = df["Close"].min()
difference_trough_peak = trough_value - peak_value
maximum_drawdown = difference_trough_peak / peak_value
print("Maximum Drawdown:", maximum_drawdown)


# Moving averages
#   https://www.investopedia.com/terms/s/sma.asp
#   Simple moving average
window_x = 5
simple_moving_average_x_days = df['Close'].rolling(window_x).mean()
print("simple moving average five day:", "\n", simple_moving_average_x_days)

#   https://www.investopedia.com/articles/technical/060401.asp
#   Weighted Moving Average
wma_df = df[["Close"]].copy()
wma_df["weight"] = pd.Series(reversed(range(len(df.index) + 1))) / ((window_x * (window_x + 1)) / 2)
wma_df["price_time_period"] = wma_df["Close"] * wma_df["weight"]
print("Price time period:", "\n", wma_df["price_time_period"].sum())


# Volume analysis
# https://www.investopedia.com/terms/v/volume-analysis.asp
# https://www.investopedia.com/terms/p/pvi.asp
# Next time, I would also try using a package like pandas-ta (https://github.com/twopirllc/pandas-ta) to do this to avoid potential miscalculations.

# positive_volume_index
pvi_df = df[["Close", "Volume"]].copy()
pvi_df['positive_volume_index'] = 0.0
pvi_df.at[0, 'positive_volume_index'] = pvi_df.at[0, 'Close']

for i in range(1, len(pvi_df)):
    if pvi_df['Volume'].iloc[i] > pvi_df['Volume'].iloc[i - 1]:
        pvi_df.at[i, 'positive_volume_index'] = pvi_df['positive_volume_index'].iloc[i - 1] + (
                (pvi_df['Close'].iloc[i] - pvi_df['Close'].iloc[i - 1]) / pvi_df['Close'].iloc[i - 1]) * \
                                                pvi_df['positive_volume_index'].iloc[i - 1]
    else:
        pvi_df.at[i, 'positive_volume_index'] = pvi_df.at[i - 1, 'positive_volume_index']
print("Positive volume index:", pvi_df['positive_volume_index'])

# negative_volume_index
# https://www.investopedia.com/terms/n/nvi.asp
nvi_df = df[["Close", "Volume"]].copy()
nvi_df['negative_volume_index'] = 0.0
nvi_df.at[0, 'negative_volume_index'] = nvi_df.at[0, 'Close']

for i in range(1, len(nvi_df)):
    if nvi_df['Volume'].iloc[i] < nvi_df['Volume'].iloc[i - 1]:
        nvi_df.at[i, 'negative_volume_index'] = nvi_df['negative_volume_index'].iloc[i - 1] + (
                (nvi_df['Close'].iloc[i] - nvi_df['Close'].iloc[i - 1]) / nvi_df['Close'].iloc[i - 1]) * \
                                                nvi_df['negative_volume_index'].iloc[i - 1]
    else:
        nvi_df.at[i, 'negative_volume_index'] = nvi_df.at[i - 1, 'negative_volume_index']
print("Negative volume index:", nvi_df['negative_volume_index'])



# Visualize the stock price trends using Matplotlib
# Candlestick patterns
#   https://www.investopedia.com/trading/candlestick-charting-what-is-it/
candlestick_df = df.copy()
candlestick_df = candlestick_df.set_index('Date')

plt.figure()

# closing stock price is >= to the opening stock prices
closing_gtr_or_eq_opening = candlestick_df[candlestick_df.Close >= candlestick_df.Open]
# closing stock price is < to the opening stock prices
closing_less_opening = candlestick_df[candlestick_df.Close < candlestick_df.Open]

color_decrease = 'red'
color_increase = 'green'

width_real_body = .4
width_shadows = .04

plt.bar(closing_gtr_or_eq_opening.index, closing_gtr_or_eq_opening.Close - closing_gtr_or_eq_opening.Open,
        width_real_body, bottom=closing_gtr_or_eq_opening.Open, color=color_decrease)
plt.bar(closing_gtr_or_eq_opening.index, closing_gtr_or_eq_opening.High - closing_gtr_or_eq_opening.Close,
        width_shadows, bottom=closing_gtr_or_eq_opening.Close, color=color_decrease)
plt.bar(closing_gtr_or_eq_opening.index, closing_gtr_or_eq_opening.Low - closing_gtr_or_eq_opening.Open, width_shadows,
        bottom=closing_gtr_or_eq_opening.Open, color=color_decrease)

plt.bar(closing_less_opening.index, closing_less_opening.Close - closing_less_opening.Open, width_real_body,
        bottom=closing_less_opening.Open, color=color_increase)
plt.bar(closing_less_opening.index, closing_less_opening.High - closing_less_opening.Open, width_shadows,
        bottom=closing_less_opening.Open, color=color_increase)
plt.bar(closing_less_opening.index, closing_less_opening.Low - closing_less_opening.Close, width_shadows,
        bottom=closing_less_opening.Close, color=color_increase)

plt.xticks(rotation=30, ha='right')

plt.show()


# Seasonality
#   https://www.investopedia.com/terms/s/seasonality.asp
axes = plt.gca()
seasonality_df = df.copy()
seasonality_df = seasonality_df.set_index('Date')
seasonality_df.plot(kind='line', y='Close', ax=axes)
seasonality_df.plot(kind='line', y='Open', ax=axes)
seasonality_df.plot(kind='line', y='High', ax=axes)
seasonality_df.plot(kind='line', y='Low', ax=axes)
xcoords = ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01', '2022-06-01',
           '2022-07-01', '2022-08-01', '2022-09-01', '2022-10-01', '2022-11-01', '2022-12-01']
for xc in xcoords:
    plt.axvline(x=xc, color='black', linestyle='--')
plt.show()
