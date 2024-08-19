# Auto-Network-Configuration

## Overview

This project contains a Python script for automating network configuration tasks on Cisco IOS XR devices. It demonstrates basic network automation principles including establishing SSH connections, sending commands, and making configuration changes.

## Features

- SSH connection to Cisco IOS XR devices
- Retrieval of device information
- Configuration of loopback interfaces
- Verification of applied configurations
- Basic error handling and reporting

## Prerequisites

- Python 3.6 or higher
- Paramiko library
- Access to a Cisco IOS XR device (physical or virtual)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/iosxr-automation.git
   cd iosxr-automation
   ```

2. (Optional) Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Edit the `device` dictionary in `iosxr_config_automation.py` with your device's details:

```python
device = {
    'hostname': 'your_device_ip_or_hostname',
    'username': 'your_username',
    'password': 'your_password',
    'port': 22,  # SSH port, usually 22
}
```

**Note:** In a production environment, it's recommended to use environment variables or a secure vault for storing credentials.

## Usage

Run the script with:

```
python iosxr_config_automation.py
```

The script will:
1. Connect to the specified IOS XR device
2. Retrieve and display device information
3. Configure a loopback interface (Loopback100)
4. Verify the configuration

## Sample Output

```
Device information (via SSH):
Cisco IOS XR Software, Version 7.3.2
...

Configuring loopback interface (via SSH):
Executed: interface loopback 100
Executed: description Configured by Python Script
Executed: ipv4 address 192.168.100.1 255.255.255.255

Verifying loopback interface configuration:
interface Loopback100
 description Configured by Python Script
 ipv4 address 192.168.100.1 255.255.255.255
!
```

## Customization

To modify the loopback interface configuration, edit the `config_commands` list in the `main()` function:

```python
config_commands = [
    'interface loopback 100',
    'description Configured by Python Script',
    'ipv4 address 192.168.100.1 255.255.255.255',
]
```

## Contributing

Contributions to this project are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License.

## Disclaimer

This script is for educational and testing purposes only. Always test automation scripts in a safe environment before using them on production networks.

