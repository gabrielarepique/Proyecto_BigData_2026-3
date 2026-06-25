import cv2
import numpy as np
from tensorflow.keras.models import load_model
import serial
import time
import os
import pandas as pd
from datetime import datetime

# ========================== CONFIGURACIÓN ==========================
PUERTO_SERIAL = 'COM3'
BAUD_RATE = 9600
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Une la ruta para apuntar a la carpeta ObjetoV2 donde se guardó el archivo
MODEL_PATH = os.path.join(BASE_DIR, 'ObjetoV2', 'modeloCNN.h5')
RUTA_MODELO = # Ruta base de tu proyecto + \modeloCNN.h5'
CLASES = #Agregar aquí las clases de tu modelo, por ejemplo: 'Botella', 'Lata', 'Ninguno'

UMBRAL_CONFIANZA = 0.95
TIEMPO_COOLDOWN = 2.0  

FRAME_WIDTH = 640
FRAME_HEIGHT = 480  
ROI_WIDTH = 300
ROI_HEIGHT = 300

ARCHIVO_EXCEL = "registro_envases.xlsx"

# ========================== FUNCIONES ==========================

def guardar_registro_excel(nombre_objeto):
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")
    nuevo = pd.DataFrame([[fecha, hora, nombre_objeto]], columns=["Fecha", "Hora", "Objeto"])

    if os.path.exists(ARCHIVO_EXCEL):
        df = pd.read_excel(ARCHIVO_EXCEL)
        df = pd.concat([df, nuevo], ignore_index=True)
    else:
        df = nuevo

    df.to_excel(ARCHIVO_EXCEL, index=False)
    print(f"📄 Registro guardado → {nombre_objeto}")


def enviar_senal_arduino(arduino, letra):
    """Envía una letra (A o B) al Arduino"""
    try:
        arduino.write(letra.encode())
        print(f"📤 Señal enviada → {letra}")
    except Exception as e:
        print(f"❌ Error enviando datos: {e}")


# ========================== INICIALIZACIÓN ==========================
try:
    model = load_model(RUTA_MODELO)
    print("✅ Modelo cargado correctamente")
except Exception as e:
    print(f"❌ Error cargando el modelo: {e}")
    exit()

try:
    arduino = serial.Serial(PUERTO_SERIAL, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"✅ Conexión serial establecida en {PUERTO_SERIAL}")
except:
    print("⚠ No se pudo conectar a Arduino")
    arduino = None

x1 = (FRAME_WIDTH - ROI_WIDTH) // 2
y1 = (FRAME_HEIGHT - ROI_HEIGHT) // 2
x2 = x1 + ROI_WIDTH
y2 = y1 + ROI_HEIGHT

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

if not cap.isOpened():
    print("❌ No se pudo abrir la cámara")
    exit()

print("📌 Sistema iniciado (ESC para salir)")

ultimo_envio = 0

# ========================== BUCLE PRINCIPAL ==========================

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    roi = frame[y1:y2, x1:x2]

    try:
        img = cv2.resize(roi, (224, 224))
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0)

        preds = model.predict(img, verbose=0)
        class_index = np.argmax(preds)
        confidence = preds[0][class_index]

        clase_detectada = CLASES[class_index]
    except:
        continue

    tiempo_actual = time.time()

    # ========================== LÓGICA DE DETECCIÓN ==========================

    if confidence >= UMBRAL_CONFIANZA and clase_detectada != 'Ninguno':
        # --- OBJETO DETECTADO ---
        text = f"{clase_detectada} ({confidence*100:.1f}%)"
        color = (0, 255, 0)

        if (tiempo_actual - ultimo_envio) > TIEMPO_COOLDOWN:
            ultimo_envio = tiempo_actual

            guardar_registro_excel(clase_detectada)

            if arduino:
                enviar_senal_arduino(arduino, 'A')  # <-- ENVÍA A CUANDO RECONOCE OBJETO

    else:
        # --- NO DETECTA OBJETO ---
        text = f"Ninguno ({confidence*100:.1f}%)"
        color = (0, 0, 255)

        if (tiempo_actual - ultimo_envio) > TIEMPO_COOLDOWN:
            ultimo_envio = tiempo_actual
            if arduino:
                enviar_senal_arduino(arduino, 'B')  # <-- ENVÍA B CUANDO NO RECONOCE

    # ========================== MOSTRAR INFO EN PANTALLA ==========================

    cv2.putText(frame, text, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    estado_serial = "Serial: OK" if arduino else "Serial: NO"
    cv2.putText(frame, estado_serial, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Reconocimiento de Objetos CNN", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()

print("✅ Sistema finalizado correctamente")
