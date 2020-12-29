#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Uses Nornir's F filter to demonstrate the intersection capabilites

Usage:
    python exercise3c.py

Output:

    Filtered devices containing both the 'WAN' role and a specific wifi password
    {'arista2': Host: arista2}

"""    
from nornir import InitNornir
from nornir.core.filter import F
import ipdb

nr = InitNornir(config_file="../config.yaml")
role_wifi_filt = F(role__contains="WAN") & F(site_details__wifi_password__contains="racecar")
nr = nr.filter(role_wifi_filt)

print("\nFiltered devices containing both the 'WAN' role and a specific wifi password")
print(nr.inventory.hosts)
print()
