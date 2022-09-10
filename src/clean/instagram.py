import toml
import json
import pandas as pd

def load_config():
    with open("config.toml") as f:
        return toml.load(f)

def load_posts(path):
    with open(f"{path}/content/posts_1.json") as f:
        return json.load(f)

def parse_posts(posts_raw):
    """
    Parses the json file containing all post metadata.  Returns two tables.
    The first containing every post, which will contain a caption, a timestamp,
    and a unique id (generated).  The second will contain a post id, a media url,
    timestamp, and a unique id (generated).
    """

    posts = []
    pictures = []

    post_id = 0
    picture_id = 0

    for post in posts_raw:
        if len(post["media"]) == 1:
            # Single image post
            post = post["media"][0]

            new_post = {
                "id": post_id,
                "timestamp": post["creation_timestamp"],
                "caption": post["title"],
            }
            posts.append(new_post)

            new_picture = {
                "id": picture_id,
                "post_id": post_id,
                "url": post["uri"],
            }
            pictures.append(new_picture)
            picture_id += 1

        else:
            # Multi-image post
            new_post = {
                "id": post_id,
                "timestamp": post["creation_timestamp"],
                "caption": post["title"],
            }

            for pic in post["media"]:
                new_picture = {
                    "id": picture_id,
                    "post_id": post_id,
                    "url": pic["uri"],
                }
                pictures.append(new_picture)
                picture_id += 1

        post_id += 1

    return pd.DataFrame(posts), pd.DataFrame(pictures)

def main():
    config = load_config()

    instagram_path = config["data"]["sources"]["instagram"]

    posts_raw = load_posts(instagram_path)

    posts, pictures = parse_posts(posts_raw)

    posts.to_csv(config["clean"]["out"]["instagram_posts"], index=False)
    pictures.to_csv(config["clean"]["out"]["instagram_pictures"], index=False)

if __name__ == "__main__":
    main()
