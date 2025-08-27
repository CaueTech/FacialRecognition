import os
import pickle
import numpy as np
import shutil
from deepface import DeepFace
import matplotlib.pyplot as plt

class FaceRecognizer:
    """
    Classe equipada com criação do modelo, vetores descritores (embeddings),
    criação e atualização do banco de dados facial, e reconhecimento facial.
    """
    def __init__(self, model_name="Facenet"):
        # Nome do modelo de reconhecimento facial a ser utilizado
        self.model_name = model_name
        # Dicionário que armazenará os vetores de características faciais
        self.face_database = {}

    def _generate_embedding(self, img_path):
        # Gera o vetor descritor (embedding) de uma imagem facial
        try:
            embedding_obj = DeepFace.represent(
                img_path=img_path,
                model_name=self.model_name,
                enforce_detection=False  # Permite processar imagens mesmo se a face não for detectada
            )
            # Retorna o vetor de características da face encontrada
            return embedding_obj[0]["embedding"]
        except Exception as e:
            print(f"Erro ao gerar embedding para {img_path}: {e}")
            return None

    def build_database(self, db_path, db_file_name="face_db.pkl"):
        # Carrega ou cria um novo banco de dados
        if os.path.exists(db_file_name):
            print(f"Carregando banco de dados existente de '{db_file_name}'...")
            with open(db_file_name, "rb") as f:
                self.face_database = pickle.load(f)
            print("Banco de dados carregado com sucesso.")
        else:
            print(f"Nenhum banco de dados encontrado. Criando novo banco a partir de '{db_path}'...")
            # Percorre as pastas de pessoas no diretório fornecido
            for person_name in os.listdir(db_path):
                person_folder_path = os.path.join(db_path, person_name)

                if os.path.isdir(person_folder_path):
                    # Cria lista para armazenar os vetores dessa pessoa
                    self.face_database[person_name] = []
                    for image_name in os.listdir(person_folder_path):
                        image_path = os.path.join(person_folder_path, image_name)
                        embedding = self._generate_embedding(image_path)
                        if embedding:
                            self.face_database[person_name].append(embedding)
                            print(f"Imagem processada: {image_path}")

            # Salva o banco de dados em arquivo
            with open(db_file_name, "wb") as f:
                pickle.dump(self.face_database, f)
            print(f"\nBanco de dados criado e salvo em '{db_file_name}'!")

    def add_person_to_database(self, person_name, source_image_path, post_processed_base_path, db_file_name):
        # Adiciona nova pessoa ao database, com suas propriedades
        print(f"\n--- Adicionando nova pessoa: {person_name} ---")
        if not os.path.exists(source_image_path):
            print(f"Aviso: Imagem de origem não encontrada em '{source_image_path}'")
            return

        # Cria a nova pasta da pessoa e copia a imagem para lá
        destination_folder = os.path.join(post_processed_base_path, person_name)
        os.makedirs(destination_folder, exist_ok=True)
        destination_image_path = os.path.join(destination_folder, os.path.basename(source_image_path))
        shutil.copy2(source_image_path, destination_image_path)
        print(f"Imagem copiada de '{source_image_path}' para '{destination_image_path}'")

        # Gera o vetor descritor da nova imagem
        embedding = self._generate_embedding(destination_image_path)

        # Atualiza o dicionário do banco de dados com o novo vetor
        if embedding:
            if person_name not in self.face_database:
                self.face_database[person_name] = []
            self.face_database[person_name].append(embedding)
            print(f"Embedding de '{person_name}' adicionado com sucesso ao banco de dados.")

            # Salva novamente o arquivo do banco de dados com os dados atualizados
            with open(db_file_name, "wb") as f:
                pickle.dump(self.face_database, f)
            print(f"Arquivo do banco de dados '{db_file_name}' atualizado.")

    def recognize(self, img_path):
        """
        Reconhece uma face presente em uma imagem comparando com o banco de dados carregado.
        Retorna o nome da pessoa mais próxima (menor distância euclidiana).
        """
        if not self.face_database:
            print("Erro: banco de dados vazio. Execute build_database() primeiro.")
            return None

        # Gera o vetor descritor da imagem de teste
        mystery_vector = self._generate_embedding(img_path)
        if not mystery_vector:
            return None

        best_match_name = ""
        smallest_distance = float('inf')  # Inicializa com infinito

        # Compara a imagem com cada vetor do banco de dados
        for person_name, vectors in self.face_database.items():
            for vector in vectors:
                distance = np.linalg.norm(np.array(mystery_vector) - np.array(vector))  # Distância Euclidiana
                if distance < smallest_distance:
                    smallest_distance = distance
                    best_match_name = person_name

        return {"identity": best_match_name, "distance": smallest_distance}

# --- CONFIGURAÇÕES GERAIS DO PROGRAMA ---
DB_PATH = "./database/"  # Caminho das pastas com imagens
MYSTERY_IMAGE_PATH = os.path.join(DB_PATH, "pessoa_com_mascara.jpg")  # Imagem a ser reconhecida
MODEL_NAME = "Facenet"  # Modelo facial utilizado
DB_FILE_NAME = "face_db.pkl"  # Nome do arquivo que armazenará o banco
POST_PROCESSED_PATH = "post-processed/"  # Pasta onde ficarão as imagens processadas

# Caminho da imagem de G.G Santos que será adicionada ao banco
GGSantosSOURCE_IMG = os.path.join(DB_PATH, "pessoa_sem_mascara.jpg")

# 1. Cria uma instância do motor de reconhecimento facial
recognizer = FaceRecognizer(model_name=MODEL_NAME)

# 2. Constrói ou carrega o banco de dados inicial (sem G.G Santos)
recognizer.build_database(db_path=DB_PATH, db_file_name=DB_FILE_NAME)

# 3. Adiciona a imagem do G.G Santos de forma separada, após o banco inicial estar pronto
recognizer.add_person_to_database(
    person_name="G. G. Santos",
    source_image_path=GGSantosSOURCE_IMG,
    post_processed_base_path=POST_PROCESSED_PATH,
    db_file_name=DB_FILE_NAME
)

# 4. Realiza o reconhecimento facial com a imagem de inferência
print("\nIniciando reconhecimento facial...")
result = recognizer.recognize(img_path=MYSTERY_IMAGE_PATH)

# 5. Mostra os resultados
if result:
    print("\n--- RECONHECIMENTO COMPLETO ---")
    print(f"Pessoa identificada: {result['identity']}")
    print(f"Pontuação de confiança (distância): {result['distance']:.4f}")
    print("(Pontuação menor indica maior similaridade/confiança na identificação)")

    # Exibe a imagem com o nome da pessoa identificada
    try:
        img = plt.imread(MYSTERY_IMAGE_PATH)
        plt.imshow(img)
        plt.title(f"Imagem de Teste\nIdentificado como: {result['identity']}")
        plt.axis('off')
        plt.show()
    except FileNotFoundError:
        print(f"\nErro: imagem de teste '{MYSTERY_IMAGE_PATH}' não encontrada para exibição.")