from os import getenv

from dotenv import load_dotenv


class SingletonMeta(type):
    """
    Singleton class for instantiate only one time the configs.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=SingletonMeta):
    """
    Loading .env file and other configs to be able to get it in all project.
    """

    load_dotenv()
    production_mode = getenv("PRODUCTION_MODE", default=True)
    SECRET_KEY = getenv("SECRET_KEY", default="secret")
    CACHE_LOCAL_MAXSIZE = getenv("CACHE_LOCAL_MAXSIZE", default=1000)
    CACHE_LOCAL_TIME = getenv("CACHE_LOCAL_TIME", default=36000)
    DATABASE_URL = getenv(
        "DATABASE_URL",
        default="postgresql+asyncpg://admin:admin@localhost:5432/backend",
    )
    DATABASE_TEST_URL = getenv(
        "DATABASE_TEST_URL",
        default="postgresql+asyncpg://admin:admin@localhost:5432/tests",
    )

    # Mailing service credentials
    HOST_MAIL = getenv(
        "HOST_MAIL", default="template.python.backend@gmail.com"
    )
    HOST_PASSWORD = getenv("HOST_PASSWORD", default="cibtlwfivfqsqssw")
    HOST_SERVER = getenv("HOST_SERVER", default="smtp.gmail.com")
    HOST_PORT = getenv("HOST_PORT", default=465)
    TEMPLATE_WELCOME = None
    TEMPLATE_RECOVERY = None
    TEMPLATE_PAYMENT = None

    # Google credentials
    GOOGLE_CLIENT_ID = getenv("GOOGLE_CLIENT_ID")
    PROJECT_ID = getenv("PROJECT_ID")
    AUTH_URI = getenv("AUTH_URI")
    TOKEN_URI = getenv("TOKEN_URI")
    AUTH_PROVIDER = getenv("AUTH_PROVIDER")
    CLIENT_SECRET = getenv("CLIENT_SECRET")
    REDIRECT_URIS = getenv("REDIRECT_URIS")

    # Payments credentials
    STRIPE_API_KEY = getenv(
        "STRIPE_API_KEY4312",
        "sk_test_51MX6kMEiusw8UqyEoLszLsLiKoCgIvViszoZaWBheqrTpcO\
        b6lS8YlhmjJqKe8M9qVkis1xDBGD7MvQVY9ejJ4Bo00i85J0Xo8"
    )
    BASE_URL = getenv("BASE_URL", "http://localhost:8000")
    SUCCESS_URL = getenv("SUCCESS_URL", "http://localhost:8000/payments/good")
    CANCEL_URL = getenv("CANCEL_URL", "http://localhost:8000/payments/cancel")
    EXPIRES_CHECKOUT = getenv("EXPIRES_CHECKOUT", 3600)
    ISO_CURRENCY_CODE = getenv("ISO_CURRENCY_CODE", "BRL")
