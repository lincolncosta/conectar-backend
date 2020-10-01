from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from db import models
from . import schemas
from app.core.security.passwords import get_password_hash


def get_area(db: Session, area_id: int) -> schemas.Area:
    area = (
        db.query(models.Area).filter(models.Area.id == area_id).first()
    )
    if not area:
        raise HTTPException(status_code=404, detail="area não encontrada")
    return area


def get_areas(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.Area]:
    return db.query(models.Area).offset(skip).limit(limit).all()


def create_area(db: Session, area: schemas.AreaCreate) -> schemas.Area:
    try:
        db_area = models.Area(
          descricao=area.descricao,
          area_pai_id=area.area_pai_id
        )
    except Exception as e:
        print(e)
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area


def delete_area(db: Session, area_id: int):
    area = get_area(db, area_id)
    if not area:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="area não encontrada"
        )
    db.delete(area)
    db.commit()
    return area


def edit_area(
    db: Session, area_id: int, area: schemas.AreaEdit
) -> schemas.Area:
    """
    Edits area on database.

    Tries to find the area in the database, if it finds, updates each field
    that was send with new information to the database.

    Args:
        db: Database Local Session. sqlalchemy.orm.sessionmaker instance.
        area_id: Integer representing the area id. Integer.
        area: New data to use on update of area. Schema from AreaEdit.

    Returns:
        A dict of area with the updated values. For example, the adition 
        of an area_pai_id:
        another_area: {
          id: 1,
          descricao: "Matemática"
        }
        old_area: {
            id: 2,
            descricao: "Algebra"
        }
        new_area: {
            id: 2,
            descricao: "Algebra"
            area_pai_id: 1
        }

    Raises:
        HTTPException: No person corresponds to area_id in the database.
    """
    db_area = get_area(db, area_id)
    if not db_area:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="area não encontrada"
        )
    update_data = area.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_area, key, value)

    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area
