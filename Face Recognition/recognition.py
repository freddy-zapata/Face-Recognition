import cv2
import face_recognition
import numpy as np
import psycopg2
import pickle
import base64
import threading
import requests
from picamera2 import Picamera2
from database import get_db_connection

def load_encodings_from_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id_persona, encoding FROM encodings;")
    rows = cur.fetchall()

    known_face_encodings = []
    known_face_ids = []

    for row in rows:
        id_persona = row[0]
        encoding = pickle.loads(row[1])
        known_face_encodings.append(encoding)
        known_face_ids.append(id_persona)

    cur.close()
    conn.close()
    return known_face_encodings, known_face_ids

def get_person_name(id_persona):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT nombre, apellido FROM personas WHERE id = %s;", (id_persona,))
    result = cur.fetchone()

    cur.close()
    conn.close()
    return result if result else ("Desconocido", "Desconocido")

def send_access_data(id_persona, foto_base64):
    data = {"id_persona": id_persona, "foto": foto_base64}
    try:
        response = requests.post("http://localhost:6001/accesos", json=data)
        print(f"[INFO] Respuesta API: {response.status_code} para id_persona={id_persona}")
    except Exception as e:
        print(f"[ERROR] Error enviando datos a la API: {e}")

def recognize_faces():
    known_face_encodings, known_face_ids = load_encodings_from_db()
    
    # Configurar PiCamera2
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
    picam2.configure(config)
    picam2.start()

    print("[INFO] Iniciando reconocimiento facial. Presiona 'q' para salir.")

    previously_detected = set()
    previously_detected_unknown = False  # Para controlar accesos de desconocidos

    try:
        while True:
            # Capturar frame desde PiCamera2
            frame = picam2.capture_array()
            
            # Convertir de RGB a BGR para OpenCV
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            rgb_frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame, model="hog")
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            face_names = []
            for encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, encoding)
                name, apellido = "Desconocido", "Desconocido"
                id_persona = None

                face_distances = face_recognition.face_distance(known_face_encodings, encoding)
                best_match_index = np.argmin(face_distances) if face_distances.size > 0 else None
                if best_match_index is not None and matches[best_match_index]:
                    id_persona = known_face_ids[best_match_index]
                    name, apellido = get_person_name(id_persona)

                face_names.append((name, apellido, id_persona))

            for i, ((top, right, bottom, left), (name, apellido, id_persona)) in enumerate(zip(face_locations, face_names)):
                # Margen para ampliar el recorte (en pixeles)
                margin = 30

                # Calculamos las nuevas coordenadas con margen, cuidando no salir del frame
                top_exp = max(top - margin, 0)
                right_exp = min(right + margin, frame_bgr.shape[1])
                bottom_exp = min(bottom + margin, frame_bgr.shape[0])
                left_exp = max(left - margin, 0)

                cv2.rectangle(frame_bgr, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(frame_bgr, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame_bgr, f"{name} {apellido}", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                # Recortar la cara con margen para enviar solo esa región ampliada
                face_image = frame_bgr[top_exp:bottom_exp, left_exp:right_exp]
                _, buffer = cv2.imencode(".jpg", face_image)
                foto_base64 = base64.b64encode(buffer).decode("utf-8")

                if id_persona and id_persona not in previously_detected:
                    threading.Thread(target=send_access_data, args=(id_persona, foto_base64)).start()
                    previously_detected.add(id_persona)
                elif id_persona is None and not previously_detected_unknown:
                    threading.Thread(target=send_access_data, args=(None, foto_base64)).start()
                    previously_detected_unknown = True

            # Si no hay caras detectadas, resetear el control de detecciones
            if len(face_locations) == 0:
                previously_detected.clear()
                previously_detected_unknown = False

            cv2.imshow('Reconocimiento Facial', frame_bgr)

            if cv2.waitKey(1) == ord("q"):
                break

    finally:
        picam2.stop()
        cv2.destroyAllWindows()
        print("[INFO] Reconocimiento finalizado.")

if __name__ == "__main__":
    recognize_faces()