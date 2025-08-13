from typing import List
from fastapi import APIRouter, Depends
from fastapi import HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from src.database import get_db
from src.entities import User, Message, QAEntry, UnansweredQuestion, Admin
from src.models import UserCreate, MessageCreate, AdminCreate, QAEntryCreate, AdminLogin, AnswerQuestion, MessageResponse, UnansweredQuestionResponse
import uuid
from src.bot_service import openrouter_service
from src.admin_service import hash_password, verify_password, verify_token, create_access_token, send_email_notification
from sqlalchemy.sql import func
import logging

logger = logging.getLogger(__name__)

app_router = APIRouter(prefix="/api", tags=["api"])



app_router.post("/auth/student")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        logger.error(f"Username {user.username} has been taken, please choose another one")
        raise HTTPException(status_code=400, detail=f"Username {user.username} has been taken, please choose another one")
    
    unique_id = str(uuid.uuid4())
    
    db_user = User(
        username=user.username,
        unique_identifier=unique_id,
        is_existing_student=user.is_existing_student
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"data": db_user, "message": "User created successfully"}

app_router.post("/message/")
async def send_message(
    message: MessageCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.unique_identifier == message.user_identifier).first()
    if not user:
        logger.error("User not found")
        raise HTTPException(status_code=404, detail="User not found")
    
    user_message = Message(
        user_id=user.id,
        content=message.content,
        is_bot=False
    )
    db.add(user_message)
    db.commit()
    
    messages = db.query(Message).filter(Message.user_id == user.id).order_by(Message.created_at).all()
    conversation_history = [
        {"role": "user" if not msg.is_bot else "assistant", "content": msg.content}
        for msg in messages[-10:]
    ]
    
    qa_entries = db.query(QAEntry).all()
    qa_data = [{"question": qa.question, "answer": qa.answer} for qa in qa_entries]
    
    bot_response = await openrouter_service.generate_response(conversation_history, qa_data)
    
    if "I don't know the answer to that question yet" in bot_response:
        logger.info(f"New unanswered question: {message.content}")
        unanswered = UnansweredQuestion(
            question=message.content,
            user_id=user.id
        )
        db.add(unanswered)
        db.commit()
        
        background_tasks.add_task(
            send_email_notification,
            "New Unanswered Question",
            f"A student asked: {message.content}\n\nPlease log into the admin dashboard to provide an answer."
        )
        logger.info("Unanswered question sent to admin")
    
    bot_message = Message(
        user_id=user.id,
        content=bot_response,
        is_bot=True
    )
    db.add(bot_message)
    db.commit()
    
    return {"response": bot_response}

app_router.get("/messages/{user_identifier}")
async def get_messages(user_identifier: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_identifier or User.unique_identifier == user_identifier).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    messages = db.query(Message).filter(Message.user_id == user.id).order_by(Message.created_at).all()
    data = [
        MessageResponse(
            id=msg.id,
            content=msg.content,
            is_bot=msg.is_bot,
            created_at=msg.created_at
        )
        for msg in messages
    ]
    return {"data": data, "message": "Messages fetched successfully"}

app_router.post("/auth/admin/register")
async def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    existing_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin already exists")
    
    hashed_password = hash_password(admin.password)
    db_admin = Admin(email=admin.email, password_hash=hashed_password)
    db.add(db_admin)
    db.commit()
    
    return {"message": "Admin registered successfully"}

@app_router.post("/auth/admin/login")
async def login_admin(admin: AdminLogin, db: Session = Depends(get_db)):
    db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if not db_admin or not verify_password(admin.password, db_admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": admin.email, "type": "admin"})
    data ={
        admin: db_admin,
        token: token,
        "token_type": "bearer"
    }
    return {"data": data, "message": "Admin sign in successful"}


app_router.get("/admin/unanswered-questions")
async def get_unanswered_questions(
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    questions = db.query(UnansweredQuestion).filter(
        UnansweredQuestion.is_answered == False
    ).order_by(UnansweredQuestion.created_at.desc()).all()
    
    unanswererd_questions = [
        UnansweredQuestionResponse(
            id=q.id,
            question=q.question,
            user_id=q.user_id,
            created_at=q.created_at,
            is_answered=q.is_answered
        )
        for q in questions
    ]
    return {"data": unanswererd_questions, "message": "Unanswered questions fetched successfully"}


app_router.post("/admin/answer-question/{question_id}")
async def answer_question(
    question_id: int,
    answer_data: AnswerQuestion,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    question = db.query(UnansweredQuestion).filter(UnansweredQuestion.id == question_id).first()
    if not question:
        logger.error(f"Question with {question_id} not found")
        raise HTTPException(status_code=404, detail="Question not found")
    
    question.answer = answer_data.answer
    question.is_answered = True
    question.answered_at = func.now()
    
    qa_entry = QAEntry(
        question=question.question,
        answer=answer_data.answer
    )
    db.add(qa_entry)
    db.commit()
    
    return {"data": question, "message": "Question answered successfully"}


app_router.get("/admin/qa-entries")
async def get_qa_entries(
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    entries = db.query(QAEntry).order_by(QAEntry.created_at.desc()).all()
    return {"data": entries, "message": "QA entries fetched successfully"}


app_router.get("/admin/unanswered-questions/{question_id}")
async def get_unanswered_question(
    question_id: int,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    question = db.query(UnansweredQuestion).filter(UnansweredQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    return {"data": question, "message": "Unanswered question fetched successfully"}


app_router.post("/admin/qa-entries")
async def create_qa_entries(qa_entries: List[QAEntryCreate], token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    for entry in qa_entries:
        qa_entry = QAEntry(question=entry.question, answer=entry.answer)
        db.add(qa_entry)
    db.commit()
    return {"data": qa_entries, "message": "QA entries created successfully"}