import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# Load .env
load_dotenv()
# Read database settings
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv("DB_DRIVER")
# Create ODBC connection string
connection_string = (
    f"DRIVER={{{DB_DRIVER}}};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_NAME};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)
# SQLAlchemy database URL
DATABASE_URL = (
    "mssql+pyodbc:///?odbc_connect="
    + quote_plus(connection_string)
)
# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)
Base = declarative_base()
# Create session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()