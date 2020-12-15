#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Calls a Nornir task to print a string and the hostname included 
         in hosts group.  

Usage: 
    python exercise4b.py

Output:
        
    It's raining in San Francisco
    hostname: rtr1.sjc
    
    
    It's raining in San Francisco
    hostname: rtr2.sjc
    
"""

from nornir import InitNornir

def my_task(task):
    print()
    print("It's raining in San Francisco")
    print(f"hostname: {task.host.hostname}")
    print()

nr = InitNornir()
nr.run(task=my_task)
