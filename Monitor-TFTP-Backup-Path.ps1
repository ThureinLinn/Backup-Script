# === SMTP Variables ===
$name = 'Switch_Config_Backup'
$smtpServer = "testi.mail.protection.outlook.com"				# change your smtp server domain
$smtpPort = 25
$from = "testit@abc.com"										# change your sender address
$to = "notice@abc.com"											# change your receiver address
$subject = "[Backup Status] $name - $(Get-Date -Format yyyy-MM-dd)"

# === TFTP Folder Monitoring ===
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = "C:\Program Files\Tftpd64\BackupLog"			# change the path you want to monitor for config files
$watcher.Filter = "*.cfg"
$watcher.EnableRaisingEvents = $true
$watcher.IncludeSubdirectories = $false

Write-Host "Monitoring TFTP folder for new backups..."

# === Register Event Handler ===
$action = {
    $fileName = $Event.SourceEventArgs.Name
    $fullPath = Join-Path $watcher.Path $fileName
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    Write-Host "New backup file detected: $fileName"

    # Email body
    $body = @"
Backup configuration file received from Cisco device.

Details:
- File Name: $fileName
- Tag: $name
- Received At: $timestamp
- Saved To: $fullPath

This is an automated notification.
"@

    # Send email with error handling
    try {
        Send-MailMessage -From $from -To $to -Subject $subject -Body $body -SmtpServer $smtpServer -Port $smtpPort
        Write-Host "Email sent successfully for $fileName"
    } catch {
        Write-Host "ERROR sending email for $fileName ${_}"
    }
}

# Register the event
Register-ObjectEvent -InputObject $watcher -EventName Created -Action $action | Out-Null

# Keep script alive and process events
while ($true) {
    Start-Sleep -Seconds 1
}