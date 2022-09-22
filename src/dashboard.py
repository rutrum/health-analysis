from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import toml
import sqlite3
import plotly.graph_objects as go
import json
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

def dict_to_table(d):
    rows = []
    for key, val in d.items():
        rows.append(html.Tr([
            html.Th(key),
            html.Th(val),
        ]))
    return html.Table(rows)

def build_summary(daily, date):
    """ generates some summary html for the given date """
    row = daily.loc[daily["date"] == date].iloc[0, :].to_dict()
    data = {
        "Date": row["date"],
        "Weight": round(row["interpolated_weight"], 1),
        "Avg. Weight": round(row["average_weight"], 1),
        "Images Taken": row["total_images"],
    }
    return dict_to_table(data)

def main():
    config = load_config()

    conn = sqlite3.connect(config["prepared"]["sqlite"])
    daily = pd.read_sql("SELECT * FROM daily", con=conn)

    app.layout = html.Div(children=[
        date_range(daily),
        dcc.Graph(id="daily"),
        html.Pre(["test"], id="summary"),
    ])

    inspect_date = daily["date"].min()

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
            go.Scatter(x=df["date"], y=df["interpolated_weight"], name="Weight (Interpolated)")
        )
        avg_days = config["extend"]["avg_weight_window"]
        fig.add_trace(
            go.Scatter(x=df["date"], y=df["average_weight"], name=f"{avg_days} day average")
        )
        fig.add_trace(
            go.Scatter(x=df["date"], y=df["weight"], name="Weight", visible='legendonly')
        )

        fig.add_trace(
            go.Bar(x=df["date"], y=df["total_images"], name="Total Images"),
            secondary_y = True,
        )

        return fig

    @app.callback(
        Output('summary', 'children'),
        Input('daily', 'clickData')
    )
    def display_click_data(click_data):
        if not click_data: return
        inspect_date = click_data["points"][0]["x"]
        return build_summary(daily, inspect_date)

    app.run_server(debug=True)

if __name__ == "__main__":
    main()
