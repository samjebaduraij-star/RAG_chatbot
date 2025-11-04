@echo off
echo Setting up Q&A Chatbot Project Structure...
echo.

REM Create main directories
mkdir frontend 2>nul
mkdir backend 2>nul
mkdir shared 2>nul
mkdir logs 2>nul
mkdir docs 2>nul
mkdir tests 2>nul

REM Create frontend structure
mkdir frontend\src 2>nul
mkdir frontend\src\ui 2>nul
mkdir frontend\src\core 2>nul
mkdir frontend\src\services 2>nul
mkdir frontend\src\utils 2>nul
mkdir frontend\data 2>nul
mkdir frontend\data\uploads 2>nul
mkdir frontend\data\chat_history 2>nul
mkdir frontend\data\processed 2>nul

REM Create backend structure
mkdir backend\app 2>nul
mkdir backend\app\api 2>nul
mkdir backend\app\models 2>nul
mkdir backend\app\services 2>nul
mkdir backend\app\core 2>nul
mkdir backend\tests 2>nul

REM Create shared structure
mkdir shared\config 2>nul
mkdir shared\schemas 2>nul

REM Create Python files
type nul > frontend\app.py
type nul > frontend\src\__init__.py
type nul > frontend\src\ui\__init__.py
type nul > frontend\src\ui\chat_interface.py
type nul > frontend\src\ui\document_upload.py
type nul > frontend\src\ui\sidebar.py
type nul > frontend\src\core\__init__.py
type nul > frontend\src\core\chat_manager.py
type nul > frontend\src\core\document_processor.py
type nul > frontend\src\core\history_manager.py
type nul > frontend\src\services\__init__.py
type nul > frontend\src\services\gemini_client.py
type nul > frontend\src\services\embedding_service.py
type nul > frontend\src\utils\__init__.py
type nul > frontend\src\utils\file_utils.py
type nul > frontend\src\utils\text_utils.py
type nul > frontend\src\utils\validators.py

REM Create configuration files
type nul > .env
type nul > .env.template
type nul > requirements.txt
type nul > README.md
type nul > setup.py

echo.
echo Project structure created successfully!
echo.
echo Next steps:
echo 1. Edit .env.template with your configuration
echo 2. Copy .env.template to .env and add your API keys
echo 3. Run: pip install -r requirements.txt
echo 4. Run: run_frontend.bat
echo.
pause