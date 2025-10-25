from typing import Optional

from fastapi import APIRouter, Depends, Query

from logic.residence_logic import ResidenceLogic
from persistency.connection import get_db
from persistency.schemas.residence_schemas import ResidenceInput, ResidenceInputPatch
from persistency.schemas.user_schemas import RoleOptions
from utils.helpers.validators.token_validator import validate_session_with_roles, validate_session

residence_router = APIRouter(prefix="/residence", tags=["residence"])

@residence_router.post(
    "/",
    description="Route to register a residence",
    status_code=201,
    dependencies=[Depends(get_db), Depends(validate_session_with_roles(RoleOptions.Default, RoleOptions.Admin))],
)
async def create_residence(residence_input: ResidenceInput, payload=Depends(validate_session)):
    return await ResidenceLogic.create_residence_logic(residence_input, payload.get("sub"))


@residence_router.get(
    "/{residence_id}",
    description="Get residence by ID",
    dependencies=[Depends(get_db), Depends(validate_session_with_roles(RoleOptions.Default, RoleOptions.Admin))],
)
async def get_residence(residence_id: int):
    return await ResidenceLogic.get_residence_logic(residence_id)


@residence_router.patch(
    "/{residence_id}",
    description="Update residence by ID",
    dependencies=[Depends(get_db), Depends(validate_session_with_roles(RoleOptions.Default, RoleOptions.Admin))],
)
async def update_residence(residence_id: int, residence_input: ResidenceInputPatch, payload=Depends(validate_session)):
    return await ResidenceLogic.update_residence_logic(residence_id, residence_input, payload.get("sub"))


@residence_router.delete(
    "/{residence_id}",
    description="Delete residence by ID",
    status_code=204,
    dependencies=[Depends(get_db), Depends(validate_session_with_roles(RoleOptions.Admin))],
)
async def delete_residence(residence_id: int):
    await ResidenceLogic.delete_residence_logic(residence_id)


@residence_router.get(
    "/",
    description="List all residences (optional filter by registered_by)",
    dependencies=[Depends(get_db), Depends(validate_session)],
)
async def list_residences(
        only_registered_by: bool = Query(False, description="Get users registers"),
        search: Optional[str] = Query(None, description="Filter individuals"),
        payload=Depends(validate_session)
):
    return await ResidenceLogic.list_residences_logic(only_registered_by, search, payload.get("sub"))
