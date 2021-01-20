    projeto = models.Projeto(
import pytest
from db import models 

@pytest.fixture
def test_area(test_db) -> models.Area:
    """
    Area for testing
    """

    area = models.Area(
        descricao="Ciência da computação"
    )
    test_db.add(area)
    test_db.commit()
    return area




@pytest.fixture
def test_area_with_parent(test_db, test_area) -> models.Area:
    """
    Area with a parent for testing
    """
    area = models.Area(
        descricao="Algoritmos",
        area_pai_id=test_area.id
    )
    test_db.add(area)
    test_db.commit()
    return area


@pytest.fixture
def test_habilidade(test_db) -> models.Habilidades:
    """
    Habilidade for testing
    """

    habilidade = models.Habilidades(
        nome="Desenvolvimento web"
    )
    test_db.add(habilidade)
    test_db.commit()
    return habilidade


@pytest.fixture
def test_projeto(test_db) -> models.Projeto:
    """
    Habilidade for testing
    """

    projeto = models.Projeto(
        nome="Conectar",
        descricao="Vamos conectar",
        objetivo="Conectar pessoas"
    )
    test_db.add(projeto)
    test_db.commit()
    return projeto