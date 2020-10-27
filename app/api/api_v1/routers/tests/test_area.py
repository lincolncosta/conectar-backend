from db import models


def test_get_area_by_id(client, test_area, fake_login_superuser):
    response = client.get(f"/api/v1/areas/id/{test_area.id}")

    area = response.json()
    t_area = {"id": test_area.id, "descricao": test_area.descricao}

    assert response.status_code == 200
    assert area == t_area


def test_get_area_by_name(client, test_area, fake_login_superuser):
    response = client.get(f"/api/v1/areas/name/{test_area.descricao}")

    area = response.json()
    t_area = {"id": test_area.id, "descricao": test_area.descricao}

    assert response.status_code == 200
    assert area == t_area


def test_get_area_with_parent(client, test_area_with_parent, fake_login_superuser):
    response = client.get(f"/api/v1/areas/id/{test_area_with_parent.id}")

    area = response.json()
    t_area = {
        "id": test_area_with_parent.id,
        "descricao": test_area_with_parent.descricao,
        "area_pai_id": test_area_with_parent.area_pai_id
    }

    assert response.status_code == 200
    assert t_area == area


def test_get_areas(client, test_area, test_area_with_parent, fake_login_superuser):
    response = client.get("/api/v1/areas")

    area = test_area_with_parent

    assert response.status_code == 200
    assert response.json() == [
        {
            'area': {
                'descricao': test_area.descricao,
                'id': test_area.id
            },
            'subareas': [{
                'descricao': area.descricao,
                'id': area.id,
                'area_pai_id': area.area_pai_id
            }]
        }
    ]


def test_create_area(client, fake_login_superuser):
    response = client.post(
        "/api/v1/areas",
        json={
            'descricao': 'Agronomia'
        }
    )
    assert response.status_code == 200
    assert response.json() == {'descricao': 'Agronomia', 'id': 7}


def test_create_area_with_parent(client, test_area, fake_login_superuser):
    response = client.post(
        "/api/v1/areas",
        json={
            'descricao': 'Topografia',
            'area_pai_id': test_area.id
        }
    )
    assert response.status_code == 200
    assert response.json() == {'descricao': 'Topografia',
                               'id': 9, 'area_pai_id': test_area.id}


def test_create_area_fail(client, fake_login_superuser):
    """
        Tests if route accepts different json body arguments
    """
    response = client.post(
        "/api/v1/areas",
        json={
            'nome': 'Agronomia',
            'id': 1
        }
    )
    assert response.status_code == 422


def test_create_area_with_parent_fail(client, fake_login_superuser):
    response = client.post(
        "/api/v1/areas",
        json={
            'descricao': 'Topografia',
            'area_pai_id': 123124
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'area pai não encontrada'}


def test_get_areas_not_found(client, fake_login_superuser):
    response = client.get(f"/api/v1/areas/name/aaasd")
    assert response.status_code == 404
    response = client.get(f"/api/v1/areas/id/123143")
    assert response.status_code == 404


def test_edit_area(client, fake_login_superuser, test_area):
    new_area = {
        "descricao": "Geografia"
    }

    response = client.put(
        f"/api/v1/areas/{test_area.id}",
        json=new_area
    )

    assert response.status_code == 200
    assert response.json() == {'descricao': 'Geografia'}


def test_edit_area_not_found(client, fake_login_superuser):
    new_area = {
        "descricao": "Geografia"
    }

    response = client.put(
        f"/api/v1/areas/123123",
        json=new_area
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'area não encontrada'}


def test_delete_area(client, fake_login_superuser, test_area):
    response = client.delete(
        f"/api/v1/areas/{test_area.id}"
    )

    assert response.status_code == 200


def test_delete_area_not_found(client, fake_login_superuser):
    response = client.delete(
        f"/api/v1/areas/12311"
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'area não encontrada'}
