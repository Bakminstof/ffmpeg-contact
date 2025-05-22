@ECHO off

:: Windows 10

@SET "ENCODING=65001"
@SET "CURRENT_DIR=%~dp0"
@SET "SCRIPT_NAME=FFMPEG contact"

:: ===Colors===
:: ==Normal foreground colors==
@SET "NF_BLACK=[30m"
@SET "NF_RED=[31m"
@SET "NF_GREEN=[32m"
@SET "NF_YELLOW=[33m"
@SET "NF_MAGENTA=[35m"
@SET "NF_CAYN=[36m"
@SET "NF_WHITE=[37m"

:: ==Strong foreground colors==
@SET "SF_RED=[91m"
@SET "SF_GREEN=[92m"
@SET "SF_YELLOW=[93m"
@SET "SF_CAYN=[96m"

:: ==Normal background colors==
@SET "NB_CAYN=[46m"
@SET "NB_WHITE=[47m"

:: ==Styles==
@SET "RESET=[0m"
@SET "BOLD=[1m"

:: ===Utils===
@SET "LINE_LENGTH=80"
@SET "LINE_SYMBOL=-"
@SET "BORDER=%NF_YELLOW%%NB_WHITE%#!%RESET%"

:: Pre start
@CHCP %ENCODING% > nul

@TITLE %SCRIPT_NAME%
:: Start
::==============================================================================================================
@PUSHD "%CURRENT_DIR%"

@SET "PYTHON=%CURRENT_DIR%..\venv\python-3.12.10-embed-amd64\python.exe"
@SET "APP_ENTRYPOINT=main.py"

@SET "SOURCE_DIR=%CURRENT_DIR%source"
@SET "RESULT_DIR=%CURRENT_DIR%result"

@SET "TARGET_EXTENSION=3gp"

@PUSHD "%CURRENT_DIR%..\src\"

IF NOT EXIST "%SOURCE_DIR%" (
    @MKDIR "%SOURCE_DIR%"
)
IF NOT EXIST "%RESULT_DIR%" (
    @MKDIR "%RESULT_DIR%"
)

@FOR /F "USEBACKQ" %%D IN (`@DIR /B "%SOURCE_DIR%" ^| @FINDSTR /V ".gitkeep"`) DO (
    @CALL :print %SF_CAYN% "Обработка - %RESET%%NF_CAYN%%%D%RESET%" Print_border

    @MKDIR "%RESULT_DIR%\%%D"

    "%PYTHON%" "%APP_ENTRYPOINT%" -te %TARGET_EXTENSION% -s "%SOURCE_DIR%\%%D" -d "%RESULT_DIR%\%%D" -n "%%D.%TARGET_EXTENSION%"

    @CALL :print_line
)

@CALL :print %NF_BLACK%%NB_CAYN% " FINISH "

@POPD
@POPD

@PAUSE > nul
::==============================================================================================================
:: Stop

@EXIT /B 0

:: Functions
:print [color] [text] [if_border]
SETLOCAL
@SET "COLON=%SF_YELLOW%:%RESET%"

@IF [%~3] == [] (
  @ECHO %~1%~2%RESET%
) ELSE (
  @ECHO %BORDER% %~1%~2%RESET%%COLON%
)

ENDLOCAL
goto :eof


:check_error_level
@IF %ERRORLEVEL% == 0 (
  @CALL :print %SF_GREEN% OK
) ELSE (
  @CALL :print %SF_RED% Fail
)

goto :eof

:run_command [command]
%*

@CALL :check_error_level

goto :eof

:run_command_with_echo [command]
@ECHO %NF_BLACK%%NB_WHITE%Run command:%RESET% %*

@CALL :run_command %*

goto :eof

:run_command_with_line [command]
@CALL :run_command %*
@CALL :print_line

goto :eof

:print_line [length]
SETLOCAL ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

@SET "LINE=%LINE_SYMBOL%"

IF [%~1] == [] (
  @SET "LENGTH=%LINE_LENGTH%"
) ELSE (
  @SET "LENGTH=%~1"
)

FOR /L %%i in (1,1,%LENGTH%) DO (
  @SET LINE=!LINE!%LINE_SYMBOL%
)

@CALL :print %SF_YELLOW% %LINE%

ENDLOCAL
goto :eof

:check_exists [file]

IF NOT EXIST %~1 (
  @CALL :print %SF_RED% "Error. Не могу найти `%~1`"
  @TIMEOUT /T 6 > nul
  @EXIT 1
)

goto :eof

:check_admin
@NET SESSION >nul 2>&1

IF %ERRORLEVEL% EQU 0 (
    @CALL :print %SF_YELLOW% "Administrator PRIVILEGES Detected!"
) ELSE (
    @CALL :print %SF_RED% "NOT AN ADMIN!"
    @PAUSE > nul
    @EXIT 1
)

goto :eof
