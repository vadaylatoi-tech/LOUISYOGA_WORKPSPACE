@echo off
chcp 65001 >nul
REM Cai dong bo Louis Yoga workspace cho MAY MOI (chay 1 lan).
REM Can co truoc: Google Drive for desktop (dang nhap dung tai khoan), Git, Python.
REM Repo phai nam o D:\LOUGA_WORKSPACE:  git clone https://github.com/vadaylatoi-tech/LOUISYOGA_WORKPSPACE D:\LOUGA_WORKSPACE
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 (
  python "..\sync\dong_bo.py" cai-dat
) else (
  py "..\sync\dong_bo.py" cai-dat
)
pause
