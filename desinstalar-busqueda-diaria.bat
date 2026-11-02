@echo off
rem Quita la busqueda diaria programada (por ejemplo, cuando ya compraste).
powershell -NoProfile -Command "Unregister-ScheduledTask -TaskName 'Camionetas - busqueda diaria' -Confirm:$false"
echo.
echo Listo: la busqueda diaria ya no va a correr.
pause
