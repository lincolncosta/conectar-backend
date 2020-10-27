from db.habilidade.crud import get_habilidades_by_id, get_habilidade_by_name
from sqlalchemy.orm import Session
from fastapi import HTTPException

async def append_habilidades(update_data: dict, db: Session):
    ids = []
    names = []
    if "habilidades" in update_data:
        habilidades = update_data.get('habilidades')
        if habilidades:
            if habilidades[0].get('id'):
                ids = [habilidade['id'] for habilidade in habilidades]
            elif habilidades[0].get('nome'):
                names = [habilidade['nome'] for habilidade in habilidades]
            else:
                return
        else:
            return

        new_habilidades = []
        try:
            if ids:
                for habilidade_id in ids:
                    new_habilidades.append(get_habilidades_by_id(db, habilidade_id))
            else:
                for habilidade_name in names:
                    new_habilidades.append(get_habilidade_by_name(db, habilidade_name))

            update_data['habilidades'] = new_habilidades
        except HTTPException as e:
            if e.detail == "habilidade não encontrada":
                pass