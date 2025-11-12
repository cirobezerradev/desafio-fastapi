from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.database import get_session
from app.schemas.schemas import AtletaIn, AtletaOut, AtletaUpdate
from app.models.models import AtletaModel


router = APIRouter(prefix='/api/v1/atletas', tags=['atletas'])


@router.post('/', response_model=AtletaOut, status_code=status.HTTP_201_CREATED)
async def create_atleta(
                atleta: AtletaIn,
                session: Annotated[AsyncSession, Depends(get_session)]
                ):
    atleta = AtletaModel(**atleta.model_dump())

    try:
        session.add(atleta)
        await session.commit()
        await session.refresh(atleta, ['centro_de_treinamento', 'categoria'])

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um atleta cadastrado com o cpf: {atleta.cpf}'
        )

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar atleta: {str(e)}"
            )
    return atleta


@router.get('/', response_model=list[AtletaOut], status_code=status.HTTP_200_OK)
async def list_atletas(
            session: Annotated[AsyncSession, Depends(get_session)],
            nome: str | None = None,
            cpf: str | None = None
            ):

    try:
        query = select(AtletaModel)

        if nome:
            query = query.where(AtletaModel.nome.ilike(f"%{nome}%"))
        if cpf:
            query = query.where(AtletaModel.cpf == cpf)

        result = await session.scalars(query)

        atletas = result.all()

        if not atletas:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum atleta encontrado"
            )

        return atletas

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Problema ao listar Atletas: {str(e)}"
            )


@router.get('/{id}', response_model=list[AtletaOut], status_code=status.HTTP_200_OK)
async def get_atleta_id(
    id: int,
    session: Annotated[AsyncSession, Depends(get_session)]
):

    atleta = await session.scalars(select(AtletaModel).where(AtletaModel.pk_id == id))

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}'
        )

    return atleta


@router.patch('/{id}', response_model=AtletaOut, status_code=status.HTTP_200_OK)
async def update_atleta(
    id: int,
    atleta_update: AtletaUpdate,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> None:

    atleta = (await session.scalars(select(AtletaModel).where(AtletaModel.pk_id == id))).first()

    atleta_update = atleta_update.model_dump(exclude_unset=True)

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no is: {id}'
        )

    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await session.commit()
    await session.refresh(atleta, ['centro_de_treinamento', 'categoria'])

    return atleta


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_atleta(
    id: int,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    result = await session.scalars(select(AtletaModel).where(AtletaModel.pk_id == id))
    atleta = result.first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado com o id: {id}'
        )

    await session.delete(atleta)
    await session.commit()
