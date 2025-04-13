import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from service.invidual_services import IndividualServices


def build_tasks(entities, handler_fn, individual_id: int, session: AsyncSession):
    return [
        handler_fn(individual_id, entity, session)
        for entity in (entities or [])
    ]

async def handle_association(individual_input, individual_id, session):
    tasks = []

    tasks.extend(build_tasks(
        individual_input.cuidadores,
        IndividualServices.add_individual_caretakers,
        individual_id, session
    ))

    tasks.extend(build_tasks(
        individual_input.condicoes,
        IndividualServices.add_individual_condition,
        individual_id, session
    ))

    tasks.extend(build_tasks(
        individual_input.deficiencias,
        IndividualServices.add_individual_deficiency,
        individual_id, session
    ))

    tasks.extend(build_tasks(
        individual_input.doencas_cardiacas,
        IndividualServices.add_individual_cardiac_disease,
        individual_id, session
    ))

    tasks.extend(build_tasks(
        individual_input.doencas_respiratorias,
        IndividualServices.add_individual_respiratory_disease,
        individual_id, session
    ))

    if tasks:
        await asyncio.gather(*tasks)