@echo off
goto :init

:header
    echo This batch file assists in the creation of virtual environments
    echo within a folder into the current directory.
    echo.
    goto :eof

:usage
    echo USAGE:
    echo   %__BAT_NAME% -n[opt] -p[opt] "python.exe location indicator"
    echo.
    echo.  /?, --help          shows this help
    echo.  /v, --version       shows the version
    echo.  /e, --verbose       shows detailed output
    echo.  -n, --name string   specifies a different name to use for the virual environment
    echo.                      default: .venv
    echo.  -p                  the location indicator will be a full path to a python.exe
    echo.
    echo.  python.exe location indicator can be:
    echo.           numeric (Ex. 39, 311): should be a python version installed on your computer
    echo.                  default_path = %user_path%\AppData\Local\Programs\Python\PythonXX\python.exe
    echo.           full_path: full path to a python install of your choice.
    goto :eof

:version
    if "%~1"=="full" call :header & goto :eof
    echo %__VERSION%
    goto :eof

:missing_argument
    call :header
    call :usage
    echo.
    echo ****    MISSING "REQUIRED ARGUMENT"    ****
    echo.
    goto :eof

:init
    set "__NAME=%~n0"
    set "__VERSION=1.00"
    set "__YEAR=2024"

    set "__BAT_FILE=%~0"
    set "__BAT_PATH=%~dp0"
    set "__BAT_NAME=%~nx0"

    set "OptHelp="
    set "OptVersion="
    set "OptVerbose="

    set "mypath=%cd%"
    set "user_path=%USERPROFILE%"
    set "venv_name=.venv"
    set "use_path=no"
    set "py_location="
    set "py_path="

:parse
    if "%~1"=="" goto :validate

    if /i "%~1"=="/?"         call :header & call :usage "%~2" & goto :end
    if /i "%~1"=="-?"         call :header & call :usage "%~2" & goto :end
    if /i "%~1"=="--help"     call :header & call :usage "%~2" & goto :end

    if /i "%~1"=="/v"         call :version      & goto :end
    if /i "%~1"=="-v"         call :version      & goto :end
    if /i "%~1"=="--version"  call :version full & goto :end

    if /i "%~1"=="/e"         set "OptVerbose=yes"  & shift & goto :parse
    if /i "%~1"=="-e"         set "OptVerbose=yes"  & shift & goto :parse
    if /i "%~1"=="--verbose"  set "OptVerbose=yes"  & shift & goto :parse

    if /i "%~1"=="-n"         set "venv_name=%~2"  & shift & shift & goto :parse
    if /i "%~1"=="--name"     set "venv_name=%~2"  & shift & shift & goto :parse

    if /i "%~1"=="-p"         set "use_path=yes"  & shift & goto :parse
    if /i "%~1"=="--path"     set "use_path=yes"  & shift & goto :parse

    if not defined py_location  set "py_location="%~1"" & shift & goto :parse

    shift
    goto :parse

:validate
    if not defined py_location call :missing_argument & goto :end

:main
    if defined OptVerbose (
        echo DEBUG IS ON
        echo cd is set to %mypath%
        echo user_path is set to %user_path%
        echo use_path is set to %use_path%
        echo venv_name is set to %venv_name%
        echo py_location is set to %py_location% currently
    )

    IF %use_path%==yes (
        if defined OptVerbose (
            echo accessed use path for py location
        )
        set py_path=%py_location%
        goto :check_path
    )

    set py_location=%py_location:"=%
    set py_location=%py_location: =%

    if defined OptVerbose (
        echo accessed default install pathing
        echo py_location is %py_location% fff
    )

    set "py_path=%user_path%\AppData\Local\Programs\Python\Python%py_location%\python.exe"
    goto :check_path
    

    :check_path
    set py_path="%py_path:"=%"
    IF EXIST %py_path% (
        echo %py_path% was found
        echo attempting to create virtual environment
        goto :create_and_activate
    ) ELSE (
        echo %py_path% was not found
        echo virtual environment cannot be created
        goto :end
    )

    :create_and_activate
        call %py_path% -m venv %mypath%\%venv_name%
        IF EXIST %mypath%\%venv_name%\Scripts\activate.bat (
            call %mypath%\%venv_name%\Scripts\activate.bat
            echo environment created and venv activated
        ) ELSE (
            echo attempted environment creation but unable to activate venv
            goto :end
        )
        
        IF EXIST %mypath%\requirements.txt (
            echo requirements.txt found in cd, attempting package installs
            goto :run_requirements
        ) ELSE (
            echo no requirements.txt found in cd, not attempting package installs
            goto :end
        )

    :run_requirements
        call pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org"
        call pip install -r requirements.txt
        goto :end

:end