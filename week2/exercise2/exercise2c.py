#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Prints the object for cisco3 from the parent Netmik_send_command object

Usage:
    python exerice2c.py

Output:

    Object for cisco3:
    --------------------
    MultiResult: [Result: "netmiko_send_command"]
    
"""

import ipdb
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command

# Create a Nornir object 
nr = InitNornir(config_file="../../config.yaml")
# ipdb.set_trace()

# Filter for devices in the ios group
filt = F(groups__contains="ios")
nr = nr.filter(filt)

# Send command `show run | inc hostname` via Netmiko
my_results = nr.run(task=netmiko_send_command,
                 command_string="show run | inc hostname"
)

#ipdb.set_trace()

# Retrieve the results from cisco3
host_results = my_results['cisco3']

print()
print("Object for cisco3:")
print("-" * 20)
print(host_results)
print()


