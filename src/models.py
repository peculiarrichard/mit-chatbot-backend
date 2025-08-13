from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta

class UserCreate(BaseModel):
    username: str
    is_existing_student: bool

class MessageCreate(BaseModel):
    content: str
    user_identifier: str

class MessageResponse(BaseModel):
    id: int
    content: str
    is_bot: bool
    created_at: datetime

class AdminCreate(BaseModel):
    email: EmailStr
    password: str

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class UnansweredQuestionResponse(BaseModel):
    id: int
    question: str
    user_id: int
    created_at: datetime
    is_answered: bool

class AnswerQuestion(BaseModel):
    answer: str

class QAEntryCreate(BaseModel):
    question: str
    answer: str