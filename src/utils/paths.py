import os

ROOT = os.path.dirname(os.path.dirname(__file__))

ASSETS = os.path.join(ROOT, "..", "assets")

DATABASE = os.path.join(
    ASSETS,
    "database"
)

INPUT = os.path.join(
    DATABASE,
    "input"
)

POST_PROCESSED = os.path.join(
    DATABASE,
    "post-processed"
)

DB_FILE = os.path.join(
    ASSETS,
    "face_db.pkl"
)