import paramiko
import time

# Device connection details
device = {
    'hostname': 'your_device_ip_or_hostname',
    'username': 'your_username',
    'password': 'your_password',
    'port': 22,  # SSH port, usually 22
}

def send_command(channel, command, expect_string='#', timeout=5):
    channel.send(command + '\n')
    output = ''
    start_time = time.time()
    while True:
        if channel.recv_ready():
            output += channel.recv(1024).decode('utf-8')
            if expect_string in output:
                break
        if time.time() - start_time > timeout:
            raise Exception(f"Timeout waiting for '{expect_string}' after command '{command}'")
        time.sleep(0.1)
    return output

def configure_device(channel, commands):
    send_command(channel, 'configure terminal', expect_string='(config)#')
    for command in commands:
        output = send_command(channel, command, expect_string='(config')
        print(f"Executed: {command}")
        print(output)
    send_command(channel, 'commit')
    send_command(channel, 'end')

def main():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(**device, timeout=10, allow_agent=False, look_for_keys=False)

        channel = ssh.invoke_shell()
        channel.settimeout(20)

        print("Device information (via SSH):")
        print(send_command(channel, "show version"))

        print("\nConfiguring loopback interface (via SSH):")
        config_commands = [
            'interface loopback 100',
            'description Configured by Python Script',
            'ipv4 address 192.168.100.1 255.255.255.255',
        ]
        configure_device(channel, config_commands)

        print("\nVerifying loopback interface configuration:")
        print(send_command(channel, "show run interface loopback 100"))

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if ssh:
            ssh.close()

if __name__ == "__main__":
    main()
