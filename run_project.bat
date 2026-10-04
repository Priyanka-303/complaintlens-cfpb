@echo off
setlocal
python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
python src\run_pipeline.py
if errorlevel 1 exit /b 1
python src\validate_data.py
if errorlevel 1 exit /b 1
python src\create_figures.py
if errorlevel 1 exit /b 1
python -m unittest discover -s tests -v
