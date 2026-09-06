from netmiko import ConnectHandler
from netmiko import NetmikoAuthenticationException
from netmiko import NetmikoTimeoutException
import os
from dotenv import load_dotenv

load_dotenv()

print("\nWelecome to ACL addition Program")

with open("/home/simba/Projects/clab/inputs/commands_list") as file:
    commands = file.read().splitlines()

with open("/home/simba/Projects/clab/inputs/devices_list") as file:
    devices = file.read().splitlines()

for switch in devices:
    try:
        device = {
            "device_type" : os.getenv('DEVICE_TYPE'),
            "host" : switch,
            "username" : os.getenv('DEVICE_USERNAME'),
            "password" : os.getenv('DEVICE_PASSWORD'),
            "port" : int(os.getenv("NETWORKING_PORT", 22))
        }

        print(f"\nConnecting to device {switch}")

        ssh_connect = ConnectHandler(**device)

        print(f"\nSuccessfully connected to device {switch}")

        enable = ssh_connect.enable()
    
        prompt = ssh_connect.find_prompt()

        print(f"\n{prompt}show ip access-list CONSOLE_ACL\n")

        pre_output = ssh_connect.send_command("show ip access-list CONSOLE_ACL")

        print(pre_output)

        print(f"\n{prompt}")

        output = ssh_connect.send_config_set(commands)

        print(output)

        print(f"\n{prompt}show ip access-list CONSOLE_ACL\n")

        post_output = ssh_connect.send_command("show ip access-list CONSOLE_ACL")

        print(post_output)

        save_config = ssh_connect.save_config()

        show_run = ssh_connect.send_command("show run")

        with open(f"/home/simba/Projects/clab/outputs/{device['host']}_output.txt", 'w') as file:
            file.write(show_run)

        print(f"Saved output to {device['host']}_output.txt")

        ssh_connect.disconnect()

    except NetmikoTimeoutException:
        print(f"Device { device['host'] } is not reachable")

    except NetmikoAuthenticationException:
        print(f"Authentication failed for { device['host'] }")