from app.db import models


def test_get_pessoas(client, test_superuser, superuser_token_headers):
    response = client.get("/api/v1/pessoas", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": test_superuser.id,
            "email": test_superuser.email,
            "is_active": test_superuser.is_active,
            "is_superuser": test_superuser.is_superuser,
        }
    ]


def test_delete_pessoa(client, test_superuser, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/pessoas/{test_superuser.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(models.User).all() == []


def test_delete_pessoa_not_found(client, superuser_token_headers):
    response = client.delete(
        "/api/v1/pessoas/4321", headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_edit_pessoa(client, test_superuser, superuser_token_headers):
    new_pessoa = {
        "email": "newemail@email.com",
        "ativo": False,
        "superusuario": True,
        "nome": "Joe Smith",
        "senha": "new_password",
    }

    response = client.put(
        f"/api/v1/pessoas/{test_superuser.id}",
        json=new_pessoa,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    new_pessoa["id"] = test_superuser.id
    new_pessoa.pop("senha")
    assert response.json() == new_pessoa


def test_edit_pessoa_not_found(client, test_db, superuser_token_headers):
    new_pessoa = {
        "email": "newemail@email.com",
        "ativo": False,
        "superusuario": False,
        "senha": "new_password",
    }
    response = client.put(
        "/api/v1/pessoas/1234", json=new_pessoa, headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_get_pessoa(
    client, test_pessoa, superuser_token_headers,
):
    response = client.get(
        f"/api/v1/pessoas/{test_pessoa.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_pessoa.id,
        "email": test_pessoa.email,
        "ativo": bool(test_pessoa.ativo),
        "superusuario": test_pessoa.superusuario,
    }


def test_pessoa_not_found(client, superuser_token_headers):
    response = client.get("/api/v1/pessoas/123", headers=superuser_token_headers)
    assert response.status_code == 404


def test_authenticated_pessoa_me(client, pessoa_token_headers):
    response = client.get("/api/v1/pessoas/me", headers=pessoa_token_headers)
    assert response.status_code == 200


def test_unauthenticated_routes(client):
    response = client.get("/api/v1/pessoas/me")
    assert response.status_code == 401
    response = client.get("/api/v1/pessoas")
    assert response.status_code == 401
    response = client.get("/api/v1/pessoas/123")
    assert response.status_code == 401
    response = client.put("/api/v1/pessoas/123")
    assert response.status_code == 401
    response = client.delete("/api/v1/pessoas/123")
    assert response.status_code == 401


def test_unauthorized_routes(client, pessoa_token_headers):
    response = client.get("/api/v1/pessoas", headers=pessoa_token_headers)
    assert response.status_code == 403
    response = client.get("/api/v1/pessoas/123", headers=pessoa_token_headers)
    assert response.status_code == 403
