from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt6.QtCore import Qt
import sys
import json

# Clases Persona, Comprador, Organizador, Evento, EventoParrillada, EventoVIP (las mismas definidas anteriormente)...
class Persona:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

class Comprador(Persona):
    def __init__(self, nombre, email, dni):
        super().__init__(nombre, email)
        self.dni = dni

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'email': self.email,
            'dni': self.dni
        }

class Organizador(Persona):
    def __init__(self, nombre, email, ruc):
        super().__init__(nombre, email)
        self.ruc = ruc

class Evento:
    def __init__(self, nombre_evento, descripcion, lugar, hora):
        self.nombre_evento = nombre_evento
        self.descripcion = descripcion
        self.lugar = lugar
        self.hora = hora

    def mostrar_detalle(self):
        raise NotImplementedError("Implementar en clases secundarias")

class EventoParrillada(Evento):
    def __init__(self, nombre_evento, descripcion, lugar, hora):
        super().__init__(nombre_evento, descripcion, lugar, hora)

    def mostrar_detalle(self):
        detalle = f'Nombre: {self.nombre_evento}\nDescripción: {self.descripcion}\nLugar: {self.lugar}\nHora: {self.hora}'
        return detalle

class EventoVIP(Evento):
    def __init__(self, nombre_evento, descripcion, lugar, hora):
        super().__init__(nombre_evento, descripcion, lugar, hora)


    def mostrar_detalle(self):
        detalle = f"Nombre: {self.nombre_evento}\nDescripción: {self.descripcion}\nLugar: {self.lugar}\nHora: {self.hora}"
        return detalle
# Clase Ventas (modificada para guardar solo los datos necesarios del comprador)
class Ventas:
    def __init__(self, comprador, evento, cantidad_tickets):
        self.comprador_info = comprador.to_dict()  # Solo guardar los datos relevantes del comprador
        self.evento = evento
        self.cantidad_tickets = cantidad_tickets

    def calcular_total(self):
        if isinstance(self.evento, EventoVIP):
            # Calcular descuento para eventos VIP
            total = self.cantidad_tickets * 100  # Supongamos que cada ticket cuesta $100
            descuento = total * 0.1  # Descuento del 10%
            total_con_descuento = total - descuento
            return total_con_descuento
        else:
            return self.cantidad_tickets * 100  # Precio estándar para otros eventos

# Clase GestorDeVentas (con método para mostrar información de ventas)
class GestorDeVentas:
    def __init__(self):
        self.ventas = []

    def agregar_venta(self, venta):
        self.ventas.append(venta)

    def total_ventas(self):
        total = 0
        for venta in self.ventas:
            total += venta.calcular_total()
        return total

    def ventas_info(self):
        info = ""
        for venta in self.ventas:
            info += f"Comprador: {venta.comprador_info['nombre']} - Evento: {venta.evento.nombre_evento} - Tickets: {venta.cantidad_tickets}\n"
        return info

    def guardar_ventas(self, archivo):
        ventas_serializables = []
        for venta in self.ventas:
            venta_dict = {
                'comprador': venta.comprador_info,
                'evento': venta.evento.nombre_evento,
                'cantidad_tickets': venta.cantidad_tickets
            }
            ventas_serializables.append(venta_dict)

        with open(archivo, 'w') as file:
            json.dump(ventas_serializables, file, indent=4)

# Clase VentanaEvento (actualizada para mostrar información de ventas)
class VentanaEvento(QMainWindow):
    def __init__(self, evento_parrillada, evento_vip, gestor_ventas):
        super().__init__()
        self.setWindowTitle("Detalles de Eventos y Ventas")
        self.setGeometry(100, 100, 800, 600)

        layout = QGridLayout()

        label_parrillada = QLabel("Evento Parrillada")
        label_parrillada.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_vip = QLabel("Evento VIP")
        label_vip.setAlignment(Qt.AlignmentFlag.AlignCenter)

        detalle_parrillada = QLabel(evento_parrillada.mostrar_detalle())
        detalle_vip = QLabel(evento_vip.mostrar_detalle())

        label_ventas = QLabel("Información de Ventas")
        label_ventas.setAlignment(Qt.AlignmentFlag.AlignCenter)

        detalle_ventas = QLabel(gestor_ventas.ventas_info())
        detalle_ventas.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(label_parrillada, 0, 0)
        layout.addWidget(label_vip, 0, 1)
        layout.addWidget(detalle_parrillada, 1, 0)
        layout.addWidget(detalle_vip, 1, 1)
        layout.addWidget(label_ventas, 2, 0, 1, 2)
        layout.addWidget(detalle_ventas, 3, 0, 1, 2)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    evento_parrillada = EventoParrillada("Fiesta Parrillada", "Disfruta de una deliciosa parrillada.", "Parque Central", "18:00")
    evento_vip = EventoVIP("Evento VIP", "Exclusivo para miembros VIP.", "Hotel de Lujo", "20:00")
    comprador1 = Comprador("Juan Perez", "juan@gmail.com", "1234567890")

    venta1 = Ventas(comprador1, evento_parrillada, 2)
    venta2 = Ventas(comprador1, evento_vip, 3)

    gestor_ventas = GestorDeVentas()
    gestor_ventas.agregar_venta(venta1)
    gestor_ventas.agregar_venta(venta2)

    ventana_evento = VentanaEvento(evento_parrillada, evento_vip, gestor_ventas)
    ventana_evento.show()

    sys.exit(app.exec())
