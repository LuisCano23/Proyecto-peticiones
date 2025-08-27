import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecreto")
    
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
    
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    