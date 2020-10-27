from db import models
from core.security import passwords
from datetime import date

def test_get_pessoas(client, test_superuser, fake_login_superuser):
    response = client.get("/api/v1/pessoas")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": test_superuser.id,
            "email": test_superuser.email,
            "ativo": test_superuser.ativo,
            "colaborador": test_superuser.colaborador,
            "aliado": test_superuser.aliado,
            "data_nascimento": date(year=1990, month=1, day=1).isoformat(),
            "data_criacao": date.today().isoformat(),
            "areas": test_superuser.areas,
            "habilidades": test_superuser.habilidades,
            "idealizador": test_superuser.idealizador
        }
    ]


def test_delete_pessoa(client, test_db, fake_login_superuser):
    response = client.delete(
        f"/api/v1/pessoas"
    )
    assert response.status_code == 200
    assert test_db.query(models.Pessoa).all() == []


def test_delete_pessoa_not_found(client, fake_login_superuser):
    response = client.delete(
        "/api/v1/admin/pessoas/4321"
    )
    assert response.status_code == 404


def test_edit_pessoa(client, test_superuser, fake_login_superuser):
    new_pessoa = {
        "email": "newemail@email.com",
        "ativo": False,
        "nome": "Joe Smith",
    }

    response = client.put(
        f"/api/v1/admin/pessoas/{test_superuser.id}",
        json=new_pessoa,
    )
    assert response.status_code == 200
    new_pessoa["id"] = test_superuser.id
    new_pessoa["aliado"] = test_superuser.aliado
    new_pessoa["areas"] = test_superuser.areas
    new_pessoa["data_criacao"] = date.today().isoformat()
    new_pessoa["data_atualizacao"] = date.today().isoformat()
    new_pessoa["data_nascimento"] = date(year=1990, month=1, day=1).isoformat()
    new_pessoa["habilidades"] = test_superuser.habilidades
    new_pessoa["idealizador"] = test_superuser.idealizador
    new_pessoa["colaborador"] = test_superuser.colaborador


    assert response.json() == new_pessoa


def test_edit_pessoa_not_found(client, fake_login_superuser):
    new_pessoa = {
        "email": "newemail@email.com",
        "ativo": False,
        "senha": "new_password",
    }
    response = client.put(
        "/api/v1/admin/pessoas/1234", json=new_pessoa
    )
    assert response.status_code == 404


def test_get_pessoa(
    client, test_pessoa, fake_login_superuser
):
    response = client.get(
        f"/api/v1/pessoas/{test_pessoa.id}"
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_pessoa.id,
        "email": test_pessoa.email,
        "ativo": bool(test_pessoa.ativo),
        "colaborador": test_pessoa.colaborador,
        "aliado": test_pessoa.aliado,
        "data_nascimento": date(year=1990, month=1, day=1).isoformat(),
        "data_criacao": date.today().isoformat(),
        "areas": test_pessoa.areas,
        "habilidades": test_pessoa.habilidades,
        "idealizador": test_pessoa.idealizador
    }


def test_pessoa_not_found(client, fake_login_superuser):
    response = client.get("/api/v1/pessoas/123")
    assert response.status_code == 404


def test_authenticated_pessoa_me(client, fake_login_superuser):
    response = client.get("/api/v1/pessoas/me")
    assert response.status_code == 200


def test_unauthenticated_routes(client):
    response = client.get("/api/v1/pessoas/me")
    assert response.status_code == 403
    response = client.get("/api/v1/pessoas")
    assert response.status_code == 403
    response = client.get("/api/v1/pessoas/123")
    assert response.status_code == 403
    response = client.put("/api/v1/pessoas")
    assert response.status_code == 403
    response = client.delete("/api/v1/pessoas")
    assert response.status_code == 403
