from .session import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship


# class User(Base):
#     __tablename__ = "user"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     first_name = Column(String)
#     last_name = Column(String)
#     hashed_password = Column(String, nullable=False)
#     is_active = Column(Boolean, default=True)
#     is_superuser = Column(Boolean, default=False)

Participa = Table('participa', Base.metadata,
                  Column('idealizador_id', Integer,
                         ForeignKey('idealizador.id'), primary_key=True),
                  Column('colaborador_id', Integer,
                         ForeignKey('colaborador.id'), primary_key=True),
                  Column('aliado_id', Integer, ForeignKey('aliado.id'),
                         primary_key=True),
                  Column('projeto_id', Integer, ForeignKey('projeto.id'),
                         primary_key=True),
                  )

Contrato = Table('contrato', Base.metadata,
                 Column('pessoa_id', Integer, ForeignKey('pessoa.id'),
                        primary_key=True,),
                 Column('projeto_id', Integer, ForeignKey('projeto.id'),
                        primary_key=True),
                 Column('tipo', String),
                 Column('tempo', String),
                 )


class Pessoa(Base):
    __tablename__ = "pessoa"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nome = Column(String)
    password = Column(String, nullable=False)
    telefone = Column(String)
    username = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    contrato = relationship("Projeto", secondary=Contrato)


class Colaborador(Pessoa):
    __tablename__ = 'colaborador'

    id = Column(Integer, ForeignKey('pessoa.id'), primary_key=True)
    caracteristicas = Column(String)
    experiencia = Column(String)
    participa = relationship("Projeto", secondary=Participa)


class Aliado(Pessoa):
    __tablename__ = 'aliado'

    id = Column(Integer, ForeignKey('pessoa.id'), primary_key=True)
    caracteristicas = Column(String)
    experiencia = Column(String)


class Idealizador(Pessoa):
    __tablename__ = 'idealizador'

    id = Column(Integer, ForeignKey('pessoa.id'), primary_key=True)


class Projeto(Base):
    __tablename__ = 'projeto'

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    necessidades = Column(String, nullable=False)
    is_private = Column(Boolean, default=0, nullable=False)
    objetivo = Column(String)
    area = Column(String, nullable=False)
    descricao = Column(String)
    publico_alvo = Column(String)
    monetizacao = Column(String)
