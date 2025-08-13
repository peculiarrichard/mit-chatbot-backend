from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base, engine

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    unique_identifier = Column(String, unique=True, index=True)
    is_existing_student = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    
    messages = relationship("Message", back_populates="user")

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=func.now())

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    is_bot = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="messages")

class QAEntry(Base):
    __tablename__ = "qa_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class UnansweredQuestion(Base):
    __tablename__ = "unanswered_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_answered = Column(Boolean, default=False)
    answer = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    answered_at = Column(DateTime, nullable=True)

# Create tables
Base.metadata.create_all(bind=engine)