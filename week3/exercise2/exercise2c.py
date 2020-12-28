#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Use Nornir to filter for devices in a group

Usage:
    python exercise2c.py

Output:

    Filtering for devices in the 'sfo' group:
    {'arista1': Host: arista1}

"""    
from nornir import InitNornir
from nornir.core.filter import F

nr = InitNornir(config_file="../config.yaml")
sfo_filt = F(groups__contains="sfo")
sfo_devices = nr.filter(sfo_filt)

print("\nFiltering for devices in the 'sfo' group:")
print(sfo_devices.inventory.hosts)
print()
#import ipdb; ipdb.set_trace()

