# from app.db.projeto import schemas
# from app.db.pessoa import schemas

# from sqlalchemy.orm import Session
# from app.db import models

# async def search_project(
#     db: Session, searchTerm: str, skip: int = 0, limit: int = 100
#     ) -> t.List[schemas.Projeto]:

# '''
#     Function made for searching project by name, objective, areas and tools
#     used.
# '''

#     projs = []

#     if searchTerm in db.query(models.Projeto.nome).offset(skip).limit(limit)
#         projs.append(db.query(models.Projeto))

#     if searchTerm in db.query(models.Projeto.objetivo).offset(skip).limit(limit)
#         projs.append(db.query(models.Projeto))

#     if searchTerm in db.query(models.Projeto.areas.secondary.columns.__name__).offset(skip).limit(limit)
#         projs.append(db.query(models.Projeto))

#     if searchTerm in db.query(models.Projeto.habilidades.secondary.columns.__name__).offset(skip).limit(limit)
#         projs.append(db.query(models.Projeto))
    
#     return projs

# async def search_pessoa(
#     db: Session, searchTerm: str, skip: int = 0, limit: int = 100
#     ) -> t.List[schemas.Pessoa]:

#     pessoas = []

#     if searchTerm in db.query(models.Pessoa.nome).offset(skip).limit(limit)
#         projs.append(db.query(models.Pessoa))

#     if searchTerm in db.query(models.Pessoa.objetivo).offset(skip).limit(limit)
#         projs.append(db.query(models.Pessoa))

#     if searchTerm in db.query(models.Pessoa.areas.secondary.columns.__name__).offset(skip).limit(limit)
#         projs.append(db.query(models.Pessoa))

#     if searchTerm in db.query(models.Pessoa.habilidades.secondary.columns.__name__).offset(skip).limit(limit)
#         projs.append(db.query(models.Pessoa))
 
#     return pessoas
