from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, ARRAY, JSON
from sqlalchemy.orm import relationship
from ..db.database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Tools(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    popular = Column(Boolean, nullable=False, server_default=text("False"))
    newly_added = Column(Boolean, nullable=False, server_default=text("True"))
    total_likes = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone='True'), nullable=False, server_default=text('now()'))
    is_free = Column(Boolean)
    link = Column(String)

class Tutors(Base):
    __tablename__ = "tutors"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    popular = Column(Boolean, nullable=False, server_default=text("False"))
    newly_added = Column(Boolean, nullable=False, server_default=text("True"))
    total_likes = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone="True"), nullable=False, server_default=text('now()'))

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone="True"), nullable=False, server_default=text("now()"))
    # actions = relationship('useractions', back_populates='users')

class UserAction(Base):
    __tablename__ = "useractions"

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    saved_tools = Column(ARRAY(String), nullable=True)
    saved_tutors = Column(ARRAY(String), nullable=True)
    liked_tools = Column(ARRAY(String), nullable=True)
    liked_tutors = Column(ARRAY(String), nullable=True)
    opened_tools = Column(ARRAY(String), nullable=True)
    opened_tutors = Column(ARRAY(String), nullable=True)

class VoteTools(Base):
    __tablename__ = "votetools"

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tool_id = Column(Integer, ForeignKey("tools.id", ondelete="CASCADE"), nullable=False)


class VoteTutors(Base):
    __tablename__ = "votetutors"

    # id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    tutor_id = Column(Integer, ForeignKey("tutors.id", ondelete="CASCADE"), nullable=False, primary_key=True)
