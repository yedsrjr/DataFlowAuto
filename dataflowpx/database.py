from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from settings import Settings

engine = create_engine(Settings().PATH_DATABASE)

def get_session():
    return Session(engine)  

