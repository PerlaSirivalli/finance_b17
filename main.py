from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.db import Base, engine, SessionLocal, User, Expense
import uvicorn

# ----------------------------
# FastAPI App
# ----------------------------
app = FastAPI()

# Create DB tables
Base.metadata.create_all(bind=engine)

# DB Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------
# Pydantic Schemas
# ----------------------------
class UserLogin(BaseModel):
    username: str
    password: str

class ExpenseCreate(BaseModel):
    description: str
    amount: float
    user_id: int

class ExpenseOut(BaseModel):
    id: int
    description: str
    amount: float
    user_id: int

    class Config:
        orm_mode = True


# ----------------------------
# Login Route
# ----------------------------
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        User.username == user.username, User.password == user.password
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": "fake-jwt-token",
        "user_id": db_user.id,
        "username": db_user.username,
    }


# ----------------------------
# Expense Routes
# ----------------------------
@app.post("/expenses/", response_model=ExpenseOut)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = Expense(
        description=expense.description,
        amount=expense.amount,
        user_id=expense.user_id,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.get("/expenses/{user_id}", response_model=list[ExpenseOut])
def get_expenses(user_id: int, db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    return expenses


# ----------------------------
# Chatbot Route (IBM Granite Stub)
# ----------------------------
class ChatQuery(BaseModel):
    query: str

@app.post("/chat")
def chat(query: ChatQuery):
    # In real setup → connect to IBM Granite LLM API
    return {"answer": f"🤖 AI (Granite) response for: {query.query}"}


# ----------------------------
# Run Backend
# ----------------------------
if __name__ == "_main_":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)