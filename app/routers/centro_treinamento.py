from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.models import CentroTreinamentoModel
from app.schemas.schemas import CentroTreinamentoIn, CentroTreinamentoOut


router = APIRouter(
    prefix='/api/v1/centros_de_treinamento',
    tags=['centros de treinamento']
    )


@router.post('/', response_model=CentroTreinamentoOut, status_code=status.HTTP_201_CREATED)
async def create_ct(
                ct: CentroTreinamentoIn,
                session: Annotated[AsyncSession, Depends(get_session)]
                ):
    ct = CentroTreinamentoModel(**ct.model_dump())

    try:
        session.add(ct)
        await session.commit()
        await session.refresh(ct)

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um Centro de Treinamento com o nome: {ct.nome}'
        )

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar CT: {str(e)}"
        )

    return ct


@router.get('/', response_model=list[CentroTreinamentoOut], status_code=status.HTTP_200_OK)
async def list_ct(
            session: Annotated[AsyncSession, Depends(get_session)]
            ):
    try:
        query = await session.scalars(select(CentroTreinamentoModel))
        cts = query.all()

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Problema ao listar CTs: {str(e)}"
            )
    return cts
