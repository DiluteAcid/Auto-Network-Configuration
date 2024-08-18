import netmiko
import requests
import json
from requests.auth import HTTPBasicAuth
import paramiko
import time

# Device connection details
device = {
    'device_type': 'cisco_xr',
    'host': 'sandbox-iosxr-1.cisco.com',
    'username': 'admin',
    'password': 'C1sco12345',  # Default password for DevNet sandbox
    'port': 22,  # SSH port
}

# API details
api_base_url = f"https://{device['host']}:443/restconf/data"  # Changed to port 443
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

def ssh_command_paramiko(command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(device['host'], port=device['port'], username=device['username'], password=device['password'], timeout=10)
        _, stdout, _ = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        ssh.close()
        return output
    except Exception as e:
        return f"Error executing command via SSH: {str(e)}"

def api_get_request(endpoint):
    try:
        response = requests.get(
            f"{api_base_url}/{endpoint}",
            auth=HTTPBasicAuth(device['username'], device['password']),
            headers=headers,
            verify=False,  # Disable SSL verification (not recommended for production)
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Error making API request: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Get device information via SSH
    print("Device information (via SSH):")
    print(ssh_command_paramiko("show version"))

    # Get interface information via RESTCONF API
    print("\nInterface information (via RESTCONF API):")
    interfaces = api_get_request("Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-xr/interface")
    print(json.dumps(interfaces, indent=2))

    # Example: Configure a loopback interface via SSH
    print("\nConfiguring loopback interface (via SSH):")
    config_commands = [
        'configure terminal',
        'interface loopback 100',
        'description Configured by Python',
        'ipv4 address 192.168.100.1 255.255.255.255',
        'commit',
        'end'
    ]
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(device['host'], port=device['port'], username=device['username'], password=device['password'], timeout=10)
        for command in config_commands:
            _, stdout, _ = ssh.exec_command(command)
            time.sleep(1)  # Give some time for each command to execute
        print("Configuration commands executed.")
    except Exception as e:
        print(f"Error configuring interface: {str(e)}")
    finally:
        ssh.close()

    # Verify the configuration
    print("\nVerifying loopback interface configuration:")
    print(ssh_command_paramiko("show run interface loopback 100"))
