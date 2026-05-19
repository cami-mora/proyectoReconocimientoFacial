# 🔐 Sistema de Seguridad Biométrica con OpenCV y ESP32

Este proyecto es un sistema de control de acceso basado en reconocimiento facial. Utiliza **Python** y **OpenCV** para el procesamiento de imágenes y la identificación de usuarios, trabajando en conjunto con un microcontrolador **ESP32** para el control del hardware físico (LEDs indicativos y un servomotor para la apertura de puertas).

## 🚀 Características Principales

* **Reconocimiento Facial en Tiempo Real:** Utiliza el algoritmo LBPH (Local Binary Patterns Histograms) para identificar rostros registrados.
* **Registro Dinámico:** Permite registrar nuevos usuarios directamente desde la interfaz de la cámara presionando una tecla.
* **Comunicación Bidireccional:** Comunicación Serial a 115200 baudios entre la computadora (Python) y el hardware (ESP32).
* **Control de Hardware (Lógica de Compuertas):**
    * **Acceso Concedido (Buffer / Compuerta YES):** Si el usuario es reconocido, la ESP32 recibe un `1`, encendiendo un LED Verde y activando el servomotor.
    * **Acceso Denegado (Inversor / Compuerta NOT):** Si el usuario es desconocido o no hay nadie, la ESP32 recibe un `0`, manteniendo la puerta cerrada y encendiendo un LED Rojo.

## 🛠️ Requisitos del Sistema

### Hardware Necesario
* Cámara web (integrada o por USB).
* Placa ESP32 (o equivalente compatible con Arduino IDE).
* 1x Servomotor (ej. SG90).
* 1x LED Verde (Acceso concedido).
* 1x LED Rojo (Acceso denegado).
* 1x Pulsador / Botón (Para solicitar el acceso).
* Resistencias y cables jumper.

### Software y Librerías
* **Python 3.x**
* **Arduino IDE** (para cargar el código a la ESP32)

Para instalar las dependencias de Python necesarias, ejecuta el siguiente comando en tu terminal:
```bash
pip install opencv-contrib-python pyserial numpy
