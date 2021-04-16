from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
import uvicorn


############################# Routers ###########################################
from app.api.api_v1.routers.pessoas import pessoas_router
from app.api.api_v1.routers.projeto import projeto_router
from app.api.api_v1.routers.experiencia.profissional import (
    experiencia_prof_router,
)
from app.api.api_v1.routers.experiencia.academica import experiencia_acad_router
from app.api.api_v1.routers.experiencia.projeto import experiencia_proj_router
from app.api.api_v1.routers.habilidade import habilidades_router
from app.api.api_v1.routers.papel import papel_router
from app.api.api_v1.routers.pesquisa.projeto import pesquisa_projeto_router
from app.api.api_v1.routers.pesquisa.pessoa import pesquisa_pessoa_router
from app.api.api_v1.routers.area import area_router
from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.pessoa_projeto import pessoa_projeto_router
from app.api.api_v1.routers.papel import papel_router
from app.api.api_v1.routers.tipo_acordo import tipo_acordo_router
from app.api.api_v1.routers.experiencia.academica import experiencia_acad_router
from app.api.api_v1.routers.experiencia.projeto import experiencia_proj_router
from app.api.api_v1.routers.habilidade import habilidades_router
from app.api.api_v1.routers.area import area_router
from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.pesquisa.pessoa import pesquisa_pessoa_router
from app.api.api_v1.routers.pesquisa.projeto import pesquisa_projeto_router
from app.api.api_v1.routers.pessoa_projeto import pessoa_projeto_router
from app.api.api_v1.routers.reacoes import reacoes_router
from app.api.api_v1.routers.notificacao import notificacao_router
############################# Routers ###########################################

# from app.core import config
# from app.db.session import SessionLocal
# from app.core.auth import get_current_active_pessoa
from core import config
from db.session import SessionLocal
from core.auth import get_current_active_pessoa

import os

DEV_ENV = os.getenv("DEV_ENV")
app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)

app.mount("/api/uploads", StaticFiles(directory="uploads"), name="uploads")

# Go to localhost:8000/api/coverage/index.html to see coverage report
# app.mount("/api/coverage", StaticFiles(directory="htmlcov"), name="htmlcov")

# Use HTTPS in production
if not DEV_ENV:
    app.add_middleware(HTTPSRedirectMiddleware)
    origins = [
        "https://conectar-frontend.vercel.app",
        "conectar-frontend.vercel.app",
        "https://boraconectar.com",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["Content-Type", "Accept", "authorization"],
    )


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
    tags=["pessoas"]
)

app.include_router(
    projeto_router,
    prefix="/api/v1",
    tags=["projeto"],
)

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

app.include_router(
    papel_router,
    prefix="/api/v1",
    tags=["papel"],
    dependencies=[Depends(get_current_active_pessoa)],
)

app.include_router(
    pesquisa_projeto_router,
    prefix="/api/v1",
    tags=["pesquisa_projeto"],
)

app.include_router(
    pesquisa_pessoa_router,
    prefix="/api/v1",
    tags=["pesquisa_pessoa"],
)

app.include_router(
    pessoa_projeto_router,
    prefix="/api/v1",
    tags=["pessoa_projeto"],
)

app.include_router(
    notificacao_router,
    prefix="/api/v1",
    tags=["notificacao"],
)

app.include_router(
    tipo_acordo_router,
    prefix="/api/v1",
    tags=["tipo_acordo"],
)

app.include_router(
    reacoes_router,
    prefix="/api/v1",
    tags=["reacoes"]
)

app.include_router(auth_router, prefix="/api", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)