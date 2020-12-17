#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Prints out the default number of workers currently configured

Usage: 
    python exercise1a.py

Output:

    num_workers: 20
    
"""
from nornir import InitNornir

nr = InitNornir()
print()
print(f"num_workers: {nr.config.core.num_workers}")
print()
