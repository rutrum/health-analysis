import toml
import subprocess
import pandas as pd

def load_config():
    with open("config.toml") as f:
        return toml.load(f)

def build_meals(posts, meal_range_minutes):
    """ a meal is just a list of posts within a time frame, and the time it started """
    meals = []

    last_meal = {
        "time_started": "",
        "post_ids": [],
    }
    for i in range(len(posts) - 1):
        a = posts.loc[i]
        b = posts.loc[i + 1]

        if last_meal["time_started"] == "":
            last_meal["time_started"] = str(a["timestamp"])
            last_meal["post_ids"].append(a["id"])

        d = b["timestamp"] - a["timestamp"]
        total_minutes = d.total_seconds() / 60

        if total_minutes < meal_range_minutes:
            last_meal["post_ids"].append(b["id"])
        else:
            meals.append(last_meal)
            last_meal = {
                "time_started": "",
                "post_ids": [],
            }

    meals.append(last_meal)

    return pd.DataFrame(meals)

def split_meals(meals):
    """
    creates two tables to flatten meals.  First table is a meal, contains an
    id, timestamp.  The second table is a meal_post, which contains pairs
    of meals and post ids.
    """

    new_meals = []
    meal_posts = []

    for id, meal in meals.iterrows():
        new_meals.append({
            "id": id,
            "timestamp": meal["time_started"],
            "total_posts": len(meal["post_ids"]),
        })
        for post_id in meal["post_ids"]:
            meal_posts.append({
                "meal_id": id,
                "post_id": post_id,
            })

    return pd.DataFrame(new_meals), pd.DataFrame(meal_posts)

def main():
    config = load_config()

    posts = pd.read_csv(config["clean"]["out"]["instagram_posts"])

    posts["timestamp"] = pd.to_datetime(posts["timestamp"])

    meals = build_meals(posts, config["extend"]["meal_range_minutes"])
    meals, meals_posts = split_meals(meals)

    meals.to_csv(config["extended"]["meals"], index=False)
    meals_posts.to_csv(config["extended"]["meals_posts"], index=False)

if __name__ == "__main__":
    main()
