import os
import uvicorn
from fastapi import FastAPI
from utils.starters.cors_starter import CorsDefiner
from utils.starters.middlewares_starter import MiddlewareDefiner
from utils.starters.routers_starter import RouterDefiner

def create_app():
    global_app = FastAPI()
    RouterDefiner().define_routers(app=global_app)
    MiddlewareDefiner().define_handlers(app=global_app)
    CorsDefiner().define_cors(app=global_app)
    return global_app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    app = create_app()
    uvicorn.run(app, host=host, port=port)
