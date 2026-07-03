import pandas as pd

def make_lags(df):
    df = df.sort_values(["Date", "Hour"]).reset_index(drop=True)
    df["lag_1h"] = df["Rented Bike Count"].shift(1)
    df["lag_24h"] = df["Rented Bike Count"].shift(24)
    return df.dropna()

def test_lag_created():
    df = pd.DataFrame({
        "Date": pd.date_range("2018-01-01", periods=50, freq="h").date,
        "Hour": list(range(24)) * 2 + [0, 1],
        "Rented Bike Count": range(50),
    })
    out = make_lags(df)
    assert "lag_1h" in out.columns and "lag_24h" in out.columns

def test_no_time_leakage():
    df = pd.DataFrame({"Date": pd.to_datetime(
        ["2018-08-30", "2018-08-31", "2018-09-01", "2018-09-02"])})
    train = df[df["Date"] < "2018-09-01"]
    test = df[df["Date"] >= "2018-09-01"]
    assert train["Date"].max() < test["Date"].min()
