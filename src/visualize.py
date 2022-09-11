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
        min_date_allowed=df["date_formatted"].min(),
        start_date=df["date_formatted"].min(),
        max_date_allowed=df["date_formatted"].max(),
        end_date=df["date_formatted"].max(),
    )

def main():
    config = load_config()

    conn = sqlite3.connect(config["prepare"]["out"]["sqlite"])
    weight = pd.read_sql("""
        select *, date(meals.timestamp, 'unixepoch') as date_formatted from weight
        join meals
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
        filtered = weight
        if start_date and end_date:
            filtered = weight[weight.date_formatted < end_date]
            filtered = filtered[weight.date_formatted > start_date]
        fig = px.line(filtered, x="date_formatted", y="weight", markers=True)
        fig.add_bar(x=filtered["date_formatted"], y=filtered["total_posts"])

        return fig

    app.run_server(debug=True)

if __name__ == "__main__":
    main()
