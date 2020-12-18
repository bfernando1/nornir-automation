#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Prints the hosts available when a filter is applied

Usage: 
    python exercise2a.py

Output:

    IOS hosts:
    --------------------
    {'cisco3': Host: cisco3, 'cisco4': Host: cisco4}
    
"""

import ipdb
from nornir import InitNornir
from nornir.core.filter import F

# Create a Nornir object 
nr = InitNornir(config_file="../config.yaml")
# ipdb.set_trace()

# Filter for devices in the ios group
filt = F(groups__contains="ios")
nr = nr.filter(filt)

print()
print("IOS hosts:")
print("-" * 20)
print(nr.inventory.hosts)
print()
