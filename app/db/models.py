import enum
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
from sqlalchemy.ext.associationproxy import association_proxy

from datetime import date

# Tables created from M*N relationships

HabilidadesPessoa = Table(
    "tb_habilidades_pessoa",
    Base.metadata,
    Column("pessoa_id", Integer, ForeignKey("tb_pessoa.id"), primary_key=True),
    Column(
        "habilidade_id",
        Integer,
        ForeignKey("tb_habilidades.id"),
        primary_key=True,
    ),
)

HabilidadesProjeto = Table(
    "tb_habilidades_projeto",
    Base.metadata,
    Column(
        "projeto_id", Integer, ForeignKey("tb_projeto.id"), primary_key=True
    ),
    Column(
        "habilidade_id",
        Integer,
        ForeignKey("tb_habilidades.id"),
        primary_key=True,
    ),
)


ExperienciaProfArea = Table(
    "tb_exp_profissional_area",
    Base.metadata,
    Column("area_id", ForeignKey("tb_area.id"), primary_key=True),
    Column(
        "experiencia_id",
        ForeignKey("tb_experiencia_profissional.id"),
        primary_key=True,
    ),
)

ExperienciaProjArea = Table(
    "tb_exp_projeto_area",
    Base.metadata,
    Column("area_id", ForeignKey("tb_area.id"), primary_key=True),
    Column(
        "experiencia_id",
        ForeignKey("tb_experiencia_projetos.id"),
        primary_key=True,
    ),
)

ExperienciaAcadArea = Table(
    "tb_exp_academica_area",
    Base.metadata,
    Column("area_id", ForeignKey("tb_area.id"), primary_key=True),
    Column(
        "experiencia_id",
        ForeignKey("tb_experiencia_academica.id"),
        primary_key=True,
    ),
)

PessoaArea = Table(
    "tb_pessoa_area",
    Base.metadata,
    Column("pessoa_id", ForeignKey("tb_pessoa.id"), primary_key=True),
    Column("area_id", ForeignKey("tb_area.id"), primary_key=True),
)

ProjetoArea = Table(
    "tb_projeto_area",
    Base.metadata,
    Column("projeto_id", ForeignKey("tb_projeto.id"), primary_key=True),
    Column("area_id", ForeignKey("tb_area.id"), primary_key=True),
)

PessoaAreaProjeto = Table(
    "tb_area_pessoa_projeto",
    Base.metadata,
    Column("area_id", ForeignKey("tb_area.id"), primary_key=True),
    Column(
        "pessoa_projeto_id",
        ForeignKey("tb_pessoa_projeto.id"),
        primary_key=True,
    ),
)

PessoaHabilidadesProjeto = Table(
    "tb_habilidades_pessoa_projeto",
    Base.metadata,
    Column("habilidade_id", ForeignKey("tb_habilidades.id"), primary_key=True),
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
        data_atualizacao: Datetime - default uses function Now()
        on the server
        data_nascimento: Date
        telefone: String
        ativo: Boolean
        superusuario: Boolean
        colaborador: Boolean
        idealizador: Boolean
        aliado: Boolean
        areas: relationship
        habilidades: relationship
        experiencia_profissional: relationship
        experiencia_projetos: relationship
        experiencia_academica: relationship
        projeto: relationship
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
    foto_perfil = Column(String)
    ativo = Column(Boolean, default=True)
    superusuario = Column(Boolean, default=False)

    experiencia_profissional = relationship("ExperienciaProf")
    experiencia_projetos = relationship("ExperienciaProj")
    experiencia_academica = relationship("ExperienciaAcad")
    pessoa_projeto = relationship("PessoaProjeto", back_populates="pessoa")

    areas = relationship("Area", secondary=PessoaArea)
    habilidades = relationship("Habilidades", secondary=HabilidadesPessoa)

    colaborador = Column(Boolean, default=False)
    idealizador = Column(Boolean, default=False)
    aliado = Column(Boolean, default=False)

    projeto = relationship("Projeto", back_populates="dono")

    def __repr__(self):
        return f"<Pessoa {self.id}, {self.email}, {self.superusuario}>"


class Projeto(Base):
    """
    Represents table "tb_projeto"


    Attributes:
        id: Integer, Primary key
        pessoa_id: Integer, Foreign Key
        descricao: String
        data_atualizacao: Datetime - default uses function Now()
        data_criacao: Datetime - default uses DB function Now()
        visibilidade: Boolean
        objetivo: String
        dono: relationship
        areas: relationship
        habilidades: relationship
        projeto_pessoa: relationship
        reacoes: association_proxy - extended form of many-to-many relationship
    """

    __tablename__ = "tb_projeto"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    descricao = Column(String)
    visibilidade = Column(Boolean, default=True)
    objetivo = Column(String)
    foto_capa = Column(String)
    habilidades = relationship("Habilidades", secondary=HabilidadesProjeto)
    areas = relationship("Area", secondary=ProjetoArea)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())
    projeto_pessoa = relationship("PessoaProjeto", back_populates="projeto")

    pessoa_id = Column(Integer, ForeignKey("tb_pessoa.id"), nullable=True)
    dono = relationship("Pessoa", back_populates="projeto")
    reacoes = association_proxy("projeto_reacoes", "pessoa")
    # publico_alvo = Column(String, nullable=True)
    # monetizacao = Column(String, nullable=True)


class PessoaProjeto(Base):

    __tablename__ = "tb_pessoa_projeto"

    id = Column(Integer, primary_key=True, index=True)
    pessoa_id = Column(Integer, ForeignKey("tb_pessoa.id"))
    projeto_id = Column(Integer, ForeignKey("tb_projeto.id"))
    papel_id = Column(Integer, ForeignKey("tb_papel.id"))
    tipo_acordo_id = Column(Integer, ForeignKey("tb_tipo_acordo.id"))
    papel = relationship("Papel")
    tipo_acordo = relationship("TipoAcordo")
    pessoa = relationship("Pessoa", back_populates="pessoa_projeto")
    projeto = relationship("Projeto", back_populates="projeto_pessoa")
    areas = relationship("Area", secondary=PessoaAreaProjeto)
    habilidades = relationship(
        "Habilidades", secondary=PessoaHabilidadesProjeto
    )
    descricao = Column(String)
    situacao = Column(String)
    titulo = Column(String, nullable=True)
    remunerado = Column(Boolean, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())


class Notificacao(Base):

    __tablename__ = "tb_notificacao"

    id = Column(Integer, primary_key=True, index=True)
    remetente_id = Column(Integer, ForeignKey("tb_pessoa.id"))
    destinatario_id = Column(Integer, ForeignKey("tb_pessoa.id"))
    projeto_id = Column(Integer, ForeignKey("tb_projeto.id"))
    pessoa_projeto_id = Column(Integer, ForeignKey("tb_pessoa_projeto.id"))
    situacao = Column(String, nullable = False)
    lido = Column(Boolean, nullable = False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_visualizacao = Column(DateTime(timezone=True), onupdate=func.now())

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
        "Area",
        backref=backref("area_pai", remote_side=[id]),
        cascade="all, delete-orphan",
        lazy="joined",
        join_depth=2,
        passive_deletes=True,
    )

    # def __str__(self, level=0):
    #     ret = f"{'    ' * level} {repr(self.descricao)} \n"
    #     for child in self.area_pai_rel:
    #         ret += child.__str__(level + 1)
    #     return ret

    def __repr__(self):
        return f"<Area {self.id}>"


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

    def __repr__(self):
        return f"<{self.__tablename__} {self.id}>"


class Papel(Base):
    """
    Represents table "tb_papel"


    Many to One relationship
    One pessoa_projeto has one Papel, meanwhile
    One Papel may be in may PessoaProjeto


    Attributes:
        id: Integer, Primary key
        descricao: String
        pessoa_projeto: Relationship
    """

    __tablename__ = "tb_papel"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    pessoa_projeto = relationship("PessoaProjeto", back_populates="papel")


class TipoAcordo(Base):
    """
    Represents table "tb_tipo_acordo"


    Many to One relationship
    One pessoa_projeto has one TipoAcordo, meanwhile
    One TipoAcordo may be in may PessoaProjeto


    Attributes:
        id: Integer, Primary key
        descricao: String
        pessoa_projeto: Relationship
    """

    __tablename__ = "tb_tipo_acordo"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    pessoa_projeto = relationship("PessoaProjeto", back_populates="tipo_acordo")


class Reacoes(Base):
    """
    Represents table "tb_reacoes"


    Many to Many relationship
    One Projeto has many Reacoes,
    One Reacao is exclusively from some pessoa in some projeto


    Attributes:
        id_projeto: Integer, Primary key, Foreign Key
        id_pessoa: Integer, Primary key, Foreign Key
        reacao: String
        data_criacao: Datetime - default uses DB function Now()
        data_atualizacao: Datetime - default uses function Now()
    """

    __tablename__ = "tb_reacoes"

    pessoa_id = Column(
        Integer, ForeignKey("tb_pessoa.id"), primary_key=True, index=True
    )
    projeto_id = Column(
        Integer, ForeignKey("tb_projeto.id"), primary_key=True, index=True
    )
    reacao = Column(String)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())

    projeto = relationship(
        Projeto,
        backref=backref("projeto_reacoes", cascade="all, delete-orphan"),
    )

    pessoa = relationship("Pessoa")
