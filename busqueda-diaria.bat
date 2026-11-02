@echo off
rem Busqueda diaria de camionetas: Claude Code revisa anuncios, busca unidades
rem nuevas, baja fotos y publica la pagina. Lo corre Windows cada manana.
cd /d "%~dp0"
if not exist "busqueda-diaria\registro" mkdir "busqueda-diaria\registro"
for /f %%d in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set HOY=%%d
echo Busqueda diaria %HOY% > "busqueda-diaria\registro\%HOY%.txt"
type "busqueda-diaria\instrucciones.md" | claude -p --permission-mode acceptEdits --allowedTools "Read" "Edit" "Write" "Glob" "Grep" "WebSearch" "WebFetch" "Bash(git:*)" "Bash(python:*)" "Bash(py:*)" "PowerShell(git:*)" "PowerShell(python:*)" "PowerShell(py:*)" >> "busqueda-diaria\registro\%HOY%.txt" 2>&1
echo Termino con codigo %ERRORLEVEL% >> "busqueda-diaria\registro\%HOY%.txt"
