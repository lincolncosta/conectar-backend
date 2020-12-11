from db.area.crud import get_area_by_id, get_area_by_name
from sqlalchemy.orm import Session
from fastapi import HTTPException

async def append_areas(update_data: dict, db: Session):
    ids = []
    descricoes = []

    if "areas" in update_data:
        areas = update_data.get('areas')
        if areas:
            if areas[0].get('id'):
                ids = [area['id'] for area in areas]
            elif areas[0].get('descricao'):
                descricoes = [area['descricao'] for area in areas]
            else:
                return
        else:
            return

        new_areas = []
        try:
            if ids:
                for area_id in ids:
                    new_areas.append(await get_area_by_id(db, area_id))
            else:
                for area_descricao in descricoes:
                    new_areas.append(await get_area_by_name(db, area_descricao))

            update_data['areas'] = new_areas
        except HTTPException as e:
            if e.detail == "area não encontrada":
                pass