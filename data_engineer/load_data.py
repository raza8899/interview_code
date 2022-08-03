import json
from typing import Dict, List
import pandas as pd
from data_engineer.db_connect import db_session
from sqlalchemy import (
    Column,
    Table,
)
from sqlalchemy import MetaData

USERS_FILE = "data_engineer/users.json"
COURSES_FILE = "data_engineer/courses.json"
CERTIFICATES_FILE = "data_engineer/certificates.json"

# schema to create all tables
TABLE_CREATION_SCHEMA = """
CREATE TABLE IF NOT EXISTS public.users(
    id               UUID constraint users_pk primary key,
    email            VARCHAR NOT NULL,
    first_name        VARCHAR NOT NULL,
    last_name         VARCHAR NOT NULL     );

create index if not exists users_email_index
    on public.users (email);

CREATE TABLE IF NOT EXISTS public.courses(
    id               UUID constraint courses_pk primary key,
    title            VARCHAR NOT NULL,
    description        VARCHAR,
    published_at      timestamp with time zone NOT NULL );

CREATE TABLE IF NOT EXISTS public.certificates(
    id               serial constraint certificates_pk primary key,
    course_id               UUID NOT NULL constraint course_id_fk
            references public.courses (id)
            on update cascade on delete cascade,
    user_id            UUID NOT NULL constraint user_id_fk
            references public.users (id)
            on update cascade on delete cascade,
    completed_date        timestamp with time zone NOT NULL,
    start_date      timestamp with time zone NOT NULL );

create index if not exists certificate_course_id_index
    on public.certificates (course_id);
create index if not exists certificate_user_id_index
    on public.certificates (user_id);
"""



def read_json_file(file_path:str):
    """read json file and convert it to a pandas dataframe

    Args:
        file_path (str): 
    """
    with open(file_path,'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    return df

def insert_bulk_data(input_data:List[Dict], table_name:str, schema:str):
    """insert bulk data into a table

    Args:
        input_data (List[Dict]): input data is a list of dictionary, where each key is a column name in table
        table_name (str): 
        schema (str): 
    """
    try:
        assert input_data
        with db_session() as session:
            engine = session.get_bind()
            metadata_obj = MetaData()
            metadata_obj.reflect(bind=engine)
            table_obj = Table(table_name, metadata_obj, schema=schema, autoload_with= engine)
            insert_statement = table_obj.insert().values(input_data)
            session.execute(insert_statement)
            print(f"Data insertion for table {table_name} was successful, total rows inserted: {len(input_data)}")
    except AssertionError:
        print("No data to be inserted")
    except Exception as em:
        print(f"Error Occured {em}")

if __name__ == "__main__":
    with db_session() as session:
        session.execute(TABLE_CREATION_SCHEMA) # run the schema to create tables if tables doesn't exist

    # read data from files
    users_df = read_json_file(USERS_FILE)
    # use pandas to rename the dictionary keys, the dictionary keys are renamed to column name in table
    users_df = users_df.rename(index=str, columns={"firstName": "first_name", "lastName": "last_name"})
    users_data = users_df.to_dict('records')
    
    courses_df = read_json_file(COURSES_FILE)
    courses_df = courses_df.rename(index=str, columns={"publishedAt": "published_at"})
    courses_data = courses_df.to_dict('records')

    certificates_df = read_json_file(CERTIFICATES_FILE)
    certificates_df = certificates_df.rename(index=str, columns={"course": "course_id","user":"user_id",
    "completedDate":"completed_date","startDate":"start_date"})
    certificates_data = certificates_df.to_dict('records')
    
    
    insert_bulk_data(users_data, "users","public")
    insert_bulk_data(courses_data, "courses","public")
    insert_bulk_data(certificates_data, "certificates","public")






