from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from persistency.models.models import User
from persistency.schemas.individual_schemas import IndividualInput
from service.invidual_services import IndividualServices
from service.shared_service import SharedService
from utils.exceptions.exception import InvalidEmail, EntityNotExists
from utils.helpers.individuas_helpers.handle_associations import handle_association
from utils.helpers.individuas_helpers.handle_homeless_condition import handle_homeless_condition
from utils.helpers.individuas_helpers.handle_update_associations import handle_update_associations
from utils.helpers.individuas_helpers.handle_update_data import handle_update_data
from utils.helpers.individuas_helpers.validate_CPF import validate_CPF
from utils.helpers.validators.email_address_validator import email_validator
from utils.middlewares.session_controller import TransactionSession


class IndividualLogic:
    @staticmethod
    @TransactionSession()
    async def create_individual_logic(individual_input: IndividualInput, username: str, session: AsyncSession):
        user = await SharedService.select_model_fields(User, session, "email", username, [User.id])

        individual_input.cpf = validate_CPF(individual_input.cpf)

        if individual_input.email:
            if not email_validator(individual_input.email):
                raise InvalidEmail(individual_input.email)


        created_individual = await IndividualServices.create_individual(individual_input, user.id, session)

        await handle_association(individual_input, created_individual.id, session)

        if individual_input.condicao_rua:
            await handle_homeless_condition(individual_input.condicao_rua, created_individual.id, session)

        return individual_input

    @staticmethod
    @TransactionSession()
    async def update_individual_logic(
            individual_id: int,
            individual_input: IndividualInput,
            username: str,
            session: AsyncSession
    ):
        user = await SharedService.select_model_fields(User, session, "email", username, [User.id])

        existing_individual = await IndividualServices.get_individual_by_id(individual_id, session)
        if not existing_individual:
            raise EntityNotExists("Individual not found")

        update_data = handle_update_data(individual_input)

        await IndividualServices.update_individual(individual_id, update_data, user.id, session)

        await handle_update_associations(individual_id, individual_input, session)

        return {"message": "Individual updated successfully"}

    @staticmethod
    @TransactionSession()
    async def get_individual_logic(individual_id: int, session: AsyncSession):
        individual = await IndividualServices.get_individual_by_id(individual_id, session)
        if not individual:
            raise EntityNotExists("Individual not found")

        caretakers = await IndividualServices.get_caretakers_by_individual_id(individual_id, session)
        conditions = await IndividualServices.get_conditions_by_individual_id(individual_id, session)
        deficiencies = await IndividualServices.get_deficiencies_by_individual_id(individual_id, session)
        cardiac_diseases = await IndividualServices.get_cardiac_diseases_by_individual_id(individual_id, session)
        respiratory_diseases = await IndividualServices.get_respiratory_diseases_by_individual_id(individual_id, session)
        homeless_condition = await IndividualServices.get_homeless_condition_by_individual_id(individual_id, session)

        result = individual.__dict__
        result["cuidadores"] = [c.cuidador for c in caretakers.scalars()]
        result["condicoes"] = [c.condicao for c in conditions.scalars()]
        result["deficiencias"] = [d.deficiencia for d in deficiencies.scalars()]
        result["doencas_cardiacas"] = [cd.doenca for cd in cardiac_diseases.scalars()]
        result["doencas_respiratorias"] = [rd.doenca for rd in respiratory_diseases.scalars()]

        homeless_condition_result = homeless_condition.scalars().first()
        if homeless_condition_result:
            homeless_condition_dict = homeless_condition_result.__dict__
            result["condicao_rua"] = homeless_condition_dict

            food_access = await IndividualServices.get_homeless_condition_food_access(homeless_condition_dict["id"], session)
            hygiene_access = await IndividualServices.get_homeless_condition_hygiene_access(homeless_condition_dict["id"], session)

            if food_access:
                result["condicao_rua"]["origem_alimentacao"] = [c.origem for c in food_access.scalars()]
            if hygiene_access:
                result["condicao_rua"]["acesso_higiene"] = [c.acesso_higiene for c in hygiene_access.scalars()]


        return result

    @staticmethod
    @TransactionSession()
    async def get_all_individuals_logic(registered_by: Optional[int], session: AsyncSession):
        individuals = await IndividualServices.get_all_individuals(registered_by, session)
        return [individual.__dict__ for individual in individuals]

    @staticmethod
    @TransactionSession()
    async def delete_individual_logic(individual_id: int, username: str, session: AsyncSession):
        individual = await IndividualServices.get_individual_by_id(individual_id, session)
        if not individual:
            raise EntityNotExists("Individual not found")

        await IndividualServices.delete_individual(individual_id, session)
        return None