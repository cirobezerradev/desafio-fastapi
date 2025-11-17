from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.models import CategoriaModel
from app.schemas.schemas import CategoriaIn, CategoriaOut

router = APIRouter(prefix='/api/v1/categorias', tags=['categorias'])


@router.post('/', response_model=CategoriaOut, status_code=status.HTTP_201_CREATED)
async def create_categoria(categoria: CategoriaIn, session: Annotated[AsyncSession, Depends(get_session)]):
    categoria = CategoriaModel(**categoria.model_dump())

    try:
        session.add(categoria)
        await session.commit()
        await session.refresh(categoria)

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já Existe uma categoria cadastrada com o nome: {categoria.nome}',
        )

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Erro ao criar categoria: {str(e)}')

    return categoria


@router.get('/', response_model=list[CategoriaOut], status_code=status.HTTP_200_OK)
async def list_categorias(session: Annotated[AsyncSession, Depends(get_session)]):

    try:
        query = await session.scalars(select(CategoriaModel))
        categorias = query.all()

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Problema ao listar categorias: {str(e)}')
    return categorias
