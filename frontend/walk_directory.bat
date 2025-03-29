@echo off
setlocal enabledelayedexpansion

if "%1"=="" (
    set "rootDir=%CD%"
) else (
    set "rootDir=%1"
)

call :walkDir "%rootDir%" 0
goto :eof

:walkDir
set "dir=%1"
set "level=%2"

for /F "tokens=*" %%A in ('dir /B /A-D "%dir%"') do (
    call :printIndent %level%
    echo +---%%A
    call :printIndent %level%
    echo ^|   File contents:
    call :printIndent %level%
    echo ^|   --------------
    type "%dir%\%%A"
    echo.
    call :printIndent %level%
    echo ^|   --------------
    echo.
)

for /F "tokens=*" %%A in ('dir /B /AD "%dir%"') do (
    call :printIndent %level%
    echo +---[%%A]
    set /a nextLevel=%level%+1
    call :walkDir "%dir%\%%A" !nextLevel!
)

goto :eof

:printIndent
set "spaces=    "
for /L %%i in (1,1,%1) do (
    set "indent=!indent!!spaces!"
)
echo !indent!
goto :eof