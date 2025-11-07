
class TipoDaño:
  
  nommbre: str
  costoBase: float
  
  def __init__(self, nombre: str, costoBase: float):
    self.nombre = nombre
    self.costoBase = costoBase
    
  def getNombre(self) -> str:
    return self.nombre
    
  def getCostoBase(self) -> float:
    return self.costoBase
  