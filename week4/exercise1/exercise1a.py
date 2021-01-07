"""
Author: Bradley Fernando
Purpose: Gathers the uptime from all devices using a custom Nornir task.

Usage:
    python exercise1a.py

Output:

    Gathering uptime from all devices...
    
    Working on cisco3:
    ------------------------------------------------------------
    cisco3 uptime is 23 weeks, 4 days, 6 hours, 21 minutes
    
    Working on cisco4:
    ------------------------------------------------------------
    cisco4 uptime is 31 weeks, 5 days, 6 hours, 38 minutes
    
    Working on nxos1:
    ------------------------------------------------------------
    Kernel uptime is 142 day(s), 7 hour(s), 3 minute(s), 6 second(s)
    
    Working on nxos2:
    ------------------------------------------------------------
    Kernel uptime is 142 day(s), 6 hour(s), 54 minute(s), 40 second(s)
    
    Working on arista1:
    ------------------------------------------------------------
    Uptime:                 91 weeks, 4 days, 22 hours and 2 minutes
    
    Working on arista2:
    ------------------------------------------------------------
    Uptime:                 67 weeks, 6 days, 5 hours and 43 minutes
    
    Working on arista3:
    ------------------------------------------------------------
    Uptime:                 91 weeks, 4 days, 21 hours and 43 minutes
    
    Working on arista4:
    ------------------------------------------------------------
    Uptime:                 91 weeks, 4 days, 21 hours and 59 minutes
    
    Working on srx2:
    ------------------------------------------------------------
    System booted: 2020-06-18 16:18:53 PDT (28w6d 00:19 ago)

"""
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from nornir.core.task import Result
from nornir.core.filter import F

nr = InitNornir(config_file="../../config.yaml")

def get_uptime(task):
    all_cmds = {
        "eos": "show version | inc Uptime",
        "ios": "show version | inc uptime",
        "junos": "show system uptime | match System",
        "nxos": "show version | inc uptime"
    }
    cmd = all_cmds[task.host.platform] 
    task.run(task=netmiko_send_command, command_string=cmd)

print("\nGathering uptime from all devices...\n")
agg_result = nr.run(task=get_uptime)
for host, uptime in agg_result.items():
    print(f"Working on {host}:")
    print('-' * 60)
    print(f"{uptime[1].result.strip()}\n")
