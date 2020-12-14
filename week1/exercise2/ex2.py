#!/usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Uses a for-loop to print the inventory items in the host and group
         vars. 

Usage: 
    python ex2.py

Output:

rtr1
--------------------
hostname: rtr1.sjc
groups: ['ios']
platform: ios
username: admin
password: cisco
port: 22


rtr2
--------------------
hostname: rtr2.sjc
groups: ['ios']
platform: ios
username: admin
password: cisco
port: 22
"""
from nornir import InitNornir

nr = InitNornir()

for key,val in nr.inventory.hosts.items():
    print()
    print(val)
    print('-' * 20)
    print(f"hostname: {val.hostname}")
    print(f"groups: {val.groups}")
    print(f"platform: {val.platform}")
    print(f"username: {val.username}")
    print(f"password: {val.password}")
    print(f"port: {val.port}")
    print()
