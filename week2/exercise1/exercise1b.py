#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Prints out the number of workers configured when a config.yaml 
         file is introduced. 

Usage: 
    python exercise1b.py

Output:

    num_workers: 5
 
"""
from nornir import InitNornir

nr = InitNornir(config_file="config.yaml")
print()
print(f"num_workers: {nr.config.core.num_workers}")
print()
