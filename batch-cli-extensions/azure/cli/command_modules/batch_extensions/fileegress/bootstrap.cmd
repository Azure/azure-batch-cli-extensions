@echo off
powershell -NoProfile -ExecutionPolicy unrestricted -Command "(iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1')))"
SET PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin
powershell -NoProfile -ExecutionPolicy unrestricted -Command "choco feature enable -n=allowGlobalConfirmation"
powershell -NoProfile -ExecutionPolicy unrestricted -Command "choco install python2"
exit /B %errorlevel%