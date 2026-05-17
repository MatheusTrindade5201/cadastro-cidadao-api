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
    def __init__(self, _description: str):
        descriptions = {
            "pt_br": f"Usuário ou senha invalidos",
            "en_us": f"Invalid username or password",
        }
        super().__init__(
            name="Authentication fail",
            descriptions=descriptions,
            status_code=401,
        )


class UnauthorizedAccess(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="INVALID_ACCESS", description=description, status_code=401
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


class AssociationAlreadyExists(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="ASSOCIATION_ALREADY_EXISTS",
            description=description,
            status_code=400,
        )


class InvalidStateUF(BaseInternalException):
    def __init__(self, uf: str):
        descriptions = {
            "pt_br": f"UF inválido informado: {uf}.",
            "en_us": f"Invalid UF informed: {uf}.",
        }
        super().__init__(
            name="INVALID_STATE_UF",
            descriptions=descriptions,
            status_code=400,
        )


class ExternalServiceFailure(BaseInternalException):
    def __init__(self):
        descriptions = {
            "pt_br": "Falha ao acessar serviço externo.",
            "en_us": "Failed to access external service",
        }
        super().__init__(
            name="EXTERNAL_SERVICE_FAILURE",
            descriptions=descriptions,
            status_code=400,
        )

class DuplicateEntryError(BaseInternalException):
    def __init__(self, field: str):
        descriptions = {
            "pt_br": f"Já existe um indivíduo cadastrado com este {field}",
            "en_us": f"There already is an individual with this {field}",
        }
        super().__init__(
            name="DUPLICATE_ENTRY_ERROR",
            descriptions=descriptions,
            status_code=400,
        )


class InvalidCityForState(BaseInternalException):
    def __init__(self, city: str, state_uf: str):
        descriptions = {
            "pt_br": f"Cidade {city} não encontrada para o estado informado: {state_uf}",
            "en_us": f"City {city} not found for given state: {state_uf}",
        }
        super().__init__(
            name="INVALID_CITY_FOR_STATE",
            descriptions=descriptions,
            status_code=400,

        )

class InvalidZipCode(BaseInternalException):
    def __init__(self, zip_code: str):
        descriptions = {
            "pt_br": f"CEP inválido: {zip_code}",
            "en_us": f"Invalid Zip Code: {zip_code}",
        }

        super().__init__(
            name="INVALID_CNPJ", descriptions=descriptions, status_code=400
        )

class InvalidCPF(BaseInternalException):
    def __init__(self, cpf: str):
        descriptions = {
            "pt_br": f"CPF inválido: {cpf}",
            "en_us": f"Invalid CPF: {cpf}",
        }

        super().__init__(
            name="INVALID_CPF", descriptions=descriptions, status_code=400
        )

class InvalidEmail(BaseInternalException):
    def __init__(self, email: str):
        descriptions = {
            "pt_br": f"email inválido: {email}",
            "en_us": f"Invalid email: {email}",
        }

        super().__init__(
            name="INVALID_EMAIL", descriptions=descriptions, status_code=400
        )


class ErrorSendingEmail(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="ERROR_SENDING_EMAIL",
            description=description,
            status_code=500,
        )


class DeveloperAlreadyExists(BaseInternalException):
    def __init__(self):
        descriptions = {
            "pt_br": "Já existe um desenvolvedor cadastrado com este e-mail.",
            "en_us": "A developer account with this email already exists.",
        }
        super().__init__(
            name="DEVELOPER_ALREADY_EXISTS",
            descriptions=descriptions,
            status_code=400,
        )


class ApiKeyAlreadyRevoked(BaseInternalException):
    def __init__(self):
        descriptions = {
            "pt_br": "Esta chave de API já foi revogada.",
            "en_us": "This API key has already been revoked.",
        }
        super().__init__(
            name="API_KEY_ALREADY_REVOKED",
            descriptions=descriptions,
            status_code=400,
        )


class InvalidApiKey(BaseInternalException):
    def __init__(self):
        descriptions = {
            "pt_br": "Chave de API inválida ou ausente.",
            "en_us": "Invalid or missing API key.",
        }
        super().__init__(
            name="INVALID_API_KEY",
            descriptions=descriptions,
            status_code=401,
        )


class MagicLinkExpired(BaseInternalException):
    def __init__(self):
        descriptions = {
            "pt_br": "Link de acesso expirado ou já utilizado.",
            "en_us": "Magic link has expired or was already used.",
        }
        super().__init__(
            name="MAGIC_LINK_EXPIRED",
            descriptions=descriptions,
            status_code=401,
        )

