import toml
import pandas as pd

def load_config():
    with open("config.toml") as f:
        return toml.load(f)

def main():
    config = load_config()

    weights = pd.read_csv(config["cleaned"]["weights"])
    weights["interpolated"] = weights["weight"].interpolate(method="linear")
    weights.to_csv(config["extended"]["interpolated_weights"], index=False)

if __name__ == "__main__":
    main()
