#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Filters the output for the gateway of Cisco and Arista devices using `show ip arp` and Netmiko

Usage: 
    python exercise3.py      

Output:
    Host: cisco3, Gateway: Internet 10.220.88.1 4 0062.ec29.70fe ARPA GigabitEthernet0/0/0
    Host: cisco4, Gateway: Internet 10.220.88.1 4 0062.ec29.70fe ARPA GigabitEthernet0/0/0
    Host: arista1, Gateway: 10.220.88.1 N/A 0062.ec29.70fe Vlan1, Ethernet1
    Host: arista2, Gateway: 10.220.88.1 N/A 0062.ec29.70fe Vlan1, Ethernet1
    Host: arista3, Gateway: 10.220.88.1 N/A 0062.ec29.70fe Vlan1, Ethernet1
    Host: arista4, Gateway: 10.220.88.1 N/A 0062.ec29.70fe Vlan1, Ethernet1

"""

import ipdb
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command

nr = InitNornir(config_file="../../config.yaml")

# Filter for devices in both ios and group.
ios_filt = F(groups__contains="ios")
eos_filt = F(groups__contains="eos")
nr = nr.filter(ios_filt | eos_filt)

# Send command `show ip arp` via Netmiko.
my_results = nr.run(task=netmiko_send_command,
                    command_string="show ip arp"
)

# Assume that 10.220.88.1 is the gateway for all devices. 
print()
for host, val in my_results.items():
    gateway = val.result.splitlines()[1].rsplit()
    print(f"Host: {host}, Gateway: {' '.join(gateway)}")
print()
