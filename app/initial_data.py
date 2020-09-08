#!/usr/bin/env python3

# from app.db.session import get_db
from app.db.pessoa.crud import create_pessoa
from app.db.pessoa.schemas import PessoaCreate
from app.db.session import SessionLocal


def init() -> None:
    db = SessionLocal()

    create_pessoa(
        db,
        PessoaCreate(
            email="email@email.com",
            senha="admin",
            usuario="admin",
            ativo=True,
            superusuario=True,
        ),
    )


if __name__ == "__main__":
    print("Creating superuser email@email.com")
    init()
    print("Superuser created")
