import asyncio
from datetime import datetime
from typing import List, Optional

from sqlalchemy import insert, update, delete, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from persistency.models.models import Individuo, CuidadorIndividuo, IndividuoDoencaCardiaca, IndividuoDeficiencia, \
    IndividuoDoencaRespiratoria, IndividuoCondicao, IndividuoCondicaoRua, CondicaoRuaOrigemAlimentacao, \
    CondicaoRuaAcessoHigiene, DomicilioIndividuo, Domicilio
from persistency.schemas.individual_schemas import IndividualInput, CondicaoRuaInput, DomicilioIndividuoInput, \
    DomicilioIndividuoUpdateInput
from utils.helpers.time_helpers.utc_to_local import utc_to_local


class IndividualServices:
    @staticmethod
    async def create_individual(individual_input: IndividualInput, user_id: int, session: AsyncSession):
        individual_dict = individual_input.dict()

        del individual_dict["cuidadores"]
        del individual_dict["deficiencias"]
        del individual_dict["doencas_cardiacas"]
        del individual_dict["doencas_respiratorias"]
        del individual_dict["doencas_renais"]
        del individual_dict["condicao_rua"]
        del individual_dict["condicoes"]

        query = (
            insert(
                Individuo
            )
            .values(
                **individual_dict,
                registered_by=user_id
            )
            .returning(Individuo)
        )

        result = await session.execute(query)
        return result.fetchone()

    @staticmethod
    async def add_individual_caretakers(individual_id: int, caretakers_input: str, session: AsyncSession):
        query = (
            insert(
                CuidadorIndividuo
            )
            .values(
                individuo_id=individual_id,
                cuidador=caretakers_input,
            )
            .returning(CuidadorIndividuo)
        )

        result = await session.execute(query)
        return result.fetchone()

    @staticmethod
    async def add_individual_cardiac_disease(individual_id: int, disease_input: str, session: AsyncSession):
        query = (
            insert(
                IndividuoDoencaCardiaca
            )
            .values(
                individuo_id=individual_id,
                doenca=disease_input,
            )
            .returning(IndividuoDoencaCardiaca)
        )

        result = await session.execute(query)
        return result.fetchone()

    @staticmethod
    async def add_individual_deficiency(individual_id: int, deficiency_input: str, session: AsyncSession):
        query = (
            insert(
                IndividuoDeficiencia
            )
            .values(
                individuo_id=individual_id,
                deficiencia=deficiency_input,
            )
            .returning(IndividuoDeficiencia)
        )

        result = await session.execute(query)
        return result.fetchone()

    @staticmethod
    async def add_individual_respiratory_disease(individual_id: int, disease_input: str, session: AsyncSession):
        query = (
            insert(
                IndividuoDoencaRespiratoria
            )
            .values(
                individuo_id=individual_id,
                doenca=disease_input,
            )
            .returning(IndividuoDoencaRespiratoria)
        )

        result = await session.execute(query)
        return result.fetchone()

    @staticmethod
    async def add_individual_condition(individual_id: int, condition_input: str, session: AsyncSession):
        query = (
            insert(
                IndividuoCondicao
            )
            .values(
                individuo_id=individual_id,
                condicao=condition_input,
            )
            .returning(IndividuoCondicao)
        )

        result = await session.execute(query)
        return result.fetchone()

    @staticmethod
    async def add_individual_homeless_condition(homeless_condition_input: CondicaoRuaInput, individual_id: int, session: AsyncSession):
        homeless_condition_dict = homeless_condition_input.dict()

        del homeless_condition_dict["origem_alimentacao"]
        del homeless_condition_dict["acesso_higiene"]

        query = (
            insert(
                IndividuoCondicaoRua
            )
            .values(
                **homeless_condition_dict,
                individuo_id=individual_id
            )
            .returning(IndividuoCondicaoRua)
        )

        result = await session.execute(query)
        return result.fetchone()

    @staticmethod
    async def add_homeless_condition_food_access(homeless_condition_id: int, food_access_input: str, session: AsyncSession):
        query = (
            insert(
                CondicaoRuaOrigemAlimentacao
            )
            .values(
                condicao_rua_id=homeless_condition_id,
                origem=food_access_input,
            )
            .returning(CondicaoRuaOrigemAlimentacao)
        )

        result = await session.execute(query)
        return result.fetchone()

    @staticmethod
    async def add_homeless_condition_hygiene_access(homeless_condition_id: int, hygiene_access_input: str, session: AsyncSession):
        query = (
            insert(
                CondicaoRuaAcessoHigiene
            )
            .values(
                condicao_rua_id=homeless_condition_id,
                acesso_higiene=hygiene_access_input,
            )
            .returning(CondicaoRuaAcessoHigiene)
        )

        result = await session.execute(query)
        return result.fetchone()

    @staticmethod
    async def get_individual_by_id(individual_id: int, session: AsyncSession):
        query = select(Individuo).where(Individuo.id == individual_id)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_all_individuals(registered_by: Optional[int], session: AsyncSession):
        query = select(Individuo)
        if registered_by:
            query = query.where(Individuo.registered_by == registered_by)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update_individual(
            individual_id: int,
            update_data: dict,
            user_id: int,
            session: AsyncSession
    ):
            query = (
                update(Individuo)
                .where(Individuo.id == individual_id)
                .values(**update_data, last_updated_by=user_id)
            )
            await session.execute(query)

    @staticmethod
    async def reset_individual_association(individual_id: int, session: AsyncSession):
        tasks = [session.execute(delete(CuidadorIndividuo).where(CuidadorIndividuo.individuo_id == individual_id)),
                 session.execute(delete(IndividuoCondicao).where(IndividuoCondicao.individuo_id == individual_id)),
                 session.execute(
                     delete(IndividuoDeficiencia).where(IndividuoDeficiencia.individuo_id == individual_id)),
                 session.execute(
                     delete(IndividuoDoencaCardiaca).where(IndividuoDoencaCardiaca.individuo_id == individual_id)),
                 session.execute(
                     delete(IndividuoDoencaRespiratoria).where(
                         IndividuoDoencaRespiratoria.individuo_id == individual_id)), session.execute(
                delete(IndividuoCondicaoRua).where(IndividuoCondicaoRua.individuo_id == individual_id))]

        await asyncio.gather(*tasks)

    @staticmethod
    async def get_caretakers_by_individual_id(individual_id: int, session: AsyncSession):
        return await session.execute(
        select(CuidadorIndividuo).where(CuidadorIndividuo.individuo_id == individual_id))

    @staticmethod
    async def get_conditions_by_individual_id(individual_id: int, session: AsyncSession):
        return await session.execute(
        select(IndividuoCondicao).where(IndividuoCondicao.individuo_id == individual_id))

    @staticmethod
    async def get_deficiencies_by_individual_id(individual_id: int, session: AsyncSession):
        return await session.execute(
        select(IndividuoDeficiencia).where(IndividuoDeficiencia.individuo_id == individual_id))

    @staticmethod
    async def get_cardiac_diseases_by_individual_id(individual_id: int, session: AsyncSession):
        return  await session.execute(
        select(IndividuoDoencaCardiaca).where(IndividuoDoencaCardiaca.individuo_id == individual_id))

    @staticmethod
    async def get_respiratory_diseases_by_individual_id(individual_id: int, session: AsyncSession):
        return await session.execute(
        select(IndividuoDoencaRespiratoria).where(IndividuoDoencaRespiratoria.individuo_id == individual_id))

    @staticmethod
    async def get_homeless_condition_by_individual_id(individual_id: int, session: AsyncSession):
        return await session.execute(
        select(IndividuoCondicaoRua).where(IndividuoCondicaoRua.individuo_id == individual_id))

    @staticmethod
    async def get_homeless_condition_food_access(homeless_condition_id: int, session: AsyncSession):
        return await session.execute(
        select(CondicaoRuaOrigemAlimentacao).where(CondicaoRuaOrigemAlimentacao.condicao_rua_id == homeless_condition_id))

    @staticmethod
    async def get_homeless_condition_hygiene_access(homeless_condition_id: int, session: AsyncSession):
        return await session.execute(
        select(CondicaoRuaAcessoHigiene).where(CondicaoRuaAcessoHigiene.condicao_rua_id == homeless_condition_id))

    @staticmethod
    async def delete_individual(individual_id: int, session: AsyncSession):
        query = (
            update(Individuo)
            .where(Individuo.id == individual_id)
            .values(deleted_at=utc_to_local(datetime.utcnow())
            ))

        await session.execute(query)

    @staticmethod
    async def associate_individual_with_residence(
            data: DomicilioIndividuoInput,
            session: AsyncSession
    ):
        query = (
            insert(DomicilioIndividuo)
            .values(**data.dict())
            .returning(DomicilioIndividuo)
        )
        result = await session.execute(query)
        return result.fetchone()

    @staticmethod
    async def update_association(
            domicilio_id: int,
            individuo_id: int,
            data: DomicilioIndividuoUpdateInput,
            session: AsyncSession
    ):
        update_data = data.dict(exclude_unset=True)

        if not update_data:
            return None

        query = (
            update(DomicilioIndividuo)
            .where(
                (DomicilioIndividuo.domicilio_id == domicilio_id) &
                (DomicilioIndividuo.individuo_id == individuo_id)
            )
            .values(**update_data)
            .returning(DomicilioIndividuo)
        )
        result = await session.execute(query)
        return result.fetchone()

    @staticmethod
    async def disassociate_individual_from_residence(
            domicilio_id: int,
            individuo_id: int,
            session: AsyncSession
    ):
        query = (
            delete(DomicilioIndividuo)
            .where(
                (DomicilioIndividuo.domicilio_id == domicilio_id) &
                (DomicilioIndividuo.individuo_id == individuo_id)
            )
            .returning(DomicilioIndividuo.domicilio_id, DomicilioIndividuo.individuo_id)
        )
        result = await session.execute(query)
        return result.fetchone()

    @staticmethod
    async def get_residence_individual(
            domicilio_id: int,
            individuo_id: int,
            session: AsyncSession
    ):
        query = (
            select(
                DomicilioIndividuo
            )
            .where(
                and_(
                    DomicilioIndividuo.domicilio_id == domicilio_id,
                    DomicilioIndividuo.individuo_id == individuo_id
                )
            )
        )

        result = await session.execute(query)
        return result.fetchone()

    @staticmethod
    async def get_residences_by_individual_id(individual_id: int, session: AsyncSession):
        query = (
            select(
                DomicilioIndividuo,
                Domicilio.cep,
                Domicilio.municipio,
                Domicilio.uf,
                Domicilio.bairro,
                Domicilio.tipo_logradouro,
                Domicilio.nome_logradouro,
                Domicilio.numero,
                Domicilio.complemento
            )
            .join(Domicilio, Domicilio.id == DomicilioIndividuo.domicilio_id)
            .where(DomicilioIndividuo.individuo_id == individual_id)
        )
        result = await session.execute(query)
        return result.all()

