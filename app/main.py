from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
import uvicorn

from api.api_v1.routers.pessoas import pessoas_router
from api.api_v1.routers.projeto import projeto_router
from api.api_v1.routers.experiencia.profissional import (
    experiencia_prof_router,
)
from api.api_v1.routers.experiencia.academica import experiencia_acad_router
from api.api_v1.routers.experiencia.projeto import experiencia_proj_router
from api.api_v1.routers.habilidade import habilidades_router
from api.api_v1.routers.area import area_router
from api.api_v1.routers.auth import auth_router
from core import config
from db.session import SessionLocal
from core.auth import get_current_active_pessoa


app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)

app.mount("/api/uploads", StaticFiles(directory="uploads"), name="uploads")

# Go to localhost:8000/api/coverage/index.html to see coverage report
# app.mount("/api/coverage", StaticFiles(directory="htmlcov"), name="htmlcov")

# Use HTTPS in production
app.add_middleware(HTTPSRedirectMiddleware)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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

app.include_router(auth_router, prefix="/api", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
