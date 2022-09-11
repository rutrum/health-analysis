from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import toml
import sqlite3

def load_config():
    with open("config.toml") as f:
        return toml.load(f)

def weight_over_time(df):
    return px.line(df, x="date", y="weight", markers=True)

def main():
    config = load_config()
    app = Dash(__name__)

    conn = sqlite3.connect(config["prepare"]["out"]["sqlite"])
    df = pd.read_sql("select * from weight", con=conn)
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")

    app.layout = html.Div(children=[
        dcc.Graph(figure=weight_over_time(df))
    ])

    app.run_server(debug=True)

if __name__ == "__main__":
    main()
