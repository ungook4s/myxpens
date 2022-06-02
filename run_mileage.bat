@ECHO OFF

@python -V

IF ERRORLEVEL 1 GOTO errorHandling
REM no error here, errolevel == 0

@python mileage.py

exit
:errorHandling

echo Python is not installed on this system. Please, install python.
PAUSE