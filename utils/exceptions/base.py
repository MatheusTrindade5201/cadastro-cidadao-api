from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse


class BaseInternalException(HTTPException):
    def __init__(
        self,
        name: str,
        description: str = None,
        descriptions: dict = None,
        status_code: int = 400,
    ):
        self._name = name or "Default Exception name"
        self._status_code = status_code or 400
        self._description = descriptions or description or "Default Exception"

        super().__init__(status_code=self._status_code)

    def generate_error_response(self):
        return JSONResponse(
            status_code=self._status_code,
            content={
                "error": self._name,
                "message": self._description,
            },
        )



class InternalServerError(BaseInternalException):
    def __init__(self, name: str, description: str):
        super().__init__(name=name, description=description, status_code=500)
