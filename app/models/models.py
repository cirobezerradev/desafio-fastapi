from uuid import uuid4

from sqlalchemy import UUID, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class BaseModel(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(UUID_PG(as_uuid=True), default=uuid4)


class AtletaModel(BaseModel):
    __tablename__ = 'atletas'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(50))
    cpf: Mapped[str] = mapped_column(String(11), unique=True)
    idade: Mapped[int] = mapped_column(Integer)
    peso: Mapped[float] = mapped_column(Float)
    altura: Mapped[float] = mapped_column(Float)
    sexo: Mapped[str] = mapped_column(String(1))
    centro_de_treinamento_id: Mapped[int] = mapped_column(ForeignKey('centros_de_treinamento.pk_id'))
    centro_de_treinamento: Mapped['CentroTreinamentoModel'] = relationship(back_populates='atletas', lazy='selectin')
    categoria_id: Mapped[int] = mapped_column(ForeignKey('categorias.pk_id'))
    categoria: Mapped['CategoriaModel'] = relationship(back_populates='atletas', lazy='selectin')


class CategoriaModel(BaseModel):
    __tablename__ = 'categorias'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(10), unique=True)
    atletas: Mapped[list['AtletaModel']] = relationship(back_populates='categoria')


class CentroTreinamentoModel(BaseModel):
    __tablename__ = 'centros_de_treinamento'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(20), unique=True)
    endereco: Mapped[str | None] = mapped_column(String(60))
    proprietario: Mapped[str | None] = mapped_column(String(30))
    atletas: Mapped[list['AtletaModel']] = relationship(back_populates='centro_de_treinamento')
