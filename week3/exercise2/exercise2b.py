#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Use Nornir to stack filters and output the results

Usage:
    python exercise2b.py

Output:

    Filtering for devices with the 'WAN' role:
    {'arista1': Host: arista1, 'arista2': Host: arista2}
    
    
    Filtering for devices with the 'WAN' role and port 22:
    {'arista2': Host: arista2}

"""
    
from nornir import InitNornir
import ipdb

nr = InitNornir(config_file="../config.yaml")

wan_filter = nr.filter(role="WAN")
print("\nFiltering for devices with the 'WAN' role:")
print(wan_filter.inventory.hosts)
print()

wan_port_filter = wan_filter.filter(port=22)
print("\nFiltering for devices with the 'WAN' role and port 22:")
print(wan_port_filter.inventory.hosts)
print()
#ipdb.set_trace()
