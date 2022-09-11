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
        min_date_allowed=df["date_formatted"].min(),
        start_date=df["date_formatted"].min(),
        max_date_allowed=df["date_formatted"].max(),
        end_date=df["date_formatted"].max(),
    )

def main():
    config = load_config()

    conn = sqlite3.connect(config["prepared"]["sqlite"])
    weight = pd.read_sql("""
        select *, date(meals.timestamp, 'unixepoch') as date_formatted from weight
        join (
            select timestamp, sum(total_posts) as total_posts from meals
            group by date(timestamp, 'unixepoch')
        ) as meals
        where date(meals.timestamp, 'unixepoch') == date(weight.date, 'unixepoch')
    """, con=conn)

    app.layout = html.Div(children=[
        date_range(weight),
        dcc.Graph(id="weight_over_time"),
    ])

    @app.callback(
        Output("weight_over_time", "figure"),
        Input("date_picker", "start_date"),
        Input("date_picker", "end_date"),
    )
    def update_weight_over_time(start_date, end_date):
        df = weight
        if start_date and end_date:
            df = weight[weight.date_formatted < end_date]
            df = df[weight.date_formatted > start_date]

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(x=df["date_formatted"], y=df["weight"], name="Weight")
        )

        fig.add_trace(
            go.Bar(x=df["date_formatted"], y=df["total_posts"], name="Total Posts"),
            secondary_y = True,
        )

        return fig

    app.run_server(debug=True)

if __name__ == "__main__":
    main()
