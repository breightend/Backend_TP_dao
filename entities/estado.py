
class Estado:
  
  nombre: str
  ambito: str
  
  def __init__(self, nombre: str, ambito: str):
    self.nombre = nombre
    self.ambito = ambito
    
  
  def getNombre(self) -> str:
    return self.nombre
    
  def getAmbito(self) -> str:
    return self.ambito
    
  