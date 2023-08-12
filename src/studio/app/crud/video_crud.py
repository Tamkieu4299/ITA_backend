import re

from sqlalchemy.orm import Session

from ..models.video_model import Video
from ..schemas.video_schema import VideoUpdate


def create_video(video: Video, db: Session):
    # If there is a same name, will add one number behind to differentiating
    if db.query(Video).filter(Video.file_name == video.file_name).first():
        same_name_videos = (
            db.query(Video)
            .filter(Video.file_name.op("~")(rf"{video.file_name} \(\d+\)"))
            .all()
        )
        max_cnt = 0
        digit_pattern = r"\((\d+)\)"
        for v in same_name_videos:
            max_cnt = max(max_cnt, int(re.search(digit_pattern, v.file_name).group(1)))
        video.file_name += f" ({max_cnt+1})"
    db.add(video)
    db.commit()
    db.refresh(video)
    return video


def read_video(video_id: str, db: Session):
    video = db.query(Video).filter(Video.id == video_id).first()
    return video


def update_video(video_id: str, video: VideoUpdate, db: Session):
    db_video = db.query(Video).filter(Video.id == video_id).first()
    if not db_video:
        return None
    update_data = video.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "file_name":
            if db.query(Video).filter(Video.file_name == value).first():
                same_name_videos = (
                    db.query(Video)
                    .filter(Video.file_name.op("~")(rf"{value} \(\d+\)"))
                    .all()
                )
                max_cnt = 0
                digit_pattern = r"\((\d+)\)"
                for v in same_name_videos:
                    max_cnt = max(
                        max_cnt,
                        int(re.search(digit_pattern, v.file_name).group(1)),
                    )
                value += f" ({max_cnt+1})"
        setattr(db_video, key, value)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def delete_video(video_id: str, db: Session):
    db_video = db.query(Video).filter(Video.id == video_id).first()
    if not db_video:
        return False
    db.delete(db_video)
    db.commit()
    return True


def get_all_videos(db: Session):
    videos = db.query(Video).filter(Video.file_name.contains("")).all()
    return videos


def get_all_videos_by_user(user_id: str, db: Session):
    videos = db.query(Video).filter(Video.user_id == user_id).all()
    return videos
