import os

class Config:
    SECRET_KEY = "SUPERSECRETKEY"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///shoestore.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False