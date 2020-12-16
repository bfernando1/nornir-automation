#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Calls a Nornir task to print the dns values that have been set
         either on a hosts or defaults level. 

Usage: 
    python exercise5.py

Output:

    hostname: rtr1.sjc
    dns1: 8.8.8.8
    dns2: 1.0.0.1
    
    
    hostname: rtr2.sjc
    dns1: 1.1.1.1
    dns2: 1.0.0.1

"""

from nornir import InitNornir

def my_task(task):
    print()
    print(f"hostname: {task.host.hostname}")
    print(f"dns1: {task.host['dns1']}")
    print(f"dns2: {task.host['dns2']}")
    print()

nr = InitNornir()
nr.run(task=my_task)
