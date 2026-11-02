@echo off
rem Programa la busqueda diaria en Windows: todos los dias a las 8:00 am.
rem Si la computadora estaba apagada a esa hora, corre en cuanto se prenda.
cd /d "%~dp0"
where claude >nul 2>nul || (echo No encontre Claude Code en esta computadora. Instalalo antes. & pause & exit /b 1)
powershell -NoProfile -Command "$a = New-ScheduledTaskAction -Execute '%~dp0busqueda-diaria.bat' -WorkingDirectory '%~dp0'; $t = New-ScheduledTaskTrigger -Daily -At 8:00am; $s = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 2); Register-ScheduledTask -TaskName 'Camionetas - busqueda diaria' -Action $a -Trigger $t -Settings $s -Force | Out-Null"
if errorlevel 1 (echo No se pudo programar. Copia este mensaje y mandaselo a Claude. & pause & exit /b 1)
echo.
echo Listo: la busqueda corre todos los dias a las 8:00 am.
echo Para probarla ahora mismo, da doble clic en busqueda-diaria.bat
pause
