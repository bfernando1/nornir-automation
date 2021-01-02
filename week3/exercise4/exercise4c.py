#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Build a custom dictionary using the results from 'show int status' and Nornir aggregated results

Usage:
    python exercise4c.py

Output:
    
    Results from 'show int status' on Arista devices:
    ------------------------------------------------------------
    {'arista1': {'Et1': {'status': 'connected', 'vlan': '1'},
                 'Et2': {'status': 'connected', 'vlan': '2'},
                 'Et3': {'status': 'connected', 'vlan': '3'},
                 'Et4': {'status': 'connected', 'vlan': '4'},
                 'Et5': {'status': 'connected', 'vlan': '5'},
                 'Et6': {'status': 'connected', 'vlan': '6'},
                 'Et7': {'status': 'connected', 'vlan': '7'}},
     'arista2': {'Et1': {'status': 'connected', 'vlan': '1'},
                 'Et2': {'status': 'connected', 'vlan': '2'},
                 'Et3': {'status': 'connected', 'vlan': '3'},
                 'Et4': {'status': 'connected', 'vlan': '4'},
                 'Et5': {'status': 'connected', 'vlan': '5'},
                 'Et6': {'status': 'connected', 'vlan': '6'},
                 'Et7': {'status': 'connected', 'vlan': '7'}},
     'arista3': {'Et1': {'status': 'connected', 'vlan': '1'},
                 'Et2': {'status': 'connected', 'vlan': '2'},
                 'Et3': {'status': 'connected', 'vlan': '3'},
                 'Et4': {'status': 'connected', 'vlan': '4'},
                 'Et5': {'status': 'connected', 'vlan': '5'},
                 'Et6': {'status': 'connected', 'vlan': '6'},
                 'Et7': {'status': 'connected', 'vlan': '7'}},
     'arista4': {'Et1': {'status': 'connected', 'vlan': '1'},
                 'Et2': {'status': 'connected', 'vlan': '2'},
                 'Et3': {'status': 'connected', 'vlan': '3'},
                 'Et4': {'status': 'connected', 'vlan': '4'},
                 'Et5': {'status': 'connected', 'vlan': '5'},
                 'Et6': {'status': 'connected', 'vlan': '6'},
                 'Et7': {'status': 'connected', 'vlan': '7'}}}
    
"""
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command
from pprint import pprint

nr = InitNornir(config_file="../../config.yaml")
eos_filt = F(groups__contains="eos")
nr = nr.filter(eos_filt)

results = nr.run(task=netmiko_send_command,
                 command_string="show interface status",
                 use_textfsm=True 
)

int_dict = {}
all_devices = {}

print(f"\nResults from 'show int status' on Arista devices:")
print('-' * 60)

for host in nr.inventory.hosts:
    # Store results for a single device
    device_dict = results[host].result
    for index, value in enumerate(device_dict):
        status = device_dict[index]['status']
        port = device_dict[index]['port']
        vlan = device_dict[index]['vlan']
        if status == 'connected': 
            # Build interface dictionary
            int_dict[port] = {'status': status, 'vlan': vlan}  
    # Build total devices dictionary
    all_devices[host] = int_dict 

pprint(all_devices)
print()
