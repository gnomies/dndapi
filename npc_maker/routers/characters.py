from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/characters/", response_model=list[schemas.Character])
def read_characters(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    characters = crud.get_characters(db, skip=skip, limit=limit)
    return characters

@router.get("/characters/{character_id}", response_model=schemas.Character)
def read_character(character_id: int, db: Session = Depends(get_db)):
    db_character = crud.get_character(db, character_id=character_id)
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return db_character

@router.post("/characters/", response_model=schemas.Character)
def create_character(character: schemas.CharacterCreate, db: Session = Depends(get_db)):
    return crud.create_character(db=db, character=character)

@router.post("/characters/generate", response_model=schemas.Character)
def generate_and_create_character(db: Session = Depends(get_db)):
    from ..npc_creator_anthropic import generate_character, generate_backstory
    character_data = generate_character()
    backstory = generate_backstory(character_data)
    character_data["backstory"] = backstory
    return crud.create_character(db=db, character=schemas.CharacterCreate(**character_data))
