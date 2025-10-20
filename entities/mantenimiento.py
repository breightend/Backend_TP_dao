class Mantenimiento:
    def __init__(self, fecha: str, costo: float):
        self.fecha = fecha
        self.costo = costo

    def mostrar_informacion(self):
        return f"Fecha: {self.fecha}, Costo: {self.costo}"