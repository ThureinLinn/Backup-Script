@echo off
REM Run Python backup script in background
start "" "C:\Users\Administrator\AppData\Local\Programs\Python\Python313\python.exe" "D:\Backups\Switch-Config-Backup\Cisco-Switch-Config-Backup.py"

REM Run Python backup script in background
start "" "C:\Users\Administrator\AppData\Local\Programs\Python\Python313\python.exe" "D:\Backups\Switch-Config-Backup\SExtremeSwitch-Config-Backup.py"

REM Run PowerShell email alert script in background
start "" powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File "D:\Backups\Switch-Config-Backup\Monitor-TFTP-Backup-path.ps1"