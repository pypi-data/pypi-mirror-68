import numpy as np
import pandas as pd
import statsmodels.api as sm
from datetime import timedelta

DEFAULT_INTERVAL = timedelta(minutes=10)
DEFAULT_PERIODS = 6 * 48  # 10 mins * 6 * 48 = 2 days
DEFAULT_MODEL_OPTIONS = {"type": "areg"}


def generate_future_periods(df, periods):
    start_0 = df.iloc[0, 0]
    return pd.date_range(start=start_0, freq="10min", periods=periods)


def sarimax_mod(df, prediction_count):
    mod = sm.tsa.SARIMAX(df.y, order=(8, 0, 0))
    res = mod.fit()
    return res.get_prediction(start=0, end=prediction_count).summary_frame()


def forecast(
    df, interval=DEFAULT_INTERVAL, periods=DEFAULT_PERIODS, model_options=None
):

    model_options = model_options or DEFAULT_MODEL_OPTIONS

    interval_granularity_ratio = interval / timedelta(minutes=10)
    periods = interval_granularity_ratio * periods

    future = generate_future_periods(df, periods=periods)

    predictions = sarimax_mod(df, len(future))

    out = pd.concat([pd.Series(future), predictions], axis=1)[
        "ds", "yhat", "se", "lower", "upper"
    ]

    for field in ["yhat", "lower", "upper"]:
        out.loc[out[field] < 0, field] = 0
        out[field] = (
            out[field].groupby(out.index // interval_granularity_ratio).cumsum()
        )

    output_rows_to_keep = (out.index + 1) % interval_granularity_ratio == 0

    return {
        "forecast_status": "success",
        "data": out[output_rows_to_keep].to_dict(orient="records"),
    }
