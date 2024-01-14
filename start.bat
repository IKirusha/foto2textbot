@echo off

call %~dp0venv\Scripts\activate

set TOKEN=
python bot.py

pause
