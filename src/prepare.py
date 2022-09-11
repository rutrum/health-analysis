import toml
import pandas as pd
import sqlite3

def load_config():
    with open("config.toml") as f:
        return toml.load(f)

def main():
    config = load_config()

    conn = sqlite3.connect(":memory:")

    posts = pd.read_csv(config["clean"]["out"]["instagram_posts"])
    posts.to_sql(name="post", con=conn, index=False)

    posts = pd.read_csv(config["clean"]["out"]["instagram_pictures"])
    posts.to_sql(name="picture", con=conn, index=False)

    weights = pd.read_csv(config["clean"]["out"]["weights"])
    weights.to_sql(name="weight", con=conn, index=False)

    meals = pd.read_csv(config["extended"]["meals"])
    meals.to_sql(name="meals", con=conn, index=False)

    meals_posts = pd.read_csv(config["extended"]["meals_posts"])
    meals_posts.to_sql(name="meals_posts", con=conn, index=False)

    to_write = sqlite3.connect(config["prepare"]["out"]["sqlite"])
    conn.backup(to_write)


if __name__ == "__main__":
    main()
