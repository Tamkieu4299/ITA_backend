import re

from sqlalchemy.orm import Session

from ..models.image_model import Image
from ..schemas.image_schema import ImageUpdate


def create_image(image: Image, db: Session):
    # If there is a same name, will add one number behind to differentiating
    if db.query(Image).filter(Image.file_name == image.file_name).first():
        same_name_images = (
            db.query(Image)
            .filter(Image.file_name.op("~")(rf"{image.file_name} \(\d+\)"))
            .all()
        )
        max_cnt = 0
        digit_pattern = r"\((\d+)\)"
        for v in same_name_images:
            max_cnt = max(max_cnt, int(re.search(digit_pattern, v.file_name).group(1)))
        image.file_name += f" ({max_cnt+1})"

    db.add(image)
    db.commit()
    db.refresh(image)
    return image


def read_image(image_id: str, db: Session):
    image = db.query(Image).filter(Image.id == image_id).first()
    return image


def update_image(image_id: str, image: ImageUpdate, db: Session):
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if not db_image:
        return None
    update_data = image.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "file_name":
            if db.query(Image).filter(Image.file_name == value).first():
                same_name_images = (
                    db.query(Image)
                    .filter(Image.file_name.op("~")(rf"{value} \(\d+\)"))
                    .all()
                )
                max_cnt = 0
                digit_pattern = r"\((\d+)\)"
                for v in same_name_images:
                    max_cnt = max(
                        max_cnt,
                        int(re.search(digit_pattern, v.file_name).group(1)),
                    )
                value += f" ({max_cnt+1})"
        setattr(db_image, key, value)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def delete_image(image_id: str, db: Session):
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if not db_image:
        return False
    db.delete(db_image)
    db.commit()
    return True


def get_all_images(db: Session):
    images = db.query(Image).filter(Image.file_name.contains("")).all()
    return images


def get_all_images_by_user(user_id: str, db: Session):
    images = db.query(Image).filter(Image.user_id == user_id).all()
    return images
