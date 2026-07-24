import os

from config import *

from core.embedding import EmbeddingGenerator
from core.database import FaceDatabase
from core.recognizer import FaceRecognizer

from utils.visualization import show_result
from utils.paths import *


embedding = EmbeddingGenerator(MODEL_NAME)

database = FaceDatabase(embedding)

if os.path.exists(DB_FILE):

    database.load(DB_FILE)

else:

    database.build(POST_PROCESSED)

    database.save(DB_FILE)

database.add_person(

    person_name=PERSON_NAME,

    source_image=os.path.join(
        INPUT,
        SOURCE_IMAGE
    ),

    destination_root=POST_PROCESSED
)

database.save(DB_FILE)

recognizer = FaceRecognizer(
    database,
    embedding
)

result = recognizer.recognize(

    os.path.join(
        INPUT,
        MYSTERY_IMAGE
    )
)

if result:

    print(result)

    show_result(
        os.path.join(
            INPUT,
            MYSTERY_IMAGE
        ),

        result
    )