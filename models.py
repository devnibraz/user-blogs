from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from db import orm


class User(orm.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    blogs = orm.relationship('Blog', backref='user', lazy=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        
        
class Blog(orm.Model):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False) 
    detail = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, user_id, detail):
        self.user_id = user_id
        self.detail = detail

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "detail": self.detail,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
