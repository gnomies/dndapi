from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    race = Column(String)
    profession = Column(String)
    equipment = Column(String)
    magic_item = Column(String)
    backstory = Column(Text)
    strength = Column(Integer)
    dexterity = Column(Integer)
    constitution = Column(Integer)
    intelligence = Column(Integer)
    wisdom = Column(Integer)
    charisma = Column(Integer)
