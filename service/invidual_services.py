from typing import List

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from persistency.models.models import Individuo, CuidadorIndividuo, IndividuoDoencaCardiaca, IndividuoDeficiencia, \
    IndividuoDoencaRespiratoria, IndividuoCondicao, IndividuoCondicaoRua, CondicaoRuaOrigemAlimentacao, \
    CondicaoRuaAcessoHigiene
from persistency.schemas.individual_schemas import IndividualInput, CondicaoRuaInput


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

