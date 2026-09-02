from sqlmodel import Session

from app.db.database import engine
from app.repositories.user import UserRepository
from app.services.user import UserService


def main():
    with Session(engine) as session:
        repository = UserRepository(session)
        service = UserService(repository)

        user = service.register_user(
            username="service_user",
            email="service@example.com",
            password="dummy-password",
        )

        print("Created user:")
        print(user)


if __name__ == "__main__":
    main()
