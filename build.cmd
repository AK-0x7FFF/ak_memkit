@echo off

net session >nul 2>&1
if %errorLevel% neq 0 (
    runas /user:Administrator "cmd /k %0"
    exit
)

git submodule update --remote --recursive --merge

set projectDir=%cd%
set libsDir=%projectDir%/libs
set pyMeowDir=%libsDir%/pyMeow
set NeacControllerDir=%libsDir%/NeacController

cd %pyMeowDir%
call build.cmd < nul

cd %NeacControllerDir%/NeacDriver
pnputil -i -a "NeacSafe64.inf"

cd %NeacControllerDir%/NeacController
if not exist .venv (
    python -m venv .venv
)
call .\.venv\Scripts\activate.bat
call build.bat < nul
call .\.venv\Scripts\deactivate.bat

cd %projectDir%