from database import create_db_and_tables, get_session
import sys
from sqlalchemy import text

def execute_sql():
    session = (next(get_session()))

    for sql_script in sys.argv[1:]:
        with open(sql_script, encoding="utf-8") as sqlf:
            sql_statements = sqlf.readlines()
        
        for statment in sql_statements:
            session._execute_internal(text(statment))
        
        session.commit()
    
def main():
    create_db_and_tables()
    execute_sql()

if __name__ == "__main__":
    main()