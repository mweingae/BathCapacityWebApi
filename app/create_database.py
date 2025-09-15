import argparse
import models
from pathlib import Path
from sqlalchemy import text
from sqlmodel import SQLModel, Session, create_engine


def get_engine(db_path: str):
    sqlite_url = f"sqlite:///{db_path}"
    return create_engine(sqlite_url, echo=True)

def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)

def execute_sql(engine, scripts: list):
    session = Session(engine)

    for sql_script in scripts:
        with open(sql_script, encoding="utf-8") as sqlf:
            sql_statements = sqlf.readlines()
        
        for statement in sql_statements:
            if statement.strip():
                session._execute_internal(text(statement))
        
        session.commit()
    
def main():
    parser = argparse.ArgumentParser(description="Script to create and/or populate the database of the BathCapacityWebApi.")

    parser.add_argument('filepath', type=str, help='The path to the database (path is created if it does not exist).')
    parser.add_argument('--execute', nargs='*', help='A list of SQL scripts to execute')
    
    args = parser.parse_args()

    # Ensure directory exists
    db_path = Path(args.filepath)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    engine = get_engine(str(db_path))
    create_db_and_tables(engine)

    if args.execute:
        execute_sql(engine, args.execute)

if __name__ == "__main__":
    main()