# src/infrastructure/db/seed.py
from sqlalchemy.orm import Session

from src.infrastructure.db.models.user_model import UserModel
from src.infrastructure.db.session import SessionLocal
from src.infrastructure.security.password import hash_password


def seed_data() -> None:
    db: Session = SessionLocal()
    try:
        # Prevent duplicate seeding
        if db.query(UserModel).first():
            print("Database already seeded. Skipping.")
            return

        print("Seeding initial data...")
        admin = UserModel(
            email="admin@example.com",
            username="admin",
            hashed_password=hash_password("AdminSecurePassword123!"),
            is_active=True,
            is_admin=True,
        )
        test_user = UserModel(
            email="user@example.com",
            username="testuser",
            hashed_password=hash_password("UserSecurePassword123!"),
            is_active=True,
        )
        db.add_all([admin, test_user])
        db.commit()
        print("Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()