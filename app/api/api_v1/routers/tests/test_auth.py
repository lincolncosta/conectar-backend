from core.security import passwords

# Monkey patch function we can use to shave a second off our tests by skipping the password hashing check
def verify_password_mock(first: str, second: str):
    return True


def test_login(client, test_pessoa, monkeypatch):
    # Patch the test to skip password hashing check for speed
    monkeypatch.setattr(passwords, "verify_password", verify_password_mock)

    response = client.post(
        "/api/token",
        data={"username": test_pessoa.email, "password": "nottheactualpass", "email": "asd"},
    )
    assert "jid" in response.headers['set-cookie']
    assert response.status_code == 200


def test_signup(client, monkeypatch):
    def get_password_hash_mock(first: str, second: str):
        return True

    monkeypatch.setattr(passwords, "get_password_hash", get_password_hash_mock)

    response = client.post(
        "/api/signup",
        data={"username": "someusername", "password": "randompassword", "email": "somemail@email.com"},
    )
    assert "jid" in response.headers['set-cookie']
    assert response.status_code == 200


def test_resignup(client, test_pessoa, monkeypatch):
    # Patch the test to skip password hashing check for speed
    monkeypatch.setattr(passwords, "verify_password", verify_password_mock)

    response = client.post(
        "/api/signup",
        data={
            "username": test_pessoa.email,
            "password": "password_hashing_is_skipped_via_monkey_patch",
            "email": "email"
        },
    )
    assert response.status_code == 409


def test_wrong_password(client, test_db, test_pessoa, test_password, monkeypatch):
    def verify_password_failed_mock(first: str, second: str):
        return False

    monkeypatch.setattr(
        passwords, "verify_password", verify_password_failed_mock
    )

    response = client.post(
        "/api/token", data={"username": test_pessoa.email, "password": "wrong"}
    )
    assert response.status_code == 401


def test_wrong_login(client, test_db, test_pessoa, test_password):
    response = client.post(
        "/api/token", data={"username": "fakeuser", "password": test_password}
    )
    assert response.status_code == 401
