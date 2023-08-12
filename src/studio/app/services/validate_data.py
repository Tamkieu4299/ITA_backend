from sqlalchemy.orm import Session
from ..crud.user_crud import read_user


# Currently we use dummy data, but later we will query in the database for validate user
def validate_user_id(id, db: Session):
    db_user = read_user(id, db)
    if db_user:
        return True
    return False
