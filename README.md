# Config-Backup-Scripts
Backup Automation Script
**
You can use .py files for backing up your cisco old switches and extreme switch config file to your TFTP server. 
(1) Store two python scripts (cisco-switch, extreme-switch), powershell code, batch file in same location. 
(2) Edit your desired address, available path inside script. 
(3) Modify the patch inside the task scheduler source. 

- Batch file intend to run two python files for config backup and powershell file for monitoring config files inside TFTP folder.
- Task scheduler file intend to define custom timestamp for running .bat file.
