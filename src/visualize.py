from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import toml
import sqlite3

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

    conn = sqlite3.connect(config["prepare"]["out"]["sqlite"])
    df = pd.read_sql("select * from weight", con=conn)
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")

    app.layout = html.Div(children=[
        date_range(df),
        dcc.Graph(id="weight_over_time"),
    ])

    @app.callback(
        Output("weight_over_time", "figure"),
        Input("date_picker", "start_date"),
        Input("date_picker", "end_date"),
    )
    def update_weight_over_time(start_date, end_date):
        print(start_date, end_date)
        filtered = df
        if start_date and end_date:
            filtered = df[df.date < end_date]
            filtered = filtered[df.date > start_date]
        return px.line(filtered, x="date", y="weight", markers=True)

    app.run_server(debug=True)

if __name__ == "__main__":
    main()
