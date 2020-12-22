#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Output any hosts that fail to complete a task. 

Usage:
    python exercise5b.py

Output:

    Hosts that failed the last task:
      - cisco3
    
    Failed hosts stored in Nornir data object:
      - {'cisco3'}

"""
import ipdb
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result


nr = InitNornir(config_file="../../config.yaml")

# Intentionally set aninvalid password on the host
nr.inventory.hosts["cisco3"].password = "bogus"

ios_filt = F(groups__contains="ios")
nr = nr.filter(ios_filt)

results = nr.run(task=netmiko_send_command,
            command_string="show ip int brief"
)

print_result(results)
print()
print(f"Hosts that failed the last task:")
for hosts in results.failed_hosts:
    print(f"  - {hosts}")
print()
print("Failed hosts stored in Nornir data object:")
print(f"  - {nr.data.failed_hosts}")
print()
