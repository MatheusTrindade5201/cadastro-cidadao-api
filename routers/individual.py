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