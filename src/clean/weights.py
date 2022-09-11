import toml
import subprocess
import pandas as pd
from datetime import datetime

def load_config():
    with open("config.toml") as f:
        return toml.load(f)

def convert_ods(path):
    subprocess.call([
        "libreoffice",
        "--headless",
        "--convert-to",
        "csv",
        "--outdir",
        "/tmp",
        path,
    ])

    basename = path.split("/")[-1]
    filestem = basename.split(".")[0]
    return f"/tmp/{filestem}.csv"

def main():
    config = load_config()

    ods_path = config["sources"]["weights"]
    csv_path = convert_ods(ods_path)

    df = pd.read_csv(csv_path, names=["date", "weight", "comment"])

    df["date"] = pd.to_datetime(df["date"]).map(pd.Timestamp.timestamp)

    df.to_csv(config["cleaned"]["weights"], index=False)


if __name__ == "__main__":
    main()
