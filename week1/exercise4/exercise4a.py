#! /usr/bin/env python3

from nornir import InitNornir

def my_task(task):
    print()
    print("Hello")
    print()

nr = InitNornir()
nr.run(task=my_task)
