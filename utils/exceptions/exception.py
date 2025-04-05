from .base import BaseInternalException


class UserAlreadyExists(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Error inserting on database",
            description=description,
            status_code=400,
        )


class InvalidCpfInserted(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Error inserting on database",
            description=description,
            status_code=400,
        )


class InvalidEmailInserted(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Error inserting on database",
            description=description,
            status_code=400,
        )


class WeakPasswordInserted(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Error inserting on database",
            description=description,
            status_code=400,
        )


class InvalidPasswordInserted(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="The password entered is not valid",
            description=description,
            status_code=401,
        )


class UnauthorizedLogin(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Authentication fail",
            description=description,
            status_code=401,
        )


class ForbiddenToken(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Not authorized",
            description=description,
            status_code=403,
        )


class UserNotExists(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Not found user",
            description=description,
            status_code=404,
        )


class InvalidToken(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Invalid token",
            description=description,
            status_code=401,
        )


class ErrorSendingEmail(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Error to send email",
            description=description,
            status_code=502,
        )


class RefundRequestError(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Refund Error",
            description=description,
            status_code=400,
        )


class PaymentAlreadyRegistered(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Error inserting on database",
            description=description,
            status_code=400,
        )


class RetrievePaymentError(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Error retrieving payment",
            description=description,
            status_code=400,
        )


class ExportRequestError(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="No payments found",
            description=description,
            status_code=400,
        )

class EntityNotExists(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="ENTITY_NOT_EXISTS",
            description=description,
            status_code=404,
        )