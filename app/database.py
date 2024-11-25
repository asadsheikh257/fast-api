from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 

# Potgresql database URL 
DATABASE_URL = "postgresql://postgres:multan990@localhost/fastapi"

engine = create_engine(DATABASE_URL)
SessionLocal =sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get the DB session 
def get_db():
    db = SessionLocal()
    try: 
        yield db
    except Exception as error:
        print(error)
    finally: 
        db.close()