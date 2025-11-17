@echo off
REM Windows Build Script for Test Pattern Player

echo ============================================
echo Building Test Pattern Player for Windows...
echo ============================================
echo.

REM Check if we're in the build directory
if not exist "build_windows.bat" (
    echo Error: Please run this script from the build\ directory
    exit /b 1
)

REM Go to parent directory
cd ..

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Creating...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Clean previous builds
echo Cleaning previous builds...
if exist "build\build" rmdir /s /q "build\build"
if exist "build\dist" rmdir /s /q "build\dist"
if exist "build\*.spec" del /q "build\*.spec"

REM Build application
echo.
echo Building Windows application...
pyinstaller --name "TestPatternPlayer" ^
            --windowed ^
            --onedir ^
            --icon=resources\icons\icon.ico ^
            --add-data "resources;resources" ^
            --add-data "data;data" ^
            --noconfirm ^
            main.py

REM Move build artifacts
move dist build\
move *.spec build\

echo.
echo ============================================
echo Build complete!
echo Application: build\dist\TestPatternPlayer\
echo ============================================
echo.
echo To run the app:
echo   build\dist\TestPatternPlayer\TestPatternPlayer.exe
echo.
echo To distribute, zip the entire TestPatternPlayer folder
echo.
pause
