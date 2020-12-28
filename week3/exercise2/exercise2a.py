#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Use Nornir filtering to get a single device

Usage:
    python exercise2a.py

Output:

    Filtering for device name 'arista1':
    {'arista1': Host: arista1}

"""

from nornir import InitNornir
import ipdb

nr = InitNornir(config_file="../config.yaml")

device_fil = nr.filter(name='arista1')
#ipdb.set_trace()
print(f"\nFiltering for device name 'arista1':")
print(device_fil.inventory.hosts)
print()
