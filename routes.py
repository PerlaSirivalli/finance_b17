# backend/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import SessionLocal, Expense, User
from pydantic import BaseModel
from typing import List

router = APIRouter()

# ------------------- DB Session -------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------- Schemas -------------------
class ExpenseCreate(BaseModel):
    description: str
    amount: float
    category: str

class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: float
    category: str
    date: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

# ------------------- Login -------------------
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        User.username == user.username, User.password == user.password
    ).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": f"fake-jwt-token-for-{user.username}",
        "token_type": "bearer",
        "user_id": db_user.id,
        "username": db_user.username
    }

# ------------------- Add Expense -------------------
@router.post("/expenses", response_model=ExpenseResponse)
def add_expense(expense: ExpenseCreate, user_id: int, db: Session = Depends(get_db)):
    db_expense = Expense(
        description=expense.description,
        amount=expense.amount,
        category=expense.category,
        user_id=user_id,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

# ------------------- Get Expenses -------------------
@router.get("/expenses", response_model=List[ExpenseResponse])
def get_expenses(user_id: int, db: Session = Depends(get_db)):
    return db.query(Expense).filter(Expense.user_id == user_id).all()