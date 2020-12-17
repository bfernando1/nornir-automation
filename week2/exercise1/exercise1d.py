#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Prints out the number of workers configured when specifed in python         directly. 

Usage: 
    python exercise1d.py

Output:

num_workers: 15
 
"""
from nornir import InitNornir

nr = InitNornir(config_file="config.yaml", 
                core={"num_workers": 15}
)
print()
print(f"num_workers: {nr.config.core.num_workers}")
print()
