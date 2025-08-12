# Models like User & Blogs (One to many blog)
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from db import orm


class User(orm.Model):
    __tablename__ = 'users'

    id = Column("id",Integer, primary_key=True)
    name = Column("name",String(100), nullable=False)
    email = Column("email",String(100), unique=True, nullable=False)
    created_at = Column("created_at",DateTime, default=datetime.utcnow)
    updated_at = Column("updated_at",DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey('users.id'), nullable=False)  # <-- یہاں اصلاح کی گئی
    detail = Column("detail", String(255), nullable=False)
    created_at = Column("created_at", DateTime, default=datetime.utcnow)
    updated_at = Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
