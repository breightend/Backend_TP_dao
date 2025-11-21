from db.base import Base
from db.connection import DatabaseEngineSingleton

class Estado(Base):
  
  __tablename__ = "Estados"

  id = Column("id", Integer, primary_key=True)
  nombre = Column("nombre", String, nullable=False)
  ambito = Column("ambito", String, nullable=False)
  
  def __init__(self, nombre: str, ambito: str):
    self.nombre = nombre
    self.ambito = ambito
    
  
  def getNombre(self) -> str:
    return self.nombre
    
  def getAmbito(self) -> str:
    return self.ambito
  
  @classmethod
  def get_all_estados_de_ambito(cls, ambito: str):
    engine = DatabaseEngineSingleton().engine
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
      estados = session.query(Estado).filter(Estado.ambito == ambito).all()
      return estados
    except Exception as e:
      print(f"Error occurred while retrieving Estados: {e}")
      return []
    finally:
      session.close()

  @classmethod
  def get_estado_by_id(cls, id: int):
    engine = DatabaseEngineSingleton().engine
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
      estado = session.query(Estado).filter(Estado.id == id).first()
      return estado
    except Exception as e:
      print(f"Error occurred while retrieving Estado: {e}")
      return None
    finally:
      session.close()
  
  @classmethod
  def get_all_estados(cls):
    engine = DatabaseEngineSingleton().engine
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
      estados = session.query(Estado).all()
      return estados
    except Exception as e:
      print(f"Error occurred while retrieving Estados: {e}")
      return []
    finally:
      session.close()
    
  def to_dict(self):
    return {
      "id": self.id,
      "nombre": self.nombre,
      "ambito": self.ambito
    }
  