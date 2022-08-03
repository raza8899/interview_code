import json
import os
from contextlib import contextmanager
from pydantic import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DbConnectSettings(BaseSettings):
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST_URL= "postgres"
    DB_NAME= "postgres"
    DATABASE_CONNECT_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST_URL}/{DB_NAME}"

def json_serializer(obj):
    return json.dumps(obj, default=str, ensure_ascii=False)


def create_db_engine(json_serializer, settings):
    engine = create_engine(
        settings.DATABASE_CONNECT_URL,
        json_serializer=json_serializer,
        json_deserializer=json.loads,
    )
    return engine


@contextmanager
def db_session():
    settings = DbConnectSettings()
    engine = create_db_engine(json_serializer, settings)
    session = sessionmaker(engine)
    with session.begin() as s:
        try:
            yield s
            s.commit()
            s.flush()
        except Exception as em:
            print(f"Error Occured: {em}")
            s.rollback()
        finally:
            s.close()