@echo off
chcp 65001 >nul

set PROJECT_PATH=%~dp0
set SHORTCUT_NAME=TimeToWork
set SCRIPT_NAME=main.pyw
set VBS_TEMP=%TEMP%\makelink.vbs

for %%I in ("%PROJECT_PATH%") do set SHORT_PATH=%%~sI

echo Set WSHShell = WScript.CreateObject("WScript.Shell") > "%VBS_TEMP%"
echo Set oShellLink = WSHShell.CreateShortcut("%SHORT_PATH%%SHORTCUT_NAME%.lnk") >> "%VBS_TEMP%"
echo oShellLink.TargetPath = "%SHORT_PATH%venv\Scripts\pythonw.exe" >> "%VBS_TEMP%"
echo oShellLink.Arguments = "%SHORT_PATH%%SCRIPT_NAME%" >> "%VBS_TEMP%"
echo oShellLink.WorkingDirectory = "%SHORT_PATH%" >> "%VBS_TEMP%"
echo oShellLink.IconLocation = "%SHORT_PATH%icon.ico" >> "%VBS_TEMP%"
echo oShellLink.Save >> "%VBS_TEMP%"

cscript //nologo "%VBS_TEMP%"
del "%VBS_TEMP%"