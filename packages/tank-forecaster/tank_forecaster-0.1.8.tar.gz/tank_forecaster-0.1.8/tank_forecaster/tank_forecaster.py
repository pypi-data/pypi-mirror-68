import numpy as np
import pandas as pd
import statsmodels.api as sm
from datetime import timedelta

DEFAULT_INTERVAL = timedelta(minutes=10)
DEFAULT_PERIODS = 6 * 48  # 10 mins * 6 * 48 = 2 days


def forecast(df, interval=timedelta(minutes=10), periods=6 * 48, model="ar"):

    # set the frequency and period according to this multiple of 10 minutes
    # the function always predicts in 10 minute intervals, you just see the rolled up version
    time = interval / timedelta(minutes=10)
    periods = time * periods

    # use pd.date_range to create datestamps for user defined period (unused 10 min intervals dropped later)
    def forecaster(df, periods=periods):
        start_0 = df.iloc[0, 0]
        future = pd.date_range(start=start_0, freq="10min", periods=periods)
        return future

    # predictions made will be based off the length of this vector, they are in no way related to the actual days
    future = forecaster(df, periods=periods)

    #  AR(8) model function
    def sarimax_mod(df, num_preds=len(future)):
        mod = sm.tsa.SARIMAX(df.y, order=(8, 0, 0))
        res = mod.fit()
        preds = res.get_prediction(start=0, end=num_preds).summary_frame()
        return preds

    preds = sarimax_mod(df)

    out = pd.concat([pd.Series(future), preds], axis=1)
    out.columns = ["ds", "yhat", "se", "lower", "upper"]

    out.loc[out.lower < 0, "lower"] = 0

    out["yhat"] = out["yhat"].groupby(out.index // time).cumsum()
    out["lower"] = out["lower"].groupby(out.index // time).cumsum()
    out["upper"] = out["upper"].groupby(out.index // time).cumsum()
    out = out[(out.index + 1) % time == 0]

    return {
        "forecast_status": "success",
        "data": out.to_dict(orient="records"),
    }
