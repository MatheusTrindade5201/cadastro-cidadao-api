import os
import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from utils.starters.cors_starter import CorsDefiner
from utils.starters.middlewares_starter import MiddlewareDefiner
from utils.starters.rate_limiter_starter import limiter
from utils.starters.routers_starter import RouterDefiner


def create_app():
    global_app = FastAPI(
        title="Cadastro Cidadão API",
        swagger_ui_parameters={"persistAuthorization": True},
    )

    global_app.state.limiter = limiter
    global_app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    RouterDefiner().define_routers(app=global_app)
    MiddlewareDefiner().define_handlers(app=global_app)
    CorsDefiner().define_cors(app=global_app)

    def custom_openapi():
        if global_app.openapi_schema:
            return global_app.openapi_schema
        schema = get_openapi(
            title=global_app.title,
            version="1.0.0",
            routes=global_app.routes,
        )
        schema.setdefault("components", {}).setdefault("securitySchemes", {})
        schema["components"]["securitySchemes"]["ApiKeyAuth"] = {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
        }
        global_app.openapi_schema = schema
        return schema

    global_app.openapi = custom_openapi

    @global_app.get("/public/openapi.json", include_in_schema=False)
    async def get_public_openapi():
        full = global_app.openapi()
        public_paths = {
            k: v for k, v in full["paths"].items()
            if k.startswith("/public/") or k.startswith("/developer/")
        }
        return {
            **full,
            "paths": public_paths,
            "info": {**full["info"], "title": "Cadastro Cidadão — API Pública"},
        }

    return global_app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    app = create_app()
    uvicorn.run(app, host=host, port=port)
