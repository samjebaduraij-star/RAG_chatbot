@echo off
echo Starting Q&A Chatbot Frontend...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Set environment variables
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.template .env
    echo Please edit .env file with your API keys before running again.
    pause
    exit /b 1
)

REM Change to frontend directory
cd frontend

REM Start Streamlit app
echo Starting Streamlit application...
echo Open your browser to: http://localhost:8501
echo.
streamlit run app.py --server.port 8501 --server.address localhost

pause