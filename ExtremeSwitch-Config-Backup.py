from paramiko import SSHClient, AutoAddPolicy
from datetime import datetime
import time
import logging

# Setup logging
logging.basicConfig(
    filename="extreme_backup_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# List of switch IPs
switch_ips = ["192.168.*.*", "192.168.*.*"]           # Add your switch IPs

# Credentials and TFTP server
username = "cisco"
password = "password"
tftp_ip = "192.168.*.*"                                 # Add your TFTP Server

for ip in switch_ips:
    try:
        logging.info(f"Connecting to switch: {ip}")
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)

        remote = ssh.invoke_shell()
        time.sleep(1)
        remote.recv(1000)

        # Enter enable mode
        remote.send("en\n")
        time.sleep(1)
        remote.recv(1000)

        # Save config
        remote.send("write memory\n")
        time.sleep(1)
        remote.send("y\n")
        time.sleep(2)
        remote.recv(5000)

        # Get hostname
        remote.send("show running-config | include hostname\n")
        time.sleep(2)
        hostname_output = remote.recv(5000).decode("utf-8")
        hostname_line = [line for line in hostname_output.splitlines() if "hostname" in line.lower()]
        hostname = hostname_line[0].split()[1] if hostname_line else f"switch{ip.split('.')[-1]}"

        # Generate filename with hostname
        timestamp = datetime.now().strftime("%m%d%H%M")
        filename = f"{hostname}_{timestamp}.cfg"

        # Backup to TFTP
        remote.send(f"copy nvram:startup-config tftp://{tftp_ip}/{filename}\n")
        time.sleep(1)
        remote.send("y\n")
        time.sleep(5)
        output = remote.recv(10000).decode("utf-8")

        ssh.close()

        if "copy complete" in output.lower() or "success" in output.lower():
            logging.info(f"{ip} - Backup successful: {filename}")
            print(f"{ip} - Backup successful: {filename}")
        else:
            logging.error(f"{ip} - Backup may have failed: {output}")
            print(f"{ip} - Backup may have failed: {output}")

    except Exception as e:
        logging.error(f"{ip} - Exception occurred: {str(e)}")
        print(f"{ip} - Error: {str(e)}")