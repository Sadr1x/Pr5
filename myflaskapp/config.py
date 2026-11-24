"""Конфігурації Flask для розробки та розгортання."""

import os
from secrets import token_hex


class Config:
    SECRET_KEY = token_hex(32)
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    @property
    def SECRET_KEY(self):
        # Читаємо змінну під час створення додатка.
        return os.environ["FLASK_SECRET_KEY"]


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
