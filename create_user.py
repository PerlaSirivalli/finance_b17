from backend.db import SessionLocal, User

from backend.db import SessionLocal, User

def create_user(username: str, password: str):
    db = SessionLocal()
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        print(f"⚠ User '{username}' already exists")
        return
    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    db.close()
    print(f"✅ User '{username}' created!")

if _name_ == "_main_":
    create_user("student", "1234")
    create_user("employee", "5678")