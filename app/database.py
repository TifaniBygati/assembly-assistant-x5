from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = int(os.getenv('DB_PORT', '5433'))
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'localbase')
DB_NAME = os.getenv('DB_NAME', 'assembly_assistant_x5_dev')

engine = create_engine(f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

Fabric_session = sessionmaker(bind=engine)

def get_session():
    with Fabric_session() as session:
        yield session