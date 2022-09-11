all:
    just clean
    just extend
    just prepare
    just explore

clean:
    python3 src/clean/instagram.py
    python3 src/clean/weights.py

extend:
    python3 src/extend/meals.py

prepare:
    python3 src/prepare.py

dash:
    python3 src/dashboard.py

explore:
    sqlite3 data/prepared/data.db

schema:
    echo ".schema" | sqlite3 data/prepared/data.db
