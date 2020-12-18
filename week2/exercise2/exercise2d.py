#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Prints the Results objects from the AggregatedResult of the Netmiko task. 

Usage: 
    python exercise2d.py

Output:
    
    Host: cisco3
    Name: netmiko_send_command
    Result: hostname cisco3
    Failed: False
       
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

#ipdb.set_trace()

# Retrieve the results from cisco3
host_results = my_results['cisco3']
task_result = host_results[0]

print()
print(f"Host: {task_result.host}")
print(f"Name: {task_result.name}")
print(f"Result: {task_result.result}")
print(f"Failed: {task_result.failed}")
print()
