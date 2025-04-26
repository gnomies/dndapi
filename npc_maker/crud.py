from sqlalchemy.orm import Session
from . import models, schemas

def get_characters(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Character).offset(skip).limit(limit).all()

def get_character(db: Session, character_id: int):
    return db.query(models.Character).filter(models.Character.id == character_id).first()

def create_character(db: Session, character: schemas.CharacterCreate):
    db_character = models.Character(**character.dict())
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character