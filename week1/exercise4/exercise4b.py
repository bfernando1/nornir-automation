#! /usr/bin/env python3

from nornir import InitNornir

def my_task(task):
    print()
    print("It's raining in San Francisco")
    print(f"hostname: {task.host.hostname}")
    print()

nr = InitNornir()
nr.run(task=my_task)
