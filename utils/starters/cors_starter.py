from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


class CorsDefiner:
    def __init__(self):
        self.origins: List[str] = ["*"]

    def define_cors(self, app: FastAPI):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=self.origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
