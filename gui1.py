import pandas as pd
import plotly.graph_objects as go
from prophet import Prophet
import warnings
from tkinter import *
from PIL import ImageTk, Image
import time
import os

warnings.filterwarnings('ignore')

# Load and clean CSV data
eth_df = pd.read_csv("data/btc2.csv")
eth_df = eth_df[["Date", "Open"]]
eth_df.columns = ["ds", "y"]

# Clean the data
eth_df = eth_df[eth_df["ds"].notnull()]
eth_df = eth_df[eth_df["ds"].str.match(r"\d{4}-\d{2}-\d{2}")]
eth_df["ds"] = pd.to_datetime(eth_df["ds"])
eth_df["y"] = pd.to_numeric(eth_df["y"], errors="coerce")
eth_df.dropna(inplace=True)

# Forecasting
m = Prophet(seasonality_mode="multiplicative")
m.fit(eth_df)
future = m.make_future_dataframe(periods=100)
forecast = m.predict(future)

# Plotting
trace_open = go.Scatter(x=forecast["ds"], y=forecast["yhat"], mode='lines', line={"color": "#f50505"}, name="Forecast")
trace_high = go.Scatter(x=forecast["ds"], y=forecast["yhat_upper"], mode='lines', fill="tonexty", line={"color": "#57b8ff"}, name="Higher uncertainty interval")
trace_low = go.Scatter(x=forecast["ds"], y=forecast["yhat_lower"], mode='lines', fill="tonexty", line={"color": "#57b8ff"}, name="Lower uncertainty interval")
trace_close = go.Scatter(x=eth_df["ds"], y=eth_df["y"], name="Data values", line={"color": "#8a2be2"})

data = [trace_open, trace_high, trace_low, trace_close]

layout = go.Layout(
    title="BTC Stock Price Forecast",
    xaxis_rangeslider_visible=True,
    xaxis_title="Date",
    yaxis_title="Price"
)

fig = go.Figure(data=data, layout=layout)

# Optional: Show forecast plot in the browser
fig.show()

# Save the image for Tkinter GUI
output_path = "images/file.png"
fig.write_image(output_path)

# Wait until image is saved before loading
while not os.path.exists(output_path):
    print("Waiting for file.png to be saved...")
    time.sleep(1)

# GUI display
win = Tk()
win.geometry("700x500")
frame = Frame(win, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

img = ImageTk.PhotoImage(Image.open(output_path))
label = Label(frame, image=img)
label.pack()

def export():
    header = ["ds", "yhat_lower", "yhat_upper", "yhat"]
    forecast.to_csv('output.csv', columns=header, index=False)

B = Button(win, text="save to csv(output.csv)", command=export, fg='red', bg='white')
B.pack()
B.place(relx=0, rely=0, anchor='nw')

win.mainloop()


