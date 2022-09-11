all:
    just clean
    just prepare
    just explore

clean:
    python3 src/clean/instagram.py
    python3 src/clean/weights.py

prepare:
    python3 src/prepare.py

explore:
    sqlite3 data/prepared/data.db -readonly

schema:
    echo ".schema" | sqlite3 data/prepared/data.db
