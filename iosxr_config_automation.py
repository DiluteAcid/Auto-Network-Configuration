import netmiko
import requests
import json
from requests.auth import HTTPBasicAuth

# Device connection details
device = {
    'device_type': 'cisco_xr',
    'host': 'sandbox-iosxr-1.cisco.com',
    'username': 'admin',
    'password': 'your_password_here',  # Replace with actual password
    'port': 22,  # SSH port
}

# API details
api_base_url = f"https://{device['host']}:830/restconf/data"
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

def ssh_command(command):
    try:
        with netmiko.ConnectHandler(**device) as conn:
            output = conn.send_command(command)
        return output
    except Exception as e:
        return f"Error executing command via SSH: {str(e)}"

def api_get_request(endpoint):
    try:
        response = requests.get(
            f"{api_base_url}/{endpoint}",
            auth=HTTPBasicAuth(device['username'], device['password']),
            headers=headers,
            verify=False  # Disable SSL verification (not recommended for production)
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Error making API request: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Get device information via SSH
    print("Device information (via SSH):")
    print(ssh_command("show version"))

    # Get interface information via NETCONF (using RESTCONF API)
    print("\nInterface information (via NETCONF/RESTCONF API):")
    interfaces = api_get_request("Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-xr/interface")
    print(json.dumps(interfaces, indent=2))

    # Example: Configure a loopback interface via SSH
    print("\nConfiguring loopback interface (via SSH):")
    config_commands = [
        'interface loopback 100',
        'description Configured by Python',
        'ipv4 address 192.168.100.1 255.255.255.255'
    ]
    with netmiko.ConnectHandler(**device) as conn:
        conn.config_mode()
        output = conn.send_config_set(config_commands)
        conn.exit_config_mode()
        print(output)

    # Verify the configuration
    print("\nVerifying loopback interface configuration:")
    print(ssh_command("show run interface loopback 100"))
