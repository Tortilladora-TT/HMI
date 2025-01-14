import serial
import time
import logging

class SerialManager:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None

    def connect(self):
        """Conecta al puerto serial."""
        try:
            self.connection = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
            time.sleep(2)  # Espera para que el dispositivo inicialice
            logging.info(f"Conexión establecida con {self.port}")
        except Exception as e:
            logging.error(f"Error al conectar al puerto {self.port}: {e}")
            self.connection = None

    def send_command(self, command):
        """Envía un comando al dispositivo serial."""
        if self.connection and self.connection.is_open:
            try:
                self.connection.write(f"{command}\n".encode())
                logging.info(f"Comando enviado: {command}")
            except Exception as e:
                logging.error(f"Error al enviar comando: {e}")
        else:
            logging.warning("No hay conexión activa para enviar comandos.")

    def read_response(self):
        """Lee la respuesta del dispositivo serial."""
        if self.connection and self.connection.is_open:
            try:
                response = self.connection.readline().decode('utf-8').strip()
                logging.info(f"Respuesta recibida: {response}")
                return response
            except Exception as e:
                logging.error(f"Error al leer respuesta: {e}")
                return None
        else:
            logging.warning("No hay conexión activa para leer respuestas.")
            return None

    def disconnect(self):
        """Cierra la conexión serial."""
        if self.connection:
            self.connection.close()
            logging.info(f"Conexión cerrada con {self.port}")
