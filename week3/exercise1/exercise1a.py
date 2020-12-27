#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Output the inventory objects for a device

Usage:
    python3 exercise1a.py

Output:
    
    Data object for arista3:
    ----------------------------------------
    	role: AGG
    
    All recursive objects for arista3:
    ----------------------------------------
    	role: AGG
    	timezone: CET
    	state: WA
"""    

from nornir import InitNornir
from nornir.plugins.functions.text import print_result

nr = InitNornir(config_file="../config.yaml")
host = "arista3"
divider = "-" * 40

host_object = nr.inventory.hosts[host].data.items()
print(f"\nData object for {host}:")
print(divider)
for key, value in host_object:
    print(f"\t{key}: {value}")

all_object = nr.inventory.hosts[host].items()
print(f"\nAll recursive objects for {host}:")
print(divider)
for key, value in all_object:
    print(f"\t{key}: {value}")
print()
