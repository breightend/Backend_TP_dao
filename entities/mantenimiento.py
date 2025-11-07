class Mantenimiento:
  
    fecha: str
    costo: float
  
    def __init__(self, fecha: str, costo: float):
        self.fecha = fecha
        self.costo = costo
        
    def getFecha(self):
        return self.fecha

    def setFecha(self, fecha: str):
        self.fecha = fecha

    def getCosto(self):
        return self.costo

    def setCosto(self, costo: float):
        self.costo = costo

    def __str__(self):
        return f"Fecha: {self.fecha}, Costo: {self.costo}"