import os
import pickle
import sys

if sys.version_info < (3, 10):
    raise RuntimeError(
        "Python 3.10 ou superior é necessário."
    )

folders = [
    "assets/database",
    "assets/post-processed"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

db_file = "assets/face_db.pkl"

if not os.path.exists(db_file):
    with open(db_file, "wb") as f:
        pickle.dump({}, f)

print("Projeto preparado.")