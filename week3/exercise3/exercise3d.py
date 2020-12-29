#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Uses Nornirs F filter to demonstrate the intersection and not capabilities

Usage: 
    python exercise3d.py

Output:

    Filtered devices containing both the 'WAN' role and NOT a specific wifi password
    {'arista1': Host: arista1}

"""

from nornir import InitNornir
from nornir.core.filter import F
import ipdb

nr = InitNornir(config_file="../config.yaml")
role_wifi_filt = F(role__contains="WAN") & ~F(site_details__wifi_password__contains="racecar")
nr = nr.filter(role_wifi_filt)

print("\nFiltered devices containing both the 'WAN' role and NOT a specific wifi password")
print(nr.inventory.hosts)
print()
