@echo off
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 goto run
where py >nul 2>nul
if %errorlevel%==0 goto runpy
echo.
echo   KHONG TIM THAY PYTHON TREN MAY NAY.
echo   Cai o https://www.python.org/downloads/
echo   (khi cai NHO TICK o "Add python.exe to PATH", roi mo lai cua so nay)
echo.
pause
exit /b 1
:run
python kiem-tra-moi-truong.py
goto end
:runpy
py kiem-tra-moi-truong.py
:end
pause
