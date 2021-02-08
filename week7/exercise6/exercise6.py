"""
Author: Bradley Fernando
Purpose: Connect to nxos device using ssh with Napalm.

Usage:
    python exercise6.py

Output:

    Napalm ssh connection:
    <napalm.nxos_ssh.nxos_ssh.NXOSSSHDriver object at 0x7feb8fbe5190>
    
    Netmiko connection:
    <netmiko.cisco.cisco_nxos_ssh.CiscoNxosSSH object at 0x7feb9024b210>
    
    Device prompt:
    nxos1#
"""


from nornir import InitNornir
from nornir.plugins.functions.text import print_result


def ssh_conn(task):
    napalm_conn = task.host.get_connection("napalm", task.nornir.config)
    netmiko_conn = napalm_conn.device
    prompt = netmiko_conn.find_prompt()

    print("\nNapalm ssh connection:")
    print(napalm_conn)
    print("\nNetmiko connection:")
    print(netmiko_conn)
    print("\nDevice prompt:")
    print(prompt)

    return prompt


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="nxos1")
    agg_result = nr.run(task=ssh_conn)
    print_result(agg_result)


if __name__ == "__main__":
    main()
