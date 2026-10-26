@echo off
chcp 65001 >nul
setlocal
REM ==========================================================================
REM  Cai skill "louisyoga-reel-style1" cho Claude Code tren may Windows nay.
REM  Chep thu muc skill vao %USERPROFILE%\.claude\skills\ (dung cho MOI project,
REM  moi tai khoan Claude dang nhap tren may nay), cai thu vien Python, kiem tra may.
REM ==========================================================================
set "SRC=%~dp0louisyoga-reel-style1"
set "DST=%USERPROFILE%\.claude\skills\louisyoga-reel-style1"

if not exist "%SRC%\SKILL.md" (
  echo [LOI] Khong thay "%SRC%\SKILL.md". Hay chay file nay ngay trong thu muc Skilleditvideo_phongcach1_louisyoga.
  pause
  exit /b 1
)

echo.
echo  1/3  Chep skill vao %DST%
robocopy "%SRC%" "%DST%" /E /NFL /NDL /NJH /NJS /NP >nul
if errorlevel 8 (
  echo [LOI] Chep that bai.
  pause
  exit /b 1
)

echo  2/3  Cai thu vien Python (faster-whisper, numpy, onnxruntime, Pillow, PyAV ^<16)
python -m pip install --upgrade faster-whisper numpy onnxruntime Pillow "av>=11,<16"
if errorlevel 1 echo [CANH BAO] pip loi - kiem tra Python da cai va co trong PATH chua.

echo  3/3  Kiem tra may
python "%DST%\scripts\preflight.py"

echo.
echo  XONG. Dong va mo lai Claude Code, roi go:  /louisyoga-reel-style1
echo  Prompt mau: xem file PROMPT-BAT-DAU.txt
pause
