#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Filters the output for the gateway of Cisco and Arista devices using `show ip arp` and Napalm

Usage: 
    python exercise4.py

Output:

    Host: cisco3, Gateway: {'interface': 'GigabitEthernet0/0/0', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 27.0}
    Host: cisco4, Gateway: {'interface': 'GigabitEthernet0/0/0', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 27.0}
    Host: arista1, Gateway: {'interface': 'Vlan1, Ethernet1', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 0.0}
    Host: arista2, Gateway: {'interface': 'Vlan1, Ethernet1', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 0.0}
    Host: arista3, Gateway: {'interface': 'Vlan1, Ethernet1', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 0.0}
    Host: arista4, Gateway: {'interface': 'Vlan1, Ethernet1', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 0.0}

"""

import ipdb
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import napalm_get
from pprint import pprint

nr = InitNornir(config_file="../../config.yaml")

# Filter for devices in both ios and group.
ios_filt = F(groups__contains="ios")
eos_filt = F(groups__contains="eos")
nr = nr.filter(ios_filt | eos_filt)

# Send command `show ip arp` via Napalm
my_results = nr.run(task=napalm_get,
                    getters=["arp_table"]
)

# Assume that 10.220.88.1 is the gateway for all devices. 
print()
for host, gw_host in my_results.items():
    gateway = gw_host.result["arp_table"][0]
    print(f"Host: {host}, Gateway: {gateway}")
print()
