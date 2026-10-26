@echo off
chcp 65001 >nul
echo.
echo   CAI SKILL Duycongeditvideo_Buoc1 cho Claude Code (moi du an tren may nay)
echo.
set "DEST=%USERPROFILE%\.claude\skills\duycongeditvideo-buoc1"
robocopy "%~dp0duycongeditvideo-buoc1" "%DEST%" /E /NFL /NDL /NJH /NJS /XD __pycache__ >nul
if not exist "%DEST%\SKILL.md" (echo   LOI: chep that bai & pause & exit /b 1)
echo   Da chep skill vao: %DEST%
echo.
echo   Cai thu vien Python (faster-whisper, numpy)...
python -m pip install -q faster-whisper numpy
echo.
echo   Neu may co card NVIDIA, cai them de Whisper chay GPU (nhanh 5-10 lan):
echo      python -m pip install nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*"
echo   Chua co ffmpeg:   winget install Gyan.FFmpeg   (roi mo lai terminal)
echo.
python "%DEST%\scripts\preflight.py"
pause
