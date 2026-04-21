@echo off
REM setup_task.bat — schedules birthday_reminder.py to run every day at 8:00 AM
REM Run this once as Administrator

SET SCRIPT_DIR=%~dp0
SET PYTHON=python
SET SCRIPT=%SCRIPT_DIR%birthday_reminder.py
SET TASK_NAME=BirthdayReminder

echo Setting up Windows Scheduled Task...
echo   Script   : %SCRIPT%
echo   Schedule : Every day at 8:00 AM
echo.

schtasks /create ^
  /tn "%TASK_NAME%" ^
  /tr "\"%PYTHON%\" \"%SCRIPT%\"" ^
  /sc daily ^
  /st 08:00 ^
  /f

IF %ERRORLEVEL% EQU 0 (
    echo.
    echo Successfully created task "%TASK_NAME%"
    echo It will run every day at 8:00 AM.
) ELSE (
    echo.
    echo Failed to create task. Try running this script as Administrator.
)

pause
