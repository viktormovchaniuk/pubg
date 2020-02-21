import bcrypt
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)

from .meta import Base


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    yt_link = Column(String(255))
    vk_link = Column(String(255))
    ds_link = Column(String(255))
    stream = Column(String(255))

    password_hash = Column(Text)

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password_hash = pwhash.decode('utf8')

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False
