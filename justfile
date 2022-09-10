all:
    just clean
    just prepare
    just explore

clean:
    python3 src/clean/instagram.py

prepare:
    python3 src/prepare.py

explore:
    sqlite3 data/prepared/data.db -readonly
