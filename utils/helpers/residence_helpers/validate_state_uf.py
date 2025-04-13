from persistency.schemas.residence_schemas import STATES_MAP
from utils.exceptions.exception import InvalidStateUF


def validate_state_uf(state_uf: str):
    if state_uf not in STATES_MAP:
        raise InvalidStateUF(state_uf)
