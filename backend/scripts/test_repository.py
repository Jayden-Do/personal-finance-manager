from sqlmodel import Session

from app.db.database import engine
from app.db.models.user import User
from app.repositories.user import UserRepository


def main():
    with Session(engine) as session:
        user_repository = UserRepository(session)

        example_user = User(
            username="josh",
            email="josh@example.com",
            password_hash="dummy-password-hash",
        )

        created_user = user_repository.create(example_user)

        print(created_user)

        user_by_id = user_repository.get_by_id(created_user.id)
        user_by_name = user_repository.get_by_username(created_user.username)
        user_by_email = user_repository.get_by_email(created_user.email)

        print(f"user get by id: {user_by_id}")
        print(f"user get by name: {user_by_name}")
        print(f"user get by email: {user_by_email}")


if __name__ == "__main__":
    main()
