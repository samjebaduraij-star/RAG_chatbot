# settings.py
# Description: Centralized settings and environment loader
# Dependencies: os
# Author: AI Generated Code
# Created: August 15, 2025

import os

class Settings:
    def __init__(self):
        self.APP_NAME = os.getenv("APP_NAME", "Intelligent Q&A Chatbot")
        self.APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
        self.DEBUG = os.getenv("DEBUG", "true").lower() == "true"
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "frontend/data/uploads")
        self.MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
        self.ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", "pdf,docx,txt,csv").split(',')
        self.SECRET_KEY = os.getenv("SECRET_KEY", "")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
        # ...other config vars
settings = Settings()