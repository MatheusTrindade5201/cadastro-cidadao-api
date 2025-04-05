from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse


class BaseInternalException(HTTPException):
    def __init__(self, name: str, description: str, status_code: int):
        self._name: str = "Default Exception name" if not name else name
        self._description: str = (
            "Default Exception" if not description else description
        )
        self._status_code: int = 400 if not status_code else status_code
        super().__init__(status_code=self._status_code)

    def generate_error_response(self):
        return JSONResponse(
            status_code=self._status_code,
            content={"error": self._name, "message": self._description},
        )


class InternalServerError(BaseInternalException):
    def __init__(self, name: str, description: str):
        super().__init__(name=name, description=description, status_code=500)
