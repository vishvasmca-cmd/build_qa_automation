@echo off
echo ========================================
echo Setting up test automation project
echo ========================================

echo.
echo [1/3] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo.
echo [2/3] Installing dependencies...
pip install -r requirements.txt

echo.
echo [3/3] Installing Playwright browsers...
playwright install chromium

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env
echo 2. Edit config/test-data.json
echo 3. Run: pytest tests/e2e/ -v
echo.
