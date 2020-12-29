#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Use Nornir's F filter with unions

Usage: 
    python exercise3b.py

Output:

    Filtered hosts in either the 'sea' or 'sfo' group
     - arista1
     - arista2
     - arista3

"""

from nornir import InitNornir
from nornir.core.filter import F
import ipdb

nr = InitNornir(config_file="../config.yaml")
site_filt = F(groups__contains="sea") | F(groups__contains="sfo")
nr = nr.filter(site_filt)

print("\nFiltered hosts in either the 'sea' or 'sfo' group")
for hosts in nr.inventory.hosts:
    print(f" - {hosts}")
print()


