from .config import DATABASE_PATH
from sqlmodel import Session, create_engine


sqlite_file_path = DATABASE_PATH
sqlite_url = f"sqlite:///{sqlite_file_path}"

engine = create_engine(sqlite_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
