from pydantic import BaseModel

class CharacterBase(BaseModel):
    name: str
    race: str
    profession: str
    equipment: str
    magic_item: str
    backstory: str
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

class CharacterCreate(CharacterBase):
    pass

class Character(CharacterBase):
    id: int

    class Config:
        orm_mode = True
