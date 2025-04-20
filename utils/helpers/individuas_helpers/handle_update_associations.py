from sqlalchemy.ext.asyncio import AsyncSession

from persistency.schemas.individual_schemas import IndividualInput
from service.invidual_services import IndividualServices
from utils.helpers.individuas_helpers.handle_associations import handle_association
from utils.helpers.individuas_helpers.handle_homeless_condition import handle_homeless_condition


async def handle_update_associations(
        individual_id: int,
        individual_input: IndividualInput,
        session: AsyncSession
):
    await IndividualServices.reset_individual_association(individual_id, session)

    await handle_association(individual_input, individual_id, session)

    if individual_input.condicao_rua:
        await handle_homeless_condition(individual_input.condicao_rua, individual_id, session)