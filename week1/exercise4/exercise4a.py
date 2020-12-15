#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Outputs a string for each item in hosts using Nornir run

Usage: 
    python exercise4a.py

Output:
    Hello
    Hello
"""
from nornir import InitNornir

def my_task(task):
    print("Hello")

nr = InitNornir()
nr.run(task=my_task)
