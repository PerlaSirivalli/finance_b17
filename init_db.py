from backend.db import SessionLocal, User, init_db

def create_default_users():
    db = SessionLocal()
    try:
        default_users = [
            {"username": "student", "password": "1234"},
            {"username": "employee", "password": "5678"},
        ]
        for u in default_users:
            existing = db.query(User).filter(User.username == u["username"]).first()
            if not existing:
                user = User(username=u["username"], password=u["password"])
                db.add(user)
                db.commit()
                db.refresh(user)
                print(f"✅ Created default user: {u['username']}")
            else:
                print(f"ℹ User already exists: {u['username']}")
    finally:
        db.close()


if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("✅ Database initialized successfully!")

    print("Inserting default users...")
    create_default_users()
    print("✅ Default users added!")