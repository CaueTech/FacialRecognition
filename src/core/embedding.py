from deepface import DeepFace


class EmbeddingGenerator:

    def __init__(self, model_name="Facenet"):
        self.model_name = model_name

    def generate(self, img_path):
        try:
            embedding = DeepFace.represent(
                img_path=img_path,
                model_name=self.model_name,
                enforce_detection=False
            )

            return embedding[0]["embedding"]

        except Exception as e:
            print(f"Error generating embedding for '{img_path}': {e}")
            return None