from db import models


def test_get_projeto_by_id(client, test_projeto, fake_login_superuser):
    response = client.get(f"/api/v1/projeto/{test_projeto.id}")

    projeto = response.json()
    t_projeto = {
      "id": test_projeto.id,
      "nome": test_projeto.nome,
      "descricao": test_projeto.descricao, 
      "objetivo": test_projeto.objetivo,
      "visibilidade": test_projeto.visibilidade,
      "areas": [],
      "habilidades": []
    }

    assert response.status_code == 200
    assert projeto == t_projeto


def test_get_projetos(client, test_projeto, fake_login_superuser):
    response = client.get("/api/v1/projetos")

    assert response.json() == [
        {
            "nome": "Conectar",
            "descricao": "Vamos conectar",
            "visibilidade": True,
            "objetivo": "Conectar pessoas",
            "areas": [],
            "habilidades": [],
            "id": test_projeto.id
        }
    ]

def test_create_projeto(client, fake_login_superuser):
    response = client.post(
        "/api/v1/projeto",
        data={
            "nome":"Criação de gado",
            "descricao":"Criação de gado na capital",
            "objetivo":"Criar gado",
            "visibilidade": True
        }
    )
    projeto_id = response.json()["id"]
    assert response.status_code == 200
    assert response.json() == {"id": projeto_id}


def test_create_projeto_fail(client, fake_login_superuser):
    """
        Tests if route accepts missing data arguments
    """
    response = client.post(
        "/api/v1/projeto",
        data={
            'nome': 'Agronomia',
            'descricao': "Falta objetivo"
        }
    )
    assert response.status_code == 422


def test_get_projetos_not_found(client, fake_login_superuser):
    response = client.get(f"/api/v1/projeto/123143")
    assert response.status_code == 404


def test_edit_projeto(client, fake_login_superuser, test_projeto):
    new_area = {
        "descricao": "Nova descrição"
    }

    response = client.put(
        f"/api/v1/projeto/{test_projeto.id}",
        json=new_area
    )

    assert response.status_code == 200
    assert response.json() == {
            "nome": "Conectar",
            "descricao": "Nova descrição",
            "visibilidade": True,
            "objetivo": "Conectar pessoas",
            "areas": [],
            "habilidades": [],
            "id": test_projeto.id
        }


def test_edit_projeto_not_found(client, fake_login_superuser):
    new_area = {
        "descricao": "Nova descrição"
    }

    response = client.put(
        f"/api/v1/projeto/123123",
        json=new_area
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'projeto não encontrado'}


def test_delete_projeto(client, fake_login_superuser, test_projeto):
    response = client.delete(
        f"/api/v1/projeto/{test_projeto.id}"
    )

    assert response.status_code == 200


def test_delete_projeto_not_found(client, fake_login_superuser):
    response = client.delete(
        f"/api/v1/projeto/12311"
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'projeto não encontrado'}
