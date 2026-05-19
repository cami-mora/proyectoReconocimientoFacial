import cv2 # Librería para procesamiento de imágenes y video
import os  # Para gestión de archivos y rutas del sistema
import numpy as np # Para manejo de matrices y arreglos numéricos
import serial # Librería para comunicación con hardware (ESP32)
import time # Para manejar pausas y tiempos de espera

# --- 1. CONFIGURACIÓN DE HARDWARE (ESP32) ---
# Cambia 'COM3' por el puerto que veas en el Arduino IDE
puerto_esp32 = 'COM7' 
try:
    # Iniciamos la conexión a 115200 baudios (velocidad de datos)
    esp32 = serial.Serial(puerto_esp32, 115200, timeout=1)
    time.sleep(2) # Espera de cortesía para que la ESP32 reinicie la conexión
    print(f"Conexión exitosa con la ESP32 en {puerto_esp32}")
except:
    esp32 = None # Si no hay nada conectado, el programa sigue sin errores
    print("ESP32 no detectada. Iniciando en modo simulación (solo pantalla).")

# --- 2. CONFIGURACIÓN DE VISIÓN Y RUTAS ---
ruta_db = "db_rostros" # Carpeta de base de datos
nombre_ventana = 'SISTEMA DE SEGURIDAD BIOMÉTRICA' # Título de la ventana

# Cargamos el detector de rostros frontal de OpenCV (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Creamos la carpeta de base de datos si no existe
if not os.path.exists(ruta_db):
    os.makedirs(ruta_db)

# Inicializamos el reconocedor LBPH (Local Binary Patterns Histograms)
# Este algoritmo analiza la textura de la piel en áreas pequeñas
reconocedor = cv2.face.LBPHFaceRecognizer_create()

# --- 3. FUNCIÓN DE ENTRENAMIENTO DEL MODELO ---
def entrenar_sistema():
    rostros, ids, nombres = [], [], {}
    
    # Verificamos si hay fotos para entrenar
    if not os.path.exists(ruta_db) or not os.listdir(ruta_db):
        return None, {}

    # Leemos cada imagen guardada en la carpeta
    for i, archivo in enumerate(os.listdir(ruta_db)):
        if archivo.lower().endswith((".jpg", ".png", ".jpeg")):
            nombre_usuario = os.path.splitext(archivo)[0]
            # Leemos la imagen en escala de grises (esencial para LBPH)
            img = cv2.imread(os.path.join(ruta_db, archivo), 0)
            
            # Redimensionamos a un tamaño estándar para que el algoritmo no falle
            rostros.append(cv2.resize(img, (200, 200)))
            ids.append(i) # ID numérico para el entrenamiento
            nombres[i] = nombre_usuario # Relación ID -> Nombre Real
            
    # El modelo "estudia" las características de los rostros y sus IDs
    reconocedor.train(rostros, np.array(ids))
    return reconocedor, nombres

# Entrenamos el sistema justo al iniciar el programa
modelo, diccionario_nombres = entrenar_sistema()

# Iniciamos la captura de la Webcam
cap = cv2.VideoCapture(0)

# Configuramos la ventana para que sea REDIMENSIONABLE
cv2.namedWindow(nombre_ventana, cv2.WINDOW_NORMAL) 

# VARIABLES PARA CONTROL DE PANTALLA POST-BOTÓN
nombre_info = ""
color_info = (255, 0, 0)
mostrar_hasta = 0 # Tiempo en segundos hasta el cual se muestra la info

print("--- SISTEMA DE ACCESO ACTIVO ---")
print("Presiona 'R' para registrar, 'Q' para salir.")
print("--- SISTEMA EN ESPERA DE BOTÓN ---")

# --- 4. BUCLE DE PROCESAMIENTO EN TIEMPO REAL ---
while True:
    ret, frame = cap.read()
    if not ret: break
    
    # IMPORTANTE: Capturamos la tecla al inicio para que la variable 'key' siempre exista
    key = cv2.waitKey(1) & 0xFF
    
    # Convertimos el cuadro a gris para detección y reconocimiento
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    # Revisamos si la ESP32 envió algo (el botón fue presionado)
    if esp32 and esp32.in_waiting > 0:
        linea = esp32.readline().decode('utf-8').strip()
        
        if linea == "SOLICITUD":
            print("Procesando reconocimiento por petición de hardware...")
            
            if len(faces) > 0:
                # Tomamos solo el primer rostro detectado para la decisión
                (x, y, w, h) = faces[0]
                rostro_recortado = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
                
                if modelo is not None:
                    id_usuario, confianza = modelo.predict(rostro_recortado)
                    
                    if confianza < 60:
                        print(f"Acceso Concedido a: {diccionario_nombres[id_usuario]}")
                        nombre_info = diccionario_nombres[id_usuario]
                        color_info = (0, 255, 0) # Verde
                        esp32.write(b'1') # Orden de encender VERDE/AZUL
                    else:
                        print("Acceso Denegado: Usuario Negado")
                        nombre_info = "NEGADA"
                        color_info = (0, 0, 255) # Rojo
                        esp32.write(b'0') # Orden de encender ROJO
                
                # Guardamos el tiempo actual + 5 segundos para mantener la info en pantalla
                mostrar_hasta = time.time() + 5
            else:
                print("No se detectó ningún rostro frente a la cámara")
                esp32.write(b'0') # Si no hay nadie, cuenta como no reconocido

    # Dibujamos la información en pantalla
    for (x, y, w, h) in faces:
        # Si estamos dentro del tiempo de los 5 segundos después del botón:
        if time.time() < mostrar_hasta:
            cv2.rectangle(frame, (x, y), (x+w, y+h), color_info, 2)
            cv2.putText(frame, nombre_info, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_info, 2)
        else:
            # Si no se ha presionado el botón o ya pasó el tiempo, cuadro azul informativo
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, "Esperando Boton...", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow(nombre_ventana, frame)
    
    # Lógica para registrar un rostro nuevo (Tecla R)
    if key == ord('r') and len(faces) > 0:
        (x, y, w, h) = faces[0]
        nuevo_nombre = input("Ingrese el nombre del usuario: ")
        if nuevo_nombre:
            # Guardamos la captura en la carpeta de rostros
            cv2.imwrite(f"{ruta_db}/{nuevo_nombre}.jpg", gray[y:y+h, x:x+w])
            # Re-entrenamos el modelo para incluir al nuevo usuario
            modelo, diccionario_nombres = entrenar_sistema()
            print(f"Usuario {nuevo_nombre} registrado correctamente.")
            
    elif key == ord('q'): # Salir del programa (Tecla Q)
        break

# --- 5. CIERRE DE RECURSOS ---
cap.release() # Soltamos la cámara
if esp32: esp32.close() # Cerramos el puerto de la ESP32
cv2.destroyAllWindows() # Cerramos las ventanas de video