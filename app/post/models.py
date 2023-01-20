import datetime

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Post(Base):
    uid = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('user.uid'))
    author = relationship('User', back_populates='posts')
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_update = Column(DateTime, onupdate=datetime.datetime.utcnow)

    def __init__(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content

    def __repr__(self):
        return f'<Post ({self.uid})>'
