import re

from sqlalchemy.orm import Session

from ..models.audio_model import Audio
from ..schemas.audio_schema import AudioUpdate


def create_audio(audio: Audio, db: Session):
    # If there is a same name, will add one number behind to differentiating
    if db.query(Audio).filter(Audio.file_name == audio.file_name).first():
        same_name_audios = (
            db.query(Audio)
            .filter(Audio.file_name.op("~")(rf"{audio.file_name} \(\d+\)"))
            .all()
        )
        max_cnt = 0
        digit_pattern = r"\((\d+)\)"
        for v in same_name_audios:
            max_cnt = max(max_cnt, int(re.search(digit_pattern, v.file_name).group(1)))
        audio.file_name += f" ({max_cnt+1})"
    db.add(audio)
    db.commit()
    db.refresh(audio)
    return audio


def read_audio(audio_id: str, db: Session):
    audio = db.query(Audio).filter(Audio.id == audio_id).first()
    return audio


def update_audio(audio_id: str, audio: AudioUpdate, db: Session):
    db_audio = db.query(Audio).filter(Audio.id == audio_id).first()
    if not db_audio:
        return None
    update_data = audio.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "file_name":
            if db.query(Audio).filter(Audio.file_name == value).first():
                same_name_audios = (
                    db.query(Audio)
                    .filter(Audio.file_name.op("~")(rf"{value} \(\d+\)"))
                    .all()
                )
                max_cnt = 0
                digit_pattern = r"\((\d+)\)"
                for v in same_name_audios:
                    max_cnt = max(
                        max_cnt,
                        int(re.search(digit_pattern, v.file_name).group(1)),
                    )
                value += f" ({max_cnt+1})"
        setattr(db_audio, key, value)
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    return db_audio


def delete_audio(audio_id: str, db: Session):
    db_audio = db.query(Audio).filter(Audio.id == audio_id).first()
    if not db_audio:
        return False
    db.delete(db_audio)
    db.commit()
    return True


def get_all_audios(db: Session):
    audios = db.query(Audio).filter(Audio.file_name.contains("")).all()
    return audios


def get_all_audios_by_user(user_id: str, db: Session):
    audios = db.query(Audio).filter(Audio.user_id == user_id).all()
    return audios
