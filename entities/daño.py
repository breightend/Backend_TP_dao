from estado import Estado
from tipoDaño import TipoDaño

class Daño:
  
  fecha: str
  gravedad: str
  estado: Estado
  tipoDaño: TipoDaño
  
  def __init__(self, fecha: str, gravedad: str, estado: Estado, tipoDaño: TipoDaño):
    self.fecha = fecha
    self.gravedad = gravedad
    self.estado = estado
    self.tipoDaño = tipoDaño
  
  
  def getFecha(self) -> str:
    return self.fecha
    
  def getGravedad(self) -> str:
    return self.gravedad
    
  def getEstado(self) -> Estado:
    return self.estado
    
  def getTipoDaño(self) -> TipoDaño:
    return self.tipoDaño
    
  