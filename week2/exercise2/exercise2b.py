#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Performs a task that uses the Netmiko_send_command and output the object type of the 
         result. 
Usage: 
    python exercise2b.py

Output:
    Object type: <class 'nornir.core.task.AggregatedResult'>
"""

import ipdb
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command

# Create a Nornir object 
nr = InitNornir(config_file="../config.yaml")
# ipdb.set_trace()

# Filter for devices in the ios group
filt = F(groups__contains="ios")
nr = nr.filter(filt)

# Send command `show run | inc hostname` via Netmiko
my_results = nr.run(task=netmiko_send_command,
                 command_string="show run | inc hostname"
)

# ipdb.set_trace()

print()
print(f"Object type: {type(my_results)}")
print()



