# 🔐 Sistema de Seguridad Biométrica con OpenCV y ESP32

Este proyecto es un sistema de control de acceso basado en reconocimiento facial. Utiliza **Python** y **OpenCV** para el procesamiento de imágenes y la identificación de usuarios, trabajando en conjunto con un microcontrolador **ESP32** para el control del hardware físico (LEDs indicativos y un servomotor para la apertura de puertas).

## 🚀 Características Principales

* **Reconocimiento Facial en Tiempo Real:** Utiliza el algoritmo LBPH (Local Binary Patterns Histograms) para identificar rostros registrados.
* **Registro Dinámico:** Permite registrar nuevos usuarios directamente desde la interfaz de la cámara presionando una tecla.
* **Comunicación Bidireccional:** Comunicación Serial a 115200 baudios entre la computadora (Python) y el hardware (ESP32).
* **Control de Hardware (Lógica de Compuertas):**
    * **Acceso Concedido (Buffer / Compuerta YES):** Si el usuario es reconocido, la ESP32 recibe un `1`, encendiendo un LED Verde y activando el servomotor.
    * **Acceso Denegado (Inversor / Compuerta NOT):** Si el usuario es desconocido o no hay nadie, la ESP32 recibe un `0`, manteniendo la puerta cerrada y encendiendo un LED Rojo.
    * **Validación de Apertura (Multiplicador / Compuerta AND):** El sistema exige que ocurran dos eventos a la vez para evaluar el acceso: que se presione el botón (Entrada A) Y que el algoritmo detecte un rostro conocido (Entrada B). Ambas deben ser verdaderas (`1` y `1`) para proceder.

## 🛠️ Requisitos del Sistema

### Hardware Necesario
* Cámara web (del pc).
* Placa ESP32 (o equivalente compatible con Arduino IDE).
* 1x Servomotor (ej. SG90).
* 1x LED Verde (Acceso concedido).
* 1x LED Rojo (Acceso denegado).
* 1x Pulsador / Botón (Para solicitar el acceso).
* Resistencias y cables jumper.

### Software y Librerías

**Entorno de Python:**
* **Python 3.x:** Lenguaje principal para la lógica del servidor y visión artificial.
* **Librerías de Python requeridas:**
    * `opencv-contrib-python`: Para el procesamiento de imágenes, captura de video y el algoritmo de reconocimiento facial (LBPH). *Nota: Es crucial instalar la versión 'contrib' y no la normal para tener acceso a los módulos de biometría.*
    * `pyserial`: Permite la comunicación por puerto COM (Serial) entre Python y la ESP32.
    * `numpy`: Utilizado por OpenCV para el manejo estructurado de los píxeles y matrices de las imágenes.
    * *(Las librerías `os` y `time` vienen preinstaladas en Python).*

**Entorno de Arduino:**
* **Arduino IDE:** Para compilar y subir el código C++ a la placa.
* **Gestor de tarjetas ESP32:** Debes tener instalado el paquete de placas de Espressif en el Arduino IDE para que reconozca la ESP32.
* **Librería de Servomotor (Recomendado):** Si usas la librería estándar `Servo.h` y te da problemas, te recomiendo instalar la librería `ESP32Servo` desde el Gestor de Librerías del Arduino IDE, ya que está optimizada para el hardware de la ESP32.
