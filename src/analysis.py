"""Download public apparel retail sales data, analyse trends, and compare forecasts."""
from pathlib import Path
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.holtwinters import ExponentialSmoothing

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "outputs"
SERIES_ID = "MRTSSM448US"
SOURCE_URL = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={SERIES_ID}"
HOLDOUT_MONTHS = 12
FORECAST_MONTHS = 12


def load_series() -> pd.Series:
    """Download and validate the monthly FRED series."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(SOURCE_URL)
    if raw.shape[1] < 2:
        raise ValueError("Unexpected FRED CSV format; inspect the source URL.")
    date_col, value_col = raw.columns[0], raw.columns[1]
    raw[date_col] = pd.to_datetime(raw[date_col], errors="coerce")
    raw[value_col] = pd.to_numeric(raw[value_col], errors="coerce")
    raw = raw.dropna(subset=[date_col, value_col]).sort_values(date_col)
    raw.to_csv(RAW_DIR / f"{SERIES_ID}.csv", index=False)
    series = pd.Series(raw[value_col].to_numpy(),
                       index=pd.DatetimeIndex(raw[date_col], name="date"),
                       name="sales_millions_usd")
    series = series[~series.index.duplicated(keep="last")].asfreq("MS").dropna()
    if len(series) < 36:
        raise ValueError(f"Only {len(series)} monthly observations found; need at least 36.")
    return series


def seasonal_naive(train: pd.Series, horizon: int) -> np.ndarray:
    """Repeat the latest observed 12-month seasonal pattern."""
    if len(train) < 12:
        return np.repeat(train.iloc[-1], horizon)
    return np.array([train.iloc[-12 + (i % 12)] for i in range(horizon)])


def moving_average_forecast(train: pd.Series, horizon: int) -> np.ndarray:
    """Iterative 12-month moving-average forecast."""
    history = list(train.astype(float))
    predictions = []
    for _ in range(horizon):
        prediction = float(np.mean(history[-12:]))
        predictions.append(prediction)
        history.append(prediction)
    return np.asarray(predictions)


def holt_winters_forecast(train: pd.Series, horizon: int) -> np.ndarray:
    """Fit additive-trend, additive-seasonality Holt-Winters model."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = ExponentialSmoothing(
            train.astype(float), trend="add", seasonal="add",
            seasonal_periods=12, initialization_method="estimated"
        ).fit(optimized=True)
    return np.asarray(model.forecast(horizon), dtype=float)


def calculate_metrics(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    mae = float(mean_absolute_error(actual, predicted))
    rmse = float(np.sqrt(mean_squared_error(actual, predicted)))
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    nonzero = actual != 0
    mape = (float(np.mean(np.abs((actual[nonzero] - predicted[nonzero]) /
                                 actual[nonzero])) * 100)
            if nonzero.any() else float("nan"))
    return {"MAE": mae, "RMSE": rmse, "MAPE_percent": mape}


def save_plots(series: pd.Series, forecast: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.plot(series.index, series.values, label="Monthly retail sales", linewidth=1)
    ax.plot(series.index, series.rolling(12).mean(),
            label="12-month rolling average", linewidth=2)
    ax.set(title="U.S. Clothing Store Retail Sales", xlabel="Month",
           ylabel="Millions of current U.S. dollars")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "historical_trend.png", dpi=160)
    plt.close(fig)

    month_profile = series.groupby(series.index.month).mean().reindex(range(1, 13))
    labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, month_profile.values)
    ax.set(title="Average Sales by Calendar Month", xlabel="Calendar month",
           ylabel="Average millions of current USD")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "monthly_seasonality.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.plot(series.index, series.values, label="Observed history", linewidth=1.3)
    ax.plot(forecast.index, forecast["forecast"],
            label="Selected model forecast", linewidth=2)
    ax.fill_between(forecast.index, forecast["lower_approx"],
                    forecast["upper_approx"], alpha=0.2,
                    label="Approximate 80% range")
    ax.set(title="12-Month Apparel Retail Sales Forecast", xlabel="Month",
           ylabel="Millions of current U.S. dollars")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "forecast.png", dpi=160)
    plt.close(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    series = load_series()
    if len(series) <= HOLDOUT_MONTHS + 24:
        raise ValueError("Not enough observations for holdout and seasonal model.")

    train, test = series.iloc[:-HOLDOUT_MONTHS], series.iloc[-HOLDOUT_MONTHS:]
    candidates = {
        "Seasonal naive": seasonal_naive(train, len(test)),
        "12-month moving average": moving_average_forecast(train, len(test)),
        "Holt-Winters additive": holt_winters_forecast(train, len(test)),
    }
    rows = [{"model": name, **calculate_metrics(test.to_numpy(), prediction)}
            for name, prediction in candidates.items()]
    comparison = pd.DataFrame(rows).sort_values("MAE")
    comparison.to_csv(OUT_DIR / "model_comparison.csv", index=False)

    best_name = str(comparison.iloc[0]["model"])
    forecast_functions = {
        "Seasonal naive": seasonal_naive,
        "12-month moving average": moving_average_forecast,
        "Holt-Winters additive": holt_winters_forecast,
    }
    point = forecast_functions[best_name](series, FORECAST_MONTHS)
    future_index = pd.date_range(series.index[-1] + pd.offsets.MonthBegin(1),
                                 periods=FORECAST_MONTHS, freq="MS")

    # Approximate residual-based range; not a formal model prediction interval.
    residuals = test.to_numpy() - candidates[best_name]
    residual_sd = float(np.std(residuals, ddof=1))
    spread = 1.2816 * residual_sd * np.sqrt(np.arange(1, FORECAST_MONTHS + 1))
    forecast = pd.DataFrame({
        "date": future_index,
        "forecast": point,
        "lower_approx": np.maximum(0, point - spread),
        "upper_approx": point + spread,
    }).set_index("date")
    forecast.to_csv(OUT_DIR / "forecast_12_months.csv", index_label="date")

    yoy = series.pct_change(12).dropna() * 100
    recent_yoy_mean = float(yoy.iloc[-12:].mean())
    monthly_means = series.groupby(series.index.month).mean()
    strongest = pd.Timestamp(2000, int(monthly_means.idxmax()), 1).strftime("%B")
    weakest = pd.Timestamp(2000, int(monthly_means.idxmin()), 1).strftime("%B")
    save_plots(series, forecast)

    summary = [
        "# Generated Analysis Summary", "",
        f"- Data source: FRED series {SERIES_ID} ({SOURCE_URL})",
        f"- Latest observation: {series.index[-1].date()}",
        f"- Observations used: {len(series)} monthly values",
        f"- Latest sales observation: \${series.iloc[-1]:,.1f} million, nominal and seasonally adjusted",
        f"- Mean year-over-year change over the latest 12 available comparisons: {recent_yoy_mean:.2f}%",
        f"- Highest average calendar-month sales: {strongest}",
        f"- Lowest average calendar-month sales: {weakest}",
        f"- Best holdout model by MAE: **{best_name}**", "",
        "## Holdout comparison", "",
        comparison.to_markdown(index=False, floatfmt=".2f"), "",
        "## Interpretation cautions", "",
        "- Values are nominal U.S. dollars; they are not inflation-adjusted unit sales.",
        "- The month profile is descriptive and may reflect holidays, promotions, and channel mix.",
        "- The forecast range is approximate, not a formal prediction interval.",
        "- The forecast is a historical-pattern scenario, not a guarantee or causal explanation.",
        "- Review the model metrics and charts before writing numerical conclusions."
    ]
    (OUT_DIR / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(f"Analysis complete. Outputs saved to: {OUT_DIR}")
    print(comparison.to_string(index=False))
    print(f"Selected model: {best_name}")


if __name__ == "__main__":
    main()
