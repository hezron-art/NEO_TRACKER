@echo off
REM Activate virtual environment
call venv\Scripts\activate

REM Navigate to project root
cd %~dp0

REM Run ETL
python src\extract.py
python src\transform.py
python src\load.py

REM Run alerts
python src\alerts.py

REM Deactivate virtual environment
deactivate
