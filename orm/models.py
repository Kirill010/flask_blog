from orm.db_session import ORMBase
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import orm

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


class User(ORMBase, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True)
    password_hash = Column(String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(ORMBase):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String)
    likes = Column(Integer, default=0)
    author_id = Column(Integer, ForeignKey('users.id'))

    author = orm.relation('User')
