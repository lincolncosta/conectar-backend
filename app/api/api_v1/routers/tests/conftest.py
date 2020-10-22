import pytest
from app.db import models 

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


def verify_password_mock(first: str, second: str) -> bool:
    return True
