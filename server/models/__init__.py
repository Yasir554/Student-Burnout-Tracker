from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy

from .User import User


__all__= [
    "User"
]