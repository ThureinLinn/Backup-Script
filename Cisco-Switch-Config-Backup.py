from netmiko import ConnectHandler
from datetime import datetime
import logging
import re

# Setup logging
logging.basicConfig(
    filename="backup_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# List of switch IPs
switch_ips = ["192.168.*.*", "192.168.*.*",]      #Replace your Switch IPs

# Common credentials
username = "cisco"
password = "password"
tftp_ip = "192.168.*.*"                            #Replace your TFTP Server

for ip in switch_ips:
    switch = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
        "fast_cli": False
    }

    try:
        logging.info(f"Connecting to switch: {ip}")
        net_connect = ConnectHandler(**switch)

        # Save running-config to startup-config with confirmation
        save_output = net_connect.send_command_timing("write memory", delay_factor=2)

        # Handle confirmation prompt
        if "overwrite file" in save_output.lower():
            save_output += net_connect.send_command_timing("Y", delay_factor=2)

        logging.info(f"{ip} - Write memory output: {save_output}")

        # Check for success indicators
        if "building configuration" in save_output.lower() or "[ok]" in save_output.lower() or "copy complete" in save_output.lower():
            logging.info(f"{ip} - Write memory completed successfully.")
        else:
            logging.warning(f"{ip} - Write memory may have failed or returned unexpected output.")

        # Get hostname
        hostname_output = net_connect.send_command_timing("show run | include hostname")
        hostname_clean = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', hostname_output)
        hostname = hostname_clean.split()[-1].replace("#", "")

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{hostname}_Backup_{timestamp}.cfg"

        # Backup to TFTP
        command = f"copy startup-config tftp://{tftp_ip}/{filename}"
        output = net_connect.send_command_timing(command, delay_factor=2)

        # Handle TFTP confirmation if needed
        if "address or name of remote host" in output.lower():
            output += net_connect.send_command_timing(tftp_ip, delay_factor=2)
        if "destination filename" in output.lower():
            output += net_connect.send_command_timing(filename, delay_factor=2)

        net_connect.disconnect()

        # Log result
        if "copy operation was completed successfully" in output.lower():
            logging.info(f"{ip} - Backup successful: {filename}")
        else:
            logging.error(f"{ip} - Backup failed: {output}")

        print(f"{ip} - {output}")

    except Exception as e:
        logging.error(f"{ip} - Exception occurred: {str(e)}")
        print(f"{ip} - Error: {str(e)}")