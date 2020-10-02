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

HabilidadesPessoa = Table(
    "tb_habilidades_pessoa",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("pessoa_id", Integer, ForeignKey("tb_pessoa.id")),
    Column("habilidade_id", Integer, ForeignKey("tb_habilidades.id")),
)

HabilidadesProjeto = Table(
    "tb_habilidades_projeto",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("projeto_id", Integer, ForeignKey("tb_projeto.id")),
    Column("habilidade_id", Integer, ForeignKey("tb_habilidades.id")),
)

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

ExperienciaProfArea = Table(
    "tb_exp_profissional_area",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("area_id", ForeignKey("tb_area.id"), primary_key=True),
    Column("experiencia_id", ForeignKey("tb_experiencia_profissional.id"), primary_key=True),
)

ExperienciaProjArea = Table(
    "tb_exp_projeto_area",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("area_id", ForeignKey("tb_area.id"), primary_key=True),
    Column("experiencia_id", ForeignKey("tb_experiencia_projetos.id"), primary_key=True),
)

ExperienciaAcadArea = Table(
    "tb_exp_academica_area",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("area_id", ForeignKey("tb_area.id"), primary_key=True),
    Column("experiencia_id", ForeignKey("tb_experiencia_academica.id"), primary_key=True),
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
            colaborador: Boolean
            idealizador: Boolean
            aliado: Boolean

    """

    __tablename__ = "tb_pessoa"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String, unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    nome = Column(String)
    # data_criacao uses server time with timezone and not user time by default
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())
    data_nascimento = Column(Date, default=date(year=1990, month=1, day=1))
    telefone = Column(String)
    ativo = Column(Boolean, default=True)
    superusuario = Column(Boolean, default=False)

    experiencia_profissional = relationship("ExperienciaProf")
    experiencia_projetos = relationship("ExperienciaProj")
    experiencia_academica = relationship("ExperienciaAcad")
    projeto_pessoa = relationship("Projeto", secondary=PessoaProjeto)
    areas = relationship("Area", secondary=PessoaArea)

    colaborador = Column(Boolean, default=False)
    idealizador = Column(Boolean, default=False)
    aliado = Column(Boolean, default=False)


class Projeto(Base):
    """
        Represents table "tb_projeto"


        Attributes:
            id: Integer, Primary key
            descricao: String
            visibilidade: Boolean
            objetivo: String
    """

    __tablename__ = "tb_projeto"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    descricao = Column(String)
    visibilidade = Column(Boolean, default=True)
    objetivo = Column(String)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())
    # publico_alvo = Column(String, nullable=True)
    # monetizacao = Column(String, nullable=True)


class ExperienciaProf(Base):
    """
        Represents table "tb_experiencia_profissional"


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
            cargo: String
            vinculo: String - PJ, PF, Freelancer, etc.
            areas: Relationship
    """

    __tablename__ = "tb_experiencia_profissional"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    organizacao = Column(String)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date)
    pessoa_id = Column(Integer, ForeignKey("tb_pessoa.id"), nullable=False)
    cargo = Column(String)
    vinculo = Column(String)
    areas = relationship("Area", secondary=ExperienciaProfArea)


class ExperienciaAcad(Base):
    """
        Represents table "tb_experiencia_academica"


        1. Many to Many relationship - Area
        Many experiencias may be in may Areas
        Many Areas may have many experiences

        2. One to Many relationship - Pessoa
        One Pessoa can have many Experience
        One experience can only have one Pessoa


        Attributes:
            id: Integer, Primary key
            descricao: String
            instituicao: String - Institution name the person studied
            data_inicio: Date
            data_fim: Date
            pessoa_id: Integer, Foreign Key
            escolaridade: String - education level, e.g. high school or college.
            curso: String - Specific course, e.g. Software Engineering bachelor
            situacao: String - Currently doing, finished or canceled.
            areas: Relationship
    """

    __tablename__ = "tb_experiencia_academica"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    instituicao = Column(String)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date)
    pessoa_id = Column(Integer, ForeignKey("tb_pessoa.id"), nullable=False)
    escolaridade = Column(String)
    curso = Column(String)
    situacao = Column(String)
    areas = relationship("Area", secondary=ExperienciaAcadArea)


class ExperienciaProj(Base):
    """
        Represents table "tb_experiencia_projetos"


        1. Many to Many relationship - Area
        Many experiencias may be in may Areas
        Many Areas may have many experiences

        2. One to Many relationship - Pessoa
        One Pessoa can have many Experience
        One experience can only have one Pessoa


        Attributes:
            id: Integer, Primary key
            nome: String
            descricao: String
            data_inicio: Date
            data_fim: Date
            cargo: String
            situacao: String - Currently doing, finished, canceled
            pessoa_id: Integer, Foreign Key
            areas: Relationship
    """

    __tablename__ = "tb_experiencia_projetos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date)
    cargo = Column(String)
    situacao = Column(String)
    pessoa_id = Column(Integer, ForeignKey("tb_pessoa.id"), nullable=False)
    areas = relationship("Area", secondary=ExperienciaProjArea)


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

class Habilidades(Base):

    """
        Represents table "tb_habilidades"


        Many to Many Relationship
        One Habilidade can have many Projetos,
        one Projeto can have many Habilidades as well.

        Many to Many Relationship
        One Habilidade can have many Pessoa,
        one Pessoa can have many Habilidades as well.

        Attributes:
            id: Integer, Primary key
            nome: String
    """

    __tablename__ = "tb_habilidades"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True)

    habilidades_projeto = relationship("Projeto", secondary=HabilidadesProjeto)
    habilidades_pessoa = relationship("Pessoa", secondary=HabilidadesPessoa)

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
