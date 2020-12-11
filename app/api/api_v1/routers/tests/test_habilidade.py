from db import models


def test_get_habilidade_by_name(client, test_habilidade, fake_login_superuser):
    response = client.get(f"/api/v1/habilidade/name/{test_habilidade.nome}")

    habilidade = response.json()
    t_habilidade = {"id": test_habilidade.id, "nome": test_habilidade.nome}

    assert response.status_code == 200
    assert habilidade == t_habilidade


def test_get_habilidades(client, test_habilidade, fake_login_superuser):
    response = client.get("/api/v1/habilidades/")

    assert response.status_code == 200
    assert response.json() == [
        {
            'nome': test_habilidade.nome,
            'id': test_habilidade.id
        }
    ]


def test_create_habilidade(client, fake_login_superuser):
    body = {
        'nome': 'Desenvolvimento Desktop'
    }
    response = client.post(
        "/api/v1/habilidade/pessoa",
        json=body
    )

    body["id"] = 3
    assert response.status_code == 200
    assert response.json() == body


def test_create_habilidade_fail(client, fake_login_superuser):
    """
        Tests if route accepts different json body arguments
    """
    response = client.post(
        "/api/v1/habilidade/pessoa",
        json={
            'descricao': 'Agronomia',
            'id': 1
        }
    )
    assert response.status_code == 422


def test_get_habilidades_not_found(client, fake_login_superuser):
    response = client.get(f"/api/v1/habilidade/name/aaasd")
    assert response.status_code == 404


def test_edit_habilidade(client, fake_login_superuser, test_habilidade):
    new_habilidade = {
        "nome": "OOP"
    }

    response = client.put(
        f"/api/v1/habilidades/pessoa/{test_habilidade.id}",
        json=new_habilidade
    )

    assert response.status_code == 200
    assert response.json() == {'id': test_habilidade.id, 'nome': 'OOP'}


def test_edit_habilidade_not_found(client, fake_login_superuser):
    new_habilidade = {
        "nome": "Geografia"
    }

    response = client.put(
        f"/api/v1/habilidades/pessoa/123123",
        json=new_habilidade
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Habilidade não encontrada'}


def test_delete_habilidade(client, fake_login_superuser, test_habilidade):
    response = client.delete(
        f"/api/v1/habilidade/pessoa/{test_habilidade.id}"
    )

    assert response.status_code == 200


def test_delete_habilidade_not_found(client, fake_login_superuser):
    response = client.delete(
        f"/api/v1/habilidade/pessoa/123"
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Habilidade não encontrada'}
