from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user import User


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user):
        existing_user = self.get_by_username(user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        existing_email = self.get_by_email(user.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already exists")

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_by_username(self, username):
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email):
        return self.db.query(User).filter(User.email == email).first()

    def list_users(self):
        return self.db.query(User).all()