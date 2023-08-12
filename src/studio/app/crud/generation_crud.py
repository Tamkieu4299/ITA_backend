from typing import Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session

from ..models.generation_model import Generation


async def create_generation(generation: Generation, db: Session, generation_data: dict):
    db_generation = db.query(Generation).filter(Generation.id == generation.id).first()
    if not db_generation:
        db.add(generation)
        db.commit()
        db.refresh(generation)
        return generation

    for key, value in generation_data.items():
        if not value:
            continue
        setattr(db_generation, key, value)
    db.add(db_generation)
    db.commit()
    db.refresh(db_generation)
    return db_generation


async def read_generation(generation_id: str, db: Session):
    generation = db.query(Generation).filter(Generation.id == generation_id).first()
    return generation


async def update_generation(generation: dict, db: Session):
    db_generation = (
        db.query(Generation).filter(Generation.id == generation["id"]).first()
    )
    if not db_generation:
        return None
    update_data = generation
    for key, value in update_data.items():
        if not value:
            continue
        setattr(db_generation, key, value)
    db.add(db_generation)
    db.commit()
    db.refresh(db_generation)
    return db_generation


async def update_type_generation(generation: dict, db: Session):
    db_generation = (
        db.query(Generation).filter(Generation.id == generation["id"]).first()
    )
    if not db_generation:
        return None
    update_data = generation
    if update_data["type"] == "base":
        base_avatar = await check_video_type_exist(db_generation.user_id, "base", db)
        if base_avatar:
            setattr(base_avatar[0], "type", "generated")
            db.add(base_avatar[0])
            db.commit()
            db.refresh(base_avatar[0])
    for key, value in update_data.items():
        if not value:
            continue
        setattr(db_generation, key, value)
    db.add(db_generation)
    db.commit()
    db.refresh(db_generation)
    return db_generation


async def delete_generation(generation_id: str, db: Session):
    db_generation = db.query(Generation).filter(Generation.id == generation_id).first()
    if not db_generation:
        return False
    db.delete(db_generation)
    db.commit()
    return True


async def get_all_generations(db: Session):
    generations = db.query(Generation).all()
    return generations


async def get_all_base_generations(db: Session):
    generations = db.query(Generation).filter(Generation.type == "base").all()
    return generations


async def get_all_generations_by_user(user_id: str, db: Session, type: Optional[str] = None):
    generations = db.query(Generation).filter(Generation.user_id == user_id, Generation.type == type if type is not None else True).all()
    return generations


async def check_video_type_exist(user_id: str, type: str, db: Session):
    generations = (
        db.query(Generation)
        .filter(and_(Generation.user_id == user_id, Generation.type == type))
        .all()
    )
    return generations
