import argparse

import uvicorn
from fastapi import FastAPI

from utils.starters.cors_starter import CorsDefiner
from utils.starters.middlewares_starter import MiddlewareDefiner
from utils.starters.routers_starter import RouterDefiner

PARSER = argparse.ArgumentParser(description="FastAPI base options.")
PARSER.add_argument("--path")
PARSER.add_argument("--port")


def create_app():
    global_app = FastAPI()
    RouterDefiner().define_routers(app=global_app)
    MiddlewareDefiner().define_handlers(app=global_app)
    CorsDefiner().define_cors(app=global_app)
    return global_app


if __name__ == "__main__":
    # Retrieve optional arguments to change host and port
    arguments = PARSER.parse_args()
    api_port = arguments.port if arguments.port else 8000
    api_path = arguments.path if arguments.path else "0.0.0.0"
    # Start FastAPI application including all necessary routers and handlers
    app = create_app()
    uvicorn.run(app, host=api_path, port=api_port)
