
from db.connection import DatabaseEngineSingleton
from db.base import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

class TipoDaño(Base):
  
  __tablename__ = "Tipo_de_daño"
  
  id = Column("id_daño", Integer, primary_key=True)
  nombre = Column("nombre", String(100), nullable=False)
  costoBase = Column("costo_base", Float, nullable=False)
  
  def __init__(self, nombre: str, costoBase: float):
    self.nombre = nombre
    self.costoBase = costoBase
    
  def getNombre(self) -> str:
    return self.nombre
    
  def getCostoBase(self) -> float:
    return self.costoBase
  

  def persist(self):
    engine = DatabaseEngineSingleton().engine
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(self)
    try:
      session.commit()
    except Exception as e:
      session.rollback()
      raise e
    finally:
      session.close()

  def to_dict(self):
    return {
      "id_tipo_daño": self.id,
      "nombre": self.nombre,
      "costoBase": self.costoBase
    }

  @classmethod
  def get_tipo_daño_by_id(cls, id: int):
    engine = DatabaseEngineSingleton().engine
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
      tipo_daño = session.query(TipoDaño).filter(TipoDaño.id == id).first()
      tipo_daño = tipo_daño.to_dict()
      return tipo_daño
    except Exception as e:
      print(f"Error occurred while retrieving Tipo de Daño: {e}")
      return None
    finally:
      session.close()
  
  @classmethod
  def get_all_tipo_daños(cls):
    engine = DatabaseEngineSingleton().engine
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
      tipo_daños = session.query(TipoDaño).all()
      tipo_daños = [tipo_daño.to_dict() for tipo_daño in tipo_daños]
      return tipo_daños
    except Exception as e:
      print(f"Error occurred while retrieving Tipo de Daños: {e}")
      return []
    finally:
      session.close()