from .session import Base
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    DateTime,
    Date,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from datetime import date

# Tables created from M*N relationships

PessoaProjeto = Table(
    "tb_pessoa_projeto",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("pessoa_id", Integer, ForeignKey("tb_pessoa.id")),
    Column("area_id", Integer, ForeignKey("tb_area.id")),
    Column("papel_id", Integer, ForeignKey("tb_papel.id")),
    Column("projeto_id", Integer, ForeignKey("tb_projeto.id")),
    Column("tipo_acordo_id", Integer, ForeignKey("tb_tipo_acordo.id")),

)

ExperienciaArea = Table(
    "tb_experiencia_area",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("area_id", ForeignKey("tb_area.id"), primary_key=True),
    Column("experiencia_id", ForeignKey("tb_experiencia.id"), primary_key=True),
)

PessoaArea = Table(
    "tb_pessoa_area",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("pessoa_id", ForeignKey("tb_pessoa.id"), primary_key=True),
    Column("area_id", ForeignKey("tb_area.id"), primary_key=True),
)

ProjetoArea = Table(
    "tb_projeto_area",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("projeto_id", ForeignKey("tb_projeto.id"), primary_key=True),
    Column("area_id", ForeignKey("tb_area.id"), primary_key=True),
)

AreaPessoaProjeto = Table(
    "tb_area_pessoa_projeto",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("area_id", ForeignKey("tb_area.id"), primary_key=True),
    Column(
        "pessoa_projeto_id",
        ForeignKey("tb_pessoa_projeto.id"),
        primary_key=True,
    ),
)


class Pessoa(Base):
    """
        Represents table "tb_pessoa"


        1. Recursive One to One relationship - colaborador
        One Pessoa can only be one colaborador

        2. Recursive One to One relationship - idealizador
        One Pessoa can only be one idealizador

        3. Recursive One to One relationship - aliado
        One Pessoa can only be one aliado


        Attributes:
            id: Integer, Primary key
            usuario: String
            senha: String
            nome: String
            data_criacao: Datetime - default uses DB function Now()
            on the server
            data_nascimento: Date
            telefone: String
            ativo: Boolean
            superusuario: Boolean
            colaborador_id: Integer, Foreign Key
            colaborador_rel: Relationship
            idealizador_id: Integer, Foreign Key
            idealizador_rel: Relationship
            aliado_id: Integer, Foreign Key
            aliado_rel: Relationship

    """

    __tablename__ = "tb_pessoa"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String, unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    nome = Column(String)
    # data_criacao uses server time with timezone and not user time by default
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_nascimento = Column(Date, default=date(year=1990, month=1, day=1))
    telefone = Column(String)
    ativo = Column(Boolean, default=True)
    superusuario = Column(Boolean, default=False)

    experiencia = relationship("Experiencia")
    projeto_pessoa = relationship("Projeto", secondary=PessoaProjeto)
    areas = relationship("Area", secondary=PessoaArea)

    # Recursive relationships

    colaborador_id = Column(Integer, ForeignKey("tb_pessoa.id", ondelete='cascade'))
    colaborador = relationship("Pessoa", uselist=False, foreign_keys=[colaborador_id])

    idealizador_id = Column(Integer, ForeignKey("tb_pessoa.id", ondelete='cascade'))
    idealizador = relationship("Pessoa", uselist=False, foreign_keys=[idealizador_id])

    aliado_id = Column(Integer, ForeignKey("tb_pessoa.id", ondelete='cascade'))
    aliado = relationship("Pessoa", foreign_keys=[aliado_id], uselist=False)

    # colaborador = Column(Integer, ForeignKey("tb_pessoa.id", ondelete='cascade'), nullable=True)
    # colaborador_rel = relationship(
    #     "Pessoa", backref=backref("colaborador", remote_side=[id], uselist=False)
    # )

    # idealizador = Column(Integer, ForeignKey("tb_pessoa.id", ondelete='cascade'), nullable=True)
    # idealizador_rel = relationship(
    #     "Pessoa", backref=backref("idealizador", remote_side=[id], uselist=False)
    # )

    # aliado = Column(Integer, ForeignKey("tb_pessoa.id", ondelete='cascade'), nullable=True)
    # aliado_rel = relationship(
    #     "Pessoa", backref=backref("aliado", remote_side=[id], uselist=False)
    # )


class Projeto(Base):
    """
        Represents table "tb_projeto"


        Attributes:
            id: Integer, Primary key
            descricao: String
            visibilidade: Boolean
    """

    __tablename__ = "tb_projeto"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    descricao = Column(String)
    visibilidade = Column(Boolean, default=True)
    # publico_alvo = Column(String, nullable=True)
    # monetizacao = Column(String, nullable=True)


class Experiencia(Base):
    """
        Represents table "tb_experiencia"


        1. Many to Many relationship - Area
        Many experiencias may be in may Areas
        Many Areas may have many experiences

        2. One to Many relationship - Pessoa
        One Pessoa can have many Experience
        One experience can only have one Pessoa


        Attributes:
            id: Integer, Primary key
            descricao: String
            organizacao: String - Organization name the person worked
            data_inicio: Date
            data_fim: Date
            pessoa_id: Integer, Foreign Key
            areas: Relationship
    """

    __tablename__ = "tb_experiencia"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    organizacao = Column(String)
    data_inicio = Column(Date)
    data_fim = Column(Date, nullable=True)
    pessoa_id = Column(Integer, ForeignKey("tb_pessoa.id"))
    areas = relationship("Area", secondary=ExperienciaArea)


class Area(Base):
    """
        Represents table "tb_area"


        Recursive Many To Many Relationship
        One Area can have many subareas,
        And subarea can have many

        Attributes:
            id: Integer, Primary key
            descricao: String
            area_pai_id: Integer, Foreign Key
            area_pai_rel: Relationship
    """

    __tablename__ = "tb_area"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)

    area_pai_id = Column(Integer, ForeignKey("tb_area.id"))
    area_pai_rel = relationship(
        "Area", backref=backref("area_pai", remote_side=[id])
    )


class Papel(Base):
    """
        Represents table "tb_papel"


        Many to One relationship
        One pessoa_projeto has one Papel, meanwhile
        One Papel may be in may PessoaProjeto


        Attributes:
            id: Integer, Primary key
            descricao: String
            pessoa_projeto_id: Integer, Foreign Key
            pessoa_projeto_rel: Relationship
    """

    __tablename__ = "tb_papel"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    # pessoa_projeto_id = Column(Integer, ForeignKey("tb_pessoa_projeto.id"))
    # pessoa_projeto_rel = relationship("PessoaProjeto")


class TipoAcordo(Base):
    """
        Represents table "tb_tipo_acordo"


        Many to One relationship
        One pessoa_projeto has one TipoAcordo, meanwhile
        One TipoAcordo may be in may PessoaProjeto


        Attributes:
            id: Integer, Primary key
            descricao: String
            pessoa_projeto_id: Integer, Foreign Key
            pessoa_projeto_rel: Relationship
    """

    __tablename__ = "tb_tipo_acordo"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    # pessoa_projeto_id = Column(Integer, ForeignKey("tb_pessoa_projeto.id"))
    # pessoa_projeto_rel = relationship("PessoaProjeto")
