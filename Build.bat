@echo off
REM Build script for TPadder
pyinstaller ^
    --clean ^
    --onefile ^
    --noconsole ^
    --workpath build ^
    --specpath build ^
    --distpath build ^
    --icon=../Icons/icon.ico ^
    --add-data "../Icons/icon.ico;Icons" ^
    main.py
echo Build complete. Executable is located in the build directory.
