from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, PositiveFloat


class BaseSchema(BaseModel):
    class Config:
        extra = 'forbid'
        from_attributes = True


class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome da Categoria', max_length=10)]


class CategoriaOut(BaseSchema):
    id: Annotated[UUID, Field(alias='id')]
    pk_id: Annotated[int, Field(description='Id da Categoria')]
    nome: Annotated[str, Field(description='Nome da Categoria', max_length=10)]

    model_config = ConfigDict(from_attributes=True)


class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome da CT', max_length=20)]
    endereco: Annotated[str | None, Field(description='Endereço do CT', max_length=60)] = None
    proprietario: Annotated[str | None, Field(description='Proprietário do CT', max_length=30)] = None


class CentroTreinamentoOut(BaseSchema):
    id: Annotated[UUID, Field(alias='id')]
    pk_id: Annotated[int, Field(description='Id do CT')]
    nome: Annotated[str, Field(description='Nome da CT', max_length=20)]
    endereco: Annotated[str | None, Field(description='Endereço do CT', max_length=60)]
    proprietario: Annotated[str | None, Field(description='Proprietário do CT', max_length=30)]

    model_config = ConfigDict(from_attributes=True)


class AtletaIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Atleta', example='João', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do Atleta', example='11122233344', max_length=11)]
    idade: Annotated[int, Field(description='Idade do Atleta', example=25)]
    peso: Annotated[PositiveFloat, Field(description='Peso do Atleta', example=70.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do Atleta', example=1.77)]
    sexo: Annotated[str, Field(description='Sexo do Atleta', example='M', max_length=1)]
    centro_de_treinamento_id: Annotated[int, Field()]
    categoria_id: Annotated[int, Field()]


class AtletaOut(BaseSchema):
    id: Annotated[UUID, Field(alias='id')]
    pk_id: Annotated[int, Field(description='Id do Atleta')]
    nome: Annotated[str, Field(description='Nome do Atleta', example='João', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do Atleta', example='11122233344', max_length=11)]
    idade: Annotated[int, Field(description='Idade do Atleta', example=25)]
    peso: Annotated[PositiveFloat, Field(description='Peso do Atleta', example=70.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do Atleta', example=1.77)]
    sexo: Annotated[str, Field(description='Sexo do Atleta', example='M', max_length=1)]
    centro_de_treinamento: CentroTreinamentoIn
    categoria: CategoriaIn

    model_config = ConfigDict(from_attributes=True)


class AtletaUpdate(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Atleta', example='João', max_length=50)]
    idade: Annotated[int, Field(description='Idade do Atleta', example=25)]
