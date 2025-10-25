from datetime import datetime
from typing import Optional

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from persistency.models.models import Domicilio, DomicilioAnimal, DomicilioIndividuo, Individuo
from persistency.schemas.residence_schemas import ResidenceInput, ResidenceAnimalsInput, ResidenceInputPatch
from persistency.schemas.user_schemas import StatusOptions
from utils.helpers.query_helpers.handle_query_search import handle_query_search


class ResidenceService:
    @staticmethod
    async def add_new_residence(residence_input: ResidenceInput, user_id: int,  session: AsyncSession):

        residence_dict = residence_input.dict()
        del residence_dict["animais"]

        query = (
            insert(
                Domicilio
            )
            .values(
                **residence_dict,
                registered_by=user_id,
                status=StatusOptions.Active
            )
            .returning(Domicilio)
        )

        result = await session.execute(query)
        return result.fetchone()

    @staticmethod
    async def add_residence_animals(residence_id: int, animal_input: ResidenceAnimalsInput, session: AsyncSession):
        query = (
            insert(
                DomicilioAnimal
            )
            .values(
                domicilio_id=residence_id,
                animal=animal_input.animal,
                quantidade=animal_input.quantidade,
            )
            .returning(DomicilioAnimal)
        )

        result = await session.execute(query)
        return result.fetchone()

    @staticmethod
    async def get_residence_by_id(residence_id: int, session: AsyncSession):
        stmt = select(*Domicilio.__table__.columns).where(Domicilio.id == residence_id, Domicilio.deleted_at == None)
        result = await session.execute(stmt)
        return result.fetchone()

    @staticmethod
    async def get_animals_by_residence(residence_id: int, session: AsyncSession):
        stmt = select(*DomicilioAnimal.__table__.columns).where(DomicilioAnimal.domicilio_id == residence_id)
        result = await session.execute(stmt)
        return result.fetchall()

    @staticmethod
    async def update_residence(residence_id: int, residence_input: ResidenceInputPatch, user_id: int, session: AsyncSession):
        residence_dict = residence_input.dict(exclude_none=True, exclude_unset=True)
        del residence_dict["animais"]

        stmt = (
            update(Domicilio)
            .where(Domicilio.id == residence_id)
            .values(**residence_dict, last_updated_by=user_id)
            .returning(*Domicilio.__table__.columns)
        )

        result = await session.execute(stmt)
        return result.fetchone()

    @staticmethod
    async def delete_residence_animals(residence_id: int, session: AsyncSession):
        stmt = delete(DomicilioAnimal).where(DomicilioAnimal.domicilio_id == residence_id)
        await session.execute(stmt)

    @staticmethod
    async def soft_delete_residence(residence_id: int, session: AsyncSession):
        stmt = (
            update(Domicilio)
            .where(Domicilio.id == residence_id)
            .values(
                deleted_at=datetime.utcnow(),
                status=StatusOptions.Erased
            )
        )
        await session.execute(stmt)

    @staticmethod
    async def list_all_residences(session: AsyncSession, search: Optional[str], user_id: int, only_registered_by: bool):
        query = select(*Domicilio.__table__.columns).where(Domicilio.status == StatusOptions.Active)

        if only_registered_by is not None:
            query = query.where(Domicilio.registered_by == user_id)

        if search:
            query = handle_query_search(
                query,
                [
                    Domicilio.cep,
                    Domicilio.municipio,
                    Domicilio.uf,
                    Domicilio.bairro,
                    Domicilio.localizacao,
                    Domicilio.nome_logradouro,
                ],
                search
            )

        result = await session.execute(query)
        return result.fetchall()

    @staticmethod
    async def get_individuals_by_residence_id(residence_id: int, session: AsyncSession):
        query = (
            select(
                DomicilioIndividuo,
                Individuo.nome,
                Individuo.nome_social,
                Individuo.data_nascimento,
                Individuo.cpf,
                Individuo.cns,
                Individuo.celular
            )
            .join(Individuo, Individuo.id == DomicilioIndividuo.individuo_id)
            .where(DomicilioIndividuo.domicilio_id == residence_id)
        )
        result = await session.execute(query)
        return result.all()


