#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Display how the hosts retrieves the timezone from inventory

Usage: 
    python3 exercise1b.py

Output:

          Host   Timezone
    ----------------------
       arista1        CET
       arista2        CET
       arista3        PST
"""

from nornir import InitNornir
import ipdb

nr = InitNornir(config_file="../config.yaml")

print("\n{:>10} {:>10}".format('Host','Timezone'))
print('-' * 22)
for host in nr.inventory.hosts:
    timezone = nr.inventory.hosts[host]['timezone']
    print("{:>10} {:>10}".format(host, timezone))
print()

