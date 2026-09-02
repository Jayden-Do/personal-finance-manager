from app.security.password import hash_password, verify_password


def test_password_is_hashed():
    password = "dummypassword"
    hashed_password = hash_password(password)

    assert password != hashed_password


def test_verify_password_success():
    password = "dummypassword"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password)


def test_verify_password_failure():
    password = "dummypassword"
    hashed_password = hash_password(password)

    assert not verify_password("fake", hashed_password)


def test_same_password_generates_different_hashes():
    password = "dummypassword"

    hash_1 = hash_password(password)
    hash_2 = hash_password(password)

    assert hash_1 != hash_2
    assert verify_password(password, hash_1)
    assert verify_password(password, hash_2)
