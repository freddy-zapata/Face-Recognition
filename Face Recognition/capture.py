import cv2
import os
import requests
import base64
from datetime import datetime
from picamera2 import Picamera2
import numpy as np

def create_folder(id_persona, nombre, apellido):
    dataset_folder = "dataset"
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)
    
    folder_name = f"{id_persona}_{nombre}_{apellido}".replace(" ", "_")
    person_folder = os.path.join(dataset_folder, folder_name)
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)
    return person_folder

def enviar_foto_api(id_persona, frame):
    _, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    url = f"http://localhost:6001/personas/{id_persona}/foto"
    data = {"foto": jpg_as_text}
    try:
        response = requests.put(url, json=data)
        if response.status_code == 200:
            print("[INFO] Foto subida con éxito a la API.")
        else:
            print(f"[ERROR] Error al subir la foto a la API. Código: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] No se pudo conectar con la API: {e}")

def capture_photos(id_persona, nombre, apellido):
    folder = create_folder(id_persona, nombre, apellido)
    
    # Configurar PiCamera2
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
    picam2.configure(config)
    picam2.start()

    print(f"Tomando fotos para {nombre} {apellido} (ID: {id_persona}). Presiona ESPACIO para capturar, 'q' para salir")

    photo_count = 0
    foto_subida = False

    try:
        while True:
            # Capturar frame desde PiCamera2
            frame = picam2.capture_array()
            
            # Convertir de RGB a BGR para OpenCV
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            cv2.imshow('Captura', frame_bgr)
            key = cv2.waitKey(1) & 0xFF

            if key == ord(' '):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{id_persona}_{nombre}_{apellido}_{timestamp}.jpg".replace(" ", "_")
                filepath = os.path.join(folder, filename)
                cv2.imwrite(filepath, frame_bgr)
                photo_count += 1
                print(f"Foto {photo_count} guardada: {filepath}")

                # Solo sube la primera foto que captures a la API
                if not foto_subida:
                    enviar_foto_api(id_persona, frame_bgr)
                    foto_subida = True

            elif key == ord('q'):
                break

    finally:
        picam2.stop()
        cv2.destroyAllWindows()
        print(f"Captura finalizada. {photo_count} fotos guardadas para {nombre} {apellido} (ID: {id_persona}).")

if __name__ == "__main__":
    import sys
    try:
        import requests
    except ImportError:
        print("Por favor instala la librería 'requests' con: pip install requests")
        sys.exit(1)

    id_persona = input("Ingresa el ID de la persona (número): ").strip()
    nombre = input("Ingresa el nombre de la persona: ").strip()
    apellido = input("Ingresa el apellido de la persona: ").strip()
    capture_photos(id_persona, nombre, apellido)