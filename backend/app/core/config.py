# config.py
# Description: Loads backend configuration from environment
# Dependencies: os
# Author: AI Generated Code
# Created: August 15, 2025

import os

class BackendConfig:
    HOST = os.getenv("BACKEND_HOST", "localhost")
    PORT = int(os.getenv("BACKEND_PORT", "8000"))
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    # ...other backend config

config = BackendConfig()