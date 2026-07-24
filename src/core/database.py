import os
import pickle
import shutil


class FaceDatabase:

    def __init__(self, embedding_generator):
        self.embedding_generator = embedding_generator
        self.database = {}

    def load(self, db_file):

        with open(db_file, "rb") as f:
            self.database = pickle.load(f)

        print("Banco carregado.")

    def save(self, db_file):

        with open(db_file, "wb") as f:
            pickle.dump(self.database, f)

        print("Banco salvo.")

    def build(self, database_path):

        self.database = {}

        for person in os.listdir(database_path):

            print(f"Pessoa: {person}")

            person_folder = os.path.join(database_path, person)

            if not os.path.isdir(person_folder):
                continue

            self.database[person] = []

            for image in os.listdir(person_folder):

                print(f"    Imagem: {image}")

                image_path = os.path.join(person_folder, image)

                embedding = self.embedding_generator.generate(image_path)

    def add_person(
        self,
        person_name,
        source_image,
        destination_root
    ):
        print("person_name:", person_name)
        print("source_image:", source_image)
        print("destination_root:", destination_root)

        destination_folder = os.path.join(
            destination_root,
            person_name
        )

        print("destination_folder:", destination_folder)

        destination_folder = os.path.join(
            destination_root,
            person_name
        )

        os.makedirs(destination_folder, exist_ok=True)

        destination_image = os.path.join(
            destination_folder,
            os.path.basename(source_image)
        )

        shutil.copy2(source_image, destination_image)

        embedding = self.embedding_generator.generate(destination_image)

        if embedding is None:
            return

        if person_name not in self.database:
            self.database[person_name] = []

        self.database[person_name].append(embedding)