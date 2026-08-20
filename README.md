# Face Recognition with DeepFace

A facial recognition system developed in Python using **DeepFace** and the **FaceNet** model. The application generates facial embeddings from a reference dataset, stores them locally, allows new identities to be added dynamically, and recognizes unknown faces by comparing embedding similarity.

This project was developed for academic purposes, focusing on the implementation and organization of a complete facial recognition pipeline.

---

## Features

- Facial embedding generation using FaceNet
- Local embedding database serialization (`face_db.pkl`)
- Automatic database creation from a dataset
- Dynamic addition of new identities
- Facial recognition using Euclidean distance
- Image visualization with recognition results
- Modular project structure

---

## Project Structure

```text
face-recognition/
│
├── assets/
│   ├── face_db.pkl
│   │
│   └── database/
│       ├── input/
│       └── post-processed/
│
├── src/
│   ├── core/
│   │   ├── recognizer.py
│   │   ├── embedding.py
│   │   └── database.py
│   │
│   ├── utils/
│   │   ├── visualization.py
│   │   └── paths.py
│   │
│   ├── config.py
│   └── main.py
│
├── scripts/
│   ├── setup.py
│   ├── install.sh
│   └── install.bat
│
├── README.md
└── .gitignore
```

---

## Pipeline

The application executes the following pipeline:

```text
Input Image
     │
     ▼
Load/Create Embedding Database
     │
     ▼
Generate Face Embeddings
     │
     ▼
Compare Against Database
     │
     ▼
Find Minimum Euclidean Distance
     │
     ▼
Display Identified Person
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd face-recognition
```

### Linux

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

### Windows

```bat
scripts\install.bat
```

The installation scripts automatically:

- create a virtual environment;
- install all required dependencies;
- prepare the project for execution.

---

## Running

Activate the virtual environment:

### Linux / macOS
```bash
source .venv/bin/activate
```

### Windows
```cmd
.venv\Scripts\activate
```

Once activated, run the application:

```bash
python src/main.py
```

---

## Configuration

The main configuration file is:

```text
src/config.py
```

It contains the parameters used during execution, including:

- Face recognition model
- Input image
- Image used to register a new identity
- Name assigned to the new identity

---

## How It Works

When executed, the application:

1. Checks whether `face_db.pkl` already exists.
2. If not, generates embeddings for every person in the reference dataset.
3. Saves the embedding database locally.
4. Adds a new identity to the database.
5. Generates an embedding for the input image.
6. Computes the Euclidean distance between the input embedding and every stored embedding.
7. Returns the closest match.

---

## Technologies

- Python
- DeepFace
- FaceNet
- TensorFlow
- OpenCV
- NumPy
- Matplotlib

---

## Notes

- The first execution may take several minutes because embeddings must be generated for the entire dataset.
- Once `face_db.pkl` has been created, subsequent executions are significantly faster.
- Deleting `face_db.pkl` forces the application to rebuild the embedding database.

---

## License

This project was developed for educational and academic purposes.