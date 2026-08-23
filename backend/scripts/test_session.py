from sqlmodel import Session, select

from app.db.database import engine
from app.db.models.user import User


with Session(engine) as session:
    # 1. Create object
    user = User(
        username="jayden",
        email="jayden@example.com",
        password_hash="dummy-password-hash",
    )

    # 2. Add object to session
    session.add(user)

    # 3. Commit transaction
    session.commit()

    # 4. Refresh object from database
    session.refresh(user)

    print(f"Created user: {user}")

    # 5. Query user
    statement = select(User).where(User.username == "jayden")
    result = session.exec(statement)
    found_user = result.one()

    print(f"Found user: {found_user}")
