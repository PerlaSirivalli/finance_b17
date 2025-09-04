from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Database URL (SQLite local file)
DATABASE_URL = "sqlite:///./finance.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ----------------------------
# User Model
# ----------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    expenses = relationship("Expense", back_populates="owner")


# ----------------------------
# Expense Model
# ----------------------------
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    amount = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="expenses")


# ----------------------------
# Initialize Database
# ----------------------------
def init_db():
    Base.metadata.create_all(bind=engine)