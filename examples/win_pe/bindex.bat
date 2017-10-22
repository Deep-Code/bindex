@ECHO OFF
CLS
ECHO Current directory: %CD%
REM Extract propeties of a WinPE header from an executable file.
python ..\..\bindex.py -i c:\windows\system32\calc.exe -v -d .\win32pe.json -o .\result.json
