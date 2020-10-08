from app.db.habilidade.crud import get_habilidades_by_id
from sqlalchemy.orm import Session
from fastapi import HTTPException

async def append_habilidades(update_data: dict, db: Session):
    if "habilidades" in update_data:
        habilidades = update_data.get('habilidades')
        # if db_pessoa.habilidades:
        #     for area in db_pessoa.habilidades:
        #         habilidades.append({"id": area.id})
        ids = [area['id'] for area in habilidades]
        new_habilidades = []
        try:
            for area_id in ids:
                new_habilidades.append(await get_habilidades_by_id(db, area_id))  
            update_data['habilidades'] = new_habilidades
        except HTTPException as e:
            if e.detail == "habilidade não encontrada":
                pass