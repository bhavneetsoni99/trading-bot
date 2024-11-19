import pandas as pd

# Use raw string notation to avoid issues with backslashes
file_path = (
    r"C:\Users\cheng\Desktop\MLTradingBot\logs\MLTrader_2024-08-05_00-14-22_trades.csv"
)
trades_df = pd.read_csv(file_path)

# Convert the 'time' column to datetime format with UTC handling
trades_df["time"] = pd.to_datetime(trades_df["time"], utc=True, errors="coerce")

# Inspect rows where 'time' conversion failed
failed_conversion = trades_df[trades_df["time"].isna()]
if not failed_conversion.empty:
    print("Rows with failed time conversion:")
    print(failed_conversion)

# Remove rows where 'time' conversion failed
trades_df = trades_df.dropna(subset=["time"])

# Extract the date from the 'time' column
trades_df["date"] = trades_df["time"].dt.date


# Function to check for day trades
def check_day_trades(group):
    has_buy = any(group["side"] == "buy")
    has_sell = any(group["side"] == "sell")
    return pd.Series({"day_trade": has_buy and has_sell})


# Group by symbol and date to find matching buy and sell trades on the same day
day_trades = trades_df.groupby(["symbol", "date"]).apply(check_day_trades).reset_index()

# Filter for day trades
day_trades = day_trades[day_trades["day_trade"]]

# Display the day trades
print(day_trades)
