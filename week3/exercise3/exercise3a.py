#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Filter groups using F filters in Nornir

Usage:
    python exercise2a.py

Output:
    
    Filtered devices that are in the 'AGG' role
    {'arista3': Host: arista3}

"""
    
from nornir import InitNornir
from nornir.core.filter import F
import ipdb

nr = InitNornir(config_file="../config.yaml")
agg_filt = F(role__contains="AGG")
nr = nr.filter(agg_filt)

print("\nFiltered devices that are in the 'AGG' role")
print(nr.inventory.hosts)
print()
