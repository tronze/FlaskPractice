import datetime

from sqlalchemy import Column, Integer, String, DateTime, event
from werkzeug.security import generate_password_hash, check_password_hash

from app.database import Base


class User(Base):
    __tablename__ = 'user'
    uid = Column(Integer, primary_key=True)
    email = Column(String(128), unique=True)
    password = Column(String(128))
    name = Column(String(100))
    created_at = Column(DateTime(), default=datetime.datetime.utcnow)
    last_update = Column(DateTime(), onupdate=datetime.datetime.utcnow)

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f'<User ({self.name}, {self.email})>'

    def check_password(self, password):
        return check_password_hash(self.password, password)
