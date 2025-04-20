from typing import Optional

from fastapi import APIRouter, Depends

from logic.individual_logic import IndividualLogic
from persistency.connection import get_db
from persistency.schemas.individual_schemas import IndividualInput
from persistency.schemas.user_schemas import RoleOptions
from utils.helpers.validators.token_validator import validate_session_with_roles, validate_session

individual_router = APIRouter(prefix="/individual", tags=["individual"])

@individual_router.post(
    "/",
    description="Route to add an individual",
    status_code=201,
    dependencies=[Depends(get_db), Depends(validate_session_with_roles(RoleOptions.Default, RoleOptions.Admin))],
)
async def create_individual(individual_input:IndividualInput, payload=Depends(validate_session)):
    return await IndividualLogic.create_individual_logic(individual_input, payload.get("sub"))

@individual_router.patch(
    "/{individual_id}",
    description="Route to update an individual",
    status_code=200,
    dependencies=[Depends(get_db), Depends(validate_session_with_roles(RoleOptions.Default, RoleOptions.Admin))],
)
async def update_individual(
    individual_id: int,
    individual_input: IndividualInput,
    payload=Depends(validate_session)
):
    return await IndividualLogic.update_individual_logic(individual_id, individual_input, payload.get("sub"))

@individual_router.get(
    "/{individual_id}",
    description="Route to get an individual by id",
    status_code=200,
    dependencies=[Depends(get_db), Depends(validate_session_with_roles(RoleOptions.Default, RoleOptions.Admin))],
)
async def get_individual(
    individual_id: int
):
    return await IndividualLogic.get_individual_logic(individual_id)

@individual_router.get(
    "/",
    description="Route to get all individuals, optionally filtered by registered_by",
    status_code=200,
    dependencies=[Depends(get_db), Depends(validate_session_with_roles(RoleOptions.Default, RoleOptions.Admin))],
)
async def get_all_individuals(
    registered_by: Optional[int] = None
):
    return await IndividualLogic.get_all_individuals_logic(registered_by)

@individual_router.delete(
    "/{individual_id}",
    description="Route to delete an individual",
    status_code=204,
    dependencies=[Depends(get_db), Depends(validate_session_with_roles(RoleOptions.Admin))],
)
async def delete_individual(
    individual_id: int,
    payload=Depends(validate_session)
):
    return await IndividualLogic.delete_individual_logic(individual_id, payload.get("sub"))