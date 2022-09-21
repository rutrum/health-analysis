import toml
import pandas as pd
import os
from datetime import datetime

def load_config():
    with open("config.toml") as f:
        return toml.load(f)

def time_from_filename(filename):
    """
    Five? cases:
        20210703_163126.jpg
        IMG_20201002_133606.jpg
        20210626_192712_HDR.jpg
        20210606_095151_Burst01.jpg
        IMG_20200902_083855_1.jpg
    """
    stem = filename.split(".")[0]
    if filename[16:19] == "HDR":
        stem = stem[:15]
    elif filename[:3] == "IMG":
        stem = stem[4:]
    elif filename[16:21] == "Burst":
        stem = stem[:15]

    stem = stem[:14] # removes the _1 for duplicates

    dt = datetime.strptime(stem, "%Y%m%d_%H%M%S")
    return dt.timestamp()

def main():
    config = load_config()

    pic_dir = config["sources"]["food_images"]

    data = []
    for filename in os.listdir(pic_dir):
        timestamp = time_from_filename(filename)
        data.append([timestamp, filename])

    df = pd.DataFrame(data, columns=["timestamp", "filename"])
    out = config["cleaned"]["food_images_meta"]
    df.to_csv(out, index=False)


if __name__ == "__main__":
    main()
