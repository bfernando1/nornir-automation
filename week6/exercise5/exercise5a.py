"""
Author: Bradley Fernando
Purpose: Runs a task that collects the time status from all devices.

Usage:
    python exercise5c.py

Output:

    <!-- Trimmed to a single device for brevity -->

    * srx2 ** changed : False ******************************************************
    vvvv send_command ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- netmiko_send_command ** changed : False ----------------------------------- INFO
    
    Current time: 2021-02-03 10:48:04 PST
    System booted: 2020-06-18 16:18:53 PDT (32w5d 19:29 ago)
    Protocols started: 2020-06-18 16:21:50 PDT (32w5d 19:26 ago)
    Last configured: 2021-02-02 04:16:15 PST (1d 06:31 ago) by pyclass
    10:48AM  up 229 days, 19:29, 1 user, load averages: 0.09, 0.07, 0.02
    
    ^^^^ END send_command ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
""" 

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result


def send_command(task):
    cmd_mapper = {
        "ios": "show clock",
        "eos": "show clock",
        "nxos": "show clock",
        "junos": "show system uptime"
    }
    cmd = cmd_mapper[f"{task.host.groups[0]}"]
    task.run(task=netmiko_send_command, command_string=cmd)


def main():
    nr = InitNornir(config_file="../../config.yaml")
    agg_result = nr.run(task=send_command)
    print_result(agg_result)


if __name__ == "__main__":
    main()
