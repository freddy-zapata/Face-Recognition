import os
import cv2
import face_recognition
import psycopg2
import pickle
from imutils import paths
from database import get_db_connection

def save_encoding_to_db(id_persona, encoding):
    conn = get_db_connection()
    cur = conn.cursor()

    encoding_bin = pickle.dumps(encoding)
    cur.execute("INSERT INTO encodings (id_persona, encoding) VALUES (%s, %s);", 
                (id_persona, encoding_bin))
    conn.commit()
    cur.close()
    conn.close()

def train_model():
    print("[INFO] Procesando Imágenes...")
    imagePaths = list(paths.list_images("dataset"))

    for i, imagePath in enumerate(imagePaths):
        print(f"[INFO] Procesando imagen {i+1}/{len(imagePaths)}")

        folder_name = os.path.basename(os.path.dirname(imagePath))

        try:
            id_persona = int(folder_name.split('_')[0])
        except ValueError:
            print(f"[ERROR] La carpeta '{folder_name}' no tiene un formato válido para extraer id_persona.")
            continue

        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        boxes = face_recognition.face_locations(rgb, model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)

        if not encodings:
            print(f"[WARNING] No se detectaron caras en la imagen: {imagePath}")
            continue

        for encoding in encodings:
            save_encoding_to_db(id_persona, encoding)

    print("[INFO] Entrenamiento completado y datos guardados en PostgreSQL.")

if __name__ == "__main__":
    train_model()
