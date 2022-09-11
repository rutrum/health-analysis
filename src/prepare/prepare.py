import toml
import pandas as pd
import os
import sqlite3

def load_config():
    with open("config.toml") as f:
        return toml.load(f)

def main():
    config = load_config()

    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()

    # Load datasets into sqlite

    posts = pd.read_csv(config["cleaned"]["instagram_posts"])
    posts.to_sql(name="post", con=conn, index=False)

    posts = pd.read_csv(config["cleaned"]["instagram_pictures"])
    posts.to_sql(name="picture", con=conn, index=False)

    weights = pd.read_csv(config["cleaned"]["weights"])
    weights.to_sql(name="weight", con=conn, index=False)

    meals = pd.read_csv(config["extended"]["meals"])
    meals.to_sql(name="meals", con=conn, index=False)

    meals_posts = pd.read_csv(config["extended"]["meals_posts"])
    meals_posts.to_sql(name="meals_posts", con=conn, index=False)

    # Run arbitrary queries in sql folder to create views

    sql_dir = config["prepare"]["sql"]
    for filename in os.listdir(sql_dir):
        path = f"{sql_dir}/{filename}"
        with open(path) as f:
            cur.execute(f.read())

    # Write out

    to_write = sqlite3.connect(config["prepared"]["sqlite"])
    conn.backup(to_write)


if __name__ == "__main__":
    main()
