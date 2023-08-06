def cmd():
    text = """
ECHO ECHO scoop reset python^> run.ps1>> run.CMD
ECHO ECHO pip install aithermal -q^>^> run.ps1 >> run.CMD
ECHO ECHO pip install aithermal -U -q ^>^> run.ps1 >> run.CMD
ECHO ECHO Write-Output("Compilation is running this may take a minute") ^>^> run.ps1 >> run.CMD
ECHO ECHO python -m aithermal.runner^>^> run.ps1 >> run.CMD

ECHO CLS >> run.CMD
ECHO @ECHO OFF>> run.CMD
ECHO SET ThisScriptsDirectory^=%%~dp0>> run.CMD
ECHO SET PowerShellScriptPath^=%%ThisScriptsDirectory%%run.ps1>> run.CMD
ECHO PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& '%%PowerShellScriptPath%%'">> run.CMD
ECHO DEL run.ps1 >> run.CMD
"""
    return text
