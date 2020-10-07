from app.db.area.crud import get_area_by_id
from sqlalchemy.orm import Session
from fastapi import HTTPException

async def append_areas(update_data: dict, db: Session):
    if "areas" in update_data:
        areas = update_data.get('areas')
        # if db_pessoa.areas:
        #     for area in db_pessoa.areas:
        #         areas.append({"id": area.id})
        ids = [area['id'] for area in areas]
        new_areas = []
        try:
            for area_id in ids:
                new_areas.append(await get_area_by_id(db, area_id))  
            update_data['areas'] = new_areas
        except HTTPException as e:
            if e.detail == "area não encontrada":
                pass