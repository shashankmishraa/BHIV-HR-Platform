@echo off
echo Setting up BHIV HR Platform virtual environment...

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install requirements for each service
echo Installing Gateway requirements...
pip install -r services\gateway\requirements.txt

echo Installing Portal requirements...
pip install -r services\portal\requirements.txt

echo Installing Client Portal requirements...
pip install -r services\client_portal\requirements.txt

echo Installing Agent requirements...
pip install -r services\agent\requirements.txt

echo Virtual environment setup complete!
echo To activate: venv\Scripts\activate
echo To deactivate: deactivate