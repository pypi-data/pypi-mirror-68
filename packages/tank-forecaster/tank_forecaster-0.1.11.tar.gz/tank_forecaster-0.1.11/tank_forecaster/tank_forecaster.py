import numpy as np
import pandas as pd
import statsmodels.api as sm
from datetime import timedelta

DEFAULT_INTERVAL = timedelta(minutes=10)
DEFAULT_PERIODS = 6 * 48  # 10 mins * 6 * 48 = 2 days


def generate_future_periods(df, periods):
    start_0 = df.iloc[0, 0]
    return pd.date_range(start=start_0, freq="10min", periods=periods)


def sarimax_mod(df, prediction_count):
    mod = sm.tsa.SARIMAX(df.y, order=(8, 0, 0))
    res = mod.fit()
    return res.get_prediction(start=0, end=prediction_count).summary_frame()


def forecast(df, interval=DEFAULT_INTERVAL, periods=DEFAULT_PERIODS, model="ar"):
    time = interval / timedelta(minutes=10)
    periods = time * periods

    future = generate_future_periods(df, periods=periods)

    predictions = sarimax_mod(df, len(future))

    out = pd.concat([pd.Series(future), predictions], axis=1)[
        "ds", "yhat", "se", "lower", "upper"
    ]

    for field in ["yhat", "lower", "upper"]:
        out.loc[out[field] < 0, field] = 0
        out[field] = out[field].groupby(out.index // time).cumsum()

    out = out[(out.index + 1) % time == 0]

    return {
        "forecast_status": "success",
        "data": out.to_dict(orient="records"),
    }
