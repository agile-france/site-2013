@ECHO OFF

set PELICAN=pelican
set PELICANOPTS=

set BASEDIR=%~dp0
set INPUTDIR=%BASEDIR%\content
set OUTPUTDIR=%BASEDIR%\output
set CONFFILE=%BASEDIR%\pelicanconf.py
set PUBLISHCONF=%BASEDIR%\publishconf.py


if "%1" == "" goto help

if "%1" == "help" (
	:help
	@echo.Makefile for a pelican Web site
	@echo.
	@echo.Usage:
	@echo.   make html                        ^(re^)generate the web site
	@echo.   make clean                       remove the generated files
	@echo.   make regenerate                  regenerate files upon modification
	@echo.   make publish                     generate using production settings
	@echo.   make serve                       serve site at http://localhost:8000
	@echo.   make devserver                   start/restart develop_server.sh
	@echo.
	goto end
)

if "%1" == "html" (
	call :clean
	%PELICAN% %INPUTDIR% -o %OUTPUTDIR% -s %CONFFILE% %PELICANOPTS%
	if errorlevel 1 exit /b 1
	echo.Done
	goto end
)

if "%1" == "clean" (
	:clean
	for /d %%i in (%OUTPUTDIR%\*) do rmdir /q /s %%i
	del /q /s %OUTPUTDIR%\*
	goto end
)

if "%1" == "regenerate" (
	call :clean
	%PELICAN% -r %INPUTDIR% -o %OUTPUTDIR% -s %CONFFILE% %PELICANOPTS%
	if errorlevel 1 exit /b 1
	echo.Done
	goto end
)

if "%1" == "serve" (
	%comspec% /c "cd %OUTPUTDIR% && python -m SimpleHTTPServer"
	goto end
)

if "%1" == "devserver" (
	%BASEDIR%\develop_server.bat restart
	goto end
)

if "%1" == "publish" (
	%PELICAN% %INPUTDIR% -o %OUTPUTDIR% -s %PUBLISHCONF% %PELICANOPTS%
	goto end
)

call :help

:end
