from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import toml
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Dash(__name__)

def load_config():
    with open("config.toml") as f:
        return toml.load(f)

def date_range(df):
    return dcc.DatePickerRange(
        id="date_picker",
        min_date_allowed=df["date"].min(),
        start_date=df["date"].min(),
        max_date_allowed=df["date"].max(),
        end_date=df["date"].max(),
    )

def main():
    config = load_config()

    conn = sqlite3.connect(config["prepared"]["sqlite"])
    daily = pd.read_sql("SELECT * FROM daily", con=conn)

    app.layout = html.Div(children=[
        date_range(daily),
        dcc.Graph(id="daily"),
    ])

    @app.callback(
        Output("daily", "figure"),
        Input("date_picker", "start_date"),
        Input("date_picker", "end_date"),
    )
    def update_weight_over_time(start_date, end_date):
        df = daily
        if start_date and end_date:
            df = daily[daily.date < end_date]
            df = df[daily.date > start_date]

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(x=df["date"], y=df["interpolated_weight"], name="Weight")
        )

        fig.add_trace(
            go.Bar(x=df["date"], y=df["total_posts"], name="Total Posts"),
            secondary_y = True,
        )

        return fig

    app.run_server(debug=True)

if __name__ == "__main__":
    main()
