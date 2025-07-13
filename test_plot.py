import pandas as pd
import plotly.graph_objects as go
from prophet import Prophet

df = pd.read_csv("data/btc2.csv")[["Date", "Open"]]
df.columns = ["ds", "y"]
df["ds"] = pd.to_datetime(df["ds"])
df["y"] = pd.to_numeric(df["y"], errors="coerce")
df.dropna(inplace=True)

m = Prophet(seasonality_mode="multiplicative")
m.fit(df)
future = m.make_future_dataframe(periods=100)
forecast = m.predict(future)

fig = go.Figure()
fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"], name="Forecast", line=dict(color="red")))
fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_upper"], name="Upper", line=dict(color="lightblue")))
fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_lower"], name="Lower", line=dict(color="lightblue")))
fig.add_trace(go.Scatter(x=df["ds"], y=df["y"], name="Actual", line=dict(color="purple")))
fig.update_layout(title="Test Forecast", xaxis_title="Date", yaxis_title="Price")
fig.show()
