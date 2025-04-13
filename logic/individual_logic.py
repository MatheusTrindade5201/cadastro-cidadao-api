from sqlalchemy.ext.asyncio import AsyncSession

from persistency.models.models import User
from persistency.schemas.individual_schemas import IndividualInput
from service.invidual_services import IndividualServices
from service.shared_service import SharedService
from utils.exceptions.exception import InvalidEmail
from utils.helpers.individuas_helpers.handle_associations import handle_association
from utils.helpers.individuas_helpers.handle_homeless_condition import handle_homeless_condition
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