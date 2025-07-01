from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .User import User
from .TokenBlocklist import TokenBlocklist
from .Evaluation import Evaluation

__all__ = [
    "db",
    "User",
    "TokenBlocklist",
    "Evaluation"
]
