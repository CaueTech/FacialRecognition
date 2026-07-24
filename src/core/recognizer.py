import numpy as np


class FaceRecognizer:

    def __init__(self, database, embedding_generator):

        self.database = database
        self.embedding_generator = embedding_generator

    def recognize(self, image_path):

        mystery_embedding = self.embedding_generator.generate(image_path)

        if mystery_embedding is None:
            return None

        best_person = None
        best_distance = float("inf")

        for person, vectors in self.database.database.items():

            for vector in vectors:

                distance = np.linalg.norm(
                    np.array(mystery_embedding) -
                    np.array(vector)
                )

                if distance < best_distance:

                    best_distance = distance
                    best_person = person

        return {
            "identity": best_person,
            "distance": best_distance
        }