from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from persistency.models.models import User
from persistency.schemas.residence_schemas import ResidenceInput, ResidenceInputPatch
from service.residence_service import ResidenceService
from service.shared_service import SharedService
from utils.exceptions.exception import EntityNotExists
from utils.helpers.residence_helpers.format_residence_individuals import format_residence_individuals
from utils.helpers.residence_helpers.validate_address import validate_delivery_address_creation
from utils.helpers.residence_helpers.validate_residence_update import validate_residence_update
from utils.middlewares.session_controller import TransactionSession


class ResidenceLogic:
    @staticmethod
    @TransactionSession()
    async def create_residence_logic(residence_input: ResidenceInput, username: str, session: AsyncSession):
        user = await SharedService.select_model_fields(User, session, "email", username, [User.id])

        await validate_delivery_address_creation(residence_input)

        created_residence = await ResidenceService.add_new_residence(residence_input,user.id, session)

        animals = []
        if residence_input.animais:
            for animal in residence_input.animais:
                added_animal = await ResidenceService.add_residence_animals(created_residence.id, animal, session)
                animals.append(added_animal)


        response_dict = dict(created_residence)
        response_dict["animais"] = animals

        return response_dict

    @staticmethod
    @TransactionSession()
    async def get_residence_logic(residence_id: int, session: AsyncSession):
        residence = await ResidenceService.get_residence_by_id(residence_id, session)
        animals = await ResidenceService.get_animals_by_residence(residence_id, session)
        individuals = await ResidenceService.get_individuals_by_residence_id(residence_id, session)

        if not residence:
            raise EntityNotExists("Residence not found")

        response = dict(residence)
        response["animais"] = animals
        response["individuos"] = format_residence_individuals(individuals)

        return response

    @staticmethod
    @TransactionSession()
    async def update_residence_logic(residence_id: int, residence_input: ResidenceInputPatch, username: str,
                                     session: AsyncSession):
        user = await SharedService.select_model_fields(User, session, "email", username, [User.id])

        residence = await ResidenceService.get_residence_by_id(residence_id, session)

        if not residence:
            raise EntityNotExists("Residence not found")

        await validate_residence_update(residence_input, residence)

        if residence_input.uf:
            residence_input.uf = residence_input.uf.upper()

        updated_residence = await ResidenceService.update_residence(residence_id, residence_input, user.id, session)

        animals = await ResidenceService.get_animals_by_residence(residence_id, session)
        if residence_input.animais:
            animals = []
            await ResidenceService.delete_residence_animals(residence_id, session)

            for animal in residence_input.animais:
                added_animal = await ResidenceService.add_residence_animals(residence_id, animal, session)
                animals.append(added_animal)

        response = dict(updated_residence)
        response["animais"] = animals
        return response

    @staticmethod
    @TransactionSession()
    async def delete_residence_logic(residence_id: int, session: AsyncSession):
        await ResidenceService.soft_delete_residence(residence_id, session)

    @staticmethod
    @TransactionSession()
    async def list_residences_logic(only_registered_by: bool, username: str, session: AsyncSession):
        user = await SharedService.select_model_fields(User, session, "email", username, [User.id])

        residences = await ResidenceService.list_all_residences(session, user.id, only_registered_by)

        return residences



