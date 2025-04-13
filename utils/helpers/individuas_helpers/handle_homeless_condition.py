from sqlalchemy.ext.asyncio import AsyncSession

from persistency.schemas.individual_schemas import IndividualInput, CondicaoRuaInput
from service.invidual_services import IndividualServices


async def handle_homeless_condition(homeless_condition_input: CondicaoRuaInput, individual_id: int, session: AsyncSession):
    registered_homeless_condition = await IndividualServices.add_individual_homeless_condition(homeless_condition_input, individual_id, session)

    if homeless_condition_input.origem_alimentacao:
        for access in homeless_condition_input.origem_alimentacao:
            await IndividualServices.add_homeless_condition_food_access(registered_homeless_condition.id, access, session)

    if homeless_condition_input.acesso_higiene:
        for access in homeless_condition_input.acesso_higiene:
            await IndividualServices.add_homeless_condition_hygiene_access(registered_homeless_condition.id, access, session)