from fastapi import FastAPI, Depends
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.api.api_v1.routers.pessoas import pessoas_router
from app.api.api_v1.routers.projeto import projeto_router
from app.api.api_v1.routers.experiencia.profissional import (
    experiencia_prof_router,
)
from app.api.api_v1.routers.experiencia.academica import experiencia_acad_router
from app.api.api_v1.routers.experiencia.projeto import experiencia_proj_router
from app.api.api_v1.routers.habilidade import habilidades_router
from app.api.api_v1.routers.area import area_router
from app.api.api_v1.routers.auth import auth_router
from app.core import config
from app.db.session import SessionLocal
from app.core.auth import get_current_active_pessoa


app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


# Routers
app.include_router(
    pessoas_router,
    prefix="/api/v1",
    tags=["pessoas"],
    dependencies=[Depends(get_current_active_pessoa)],
)

app.include_router(projeto_router, prefix="/api/v1",
    tags=["projeto"],)

app.include_router(
    experiencia_prof_router,
    prefix="/api/v1",
    tags=["experiencia profissional"],
    dependencies=[Depends(get_current_active_pessoa)],
)

app.include_router(
    experiencia_acad_router,
    prefix="/api/v1",
    tags=["experiencia academica"],
    dependencies=[Depends(get_current_active_pessoa)],
)

app.include_router(
    experiencia_proj_router,
    prefix="/api/v1",
    tags=["experiencia projeto"],
    dependencies=[Depends(get_current_active_pessoa)],
)

app.include_router(
    area_router,
    prefix="/api/v1",
    tags=["area"],
    dependencies=[Depends(get_current_active_pessoa)],
)

app.include_router(
    habilidades_router,
    prefix="/api/v1",
    tags=["habilidade"],
    dependencies=[Depends(get_current_active_pessoa)],
)

# @app.post("/api/v1/uploadfile/")
# async def create_upload_file(file: UploadFile = File(...)):
#     ''' Handles file upload, but files get overwritten

#     Have to create a hashing function to avoid naming colision
#     and save hash in the DB as image name
#     '''
#     try:
#         contents = await file.read()
#         path = store_image(contents, file.filename)
#         print(f"path from created image {path}")
#         return FileResponse(path)
#     except Exception as e:
#         print(e)

app.include_router(auth_router, prefix="/api", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
