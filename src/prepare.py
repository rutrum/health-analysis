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
    posts.to_sql(name="posts", con=conn, index=False)

    posts = pd.read_csv(config["clean"]["out"]["instagram_pictures"])
    posts.to_sql(name="pictures", con=conn, index=False)

    to_write = sqlite3.connect(config["prepare"]["out"]["sqlite"])
    conn.backup(to_write)


if __name__ == "__main__":
    main()
