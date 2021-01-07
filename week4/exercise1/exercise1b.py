"""
Author: Bradley Fernando
Propose: Convert the uptime output into seconds

Usage:
    python exercise1b.py

Output:

    Working on cisco3:
    --------------------
    14305260
    
    Working on cisco4:
    --------------------
    19231140
    
    Working on arista2:
    --------------------
    41086800
    
    Working on arista4:
    --------------------
    55486800
    
    Working on arista1:
    --------------------
    55486800
    
    Working on arista3:
    --------------------
    55486800
    
    > > > > > > > > > >
    WARNING! srx2 rebooted 90 second(s) ago
    < < < < < < < < < <
    
    Working on nxos1:
    --------------------
    12320610
    
    Working on nxos2:
    --------------------
    12320107

"""
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from nornir.core.task import Result
from nornir.core.filter import F
import re

HOURS_SECONDS = 3600
DAY_SECONDS = 24 * HOURS_SECONDS
WEEK_SECONDS = 7 * DAY_SECONDS
YEAR_SECONDS = 365 * DAY_SECONDS

def parse_uptime(uptime_str):
    """
    Original solution from Napalm:
    ref: https://github.com/napalm-automation/napalm/blob/2.4.0/napalm/ios/ios.py#L894

    Extract the uptime string from the devices.

    Return the uptime in seconds as an integer.
    """
    # Initialize to zero
    (years, weeks, days, hours, minutes, seconds) = (0, 0, 0, 0, 0, 0)

    # IOS/NX-OS string output
    if " uptime is " in uptime_str:
        _, uptime_str = uptime_str.split(" uptime is")

    # EOS string output
    elif "Uptime: " in uptime_str:
        _, uptime_str = uptime_str.split("Uptime:")

    # JUNOS string output
    # System booted: 2020-06-18 16:18:53 PDT (28w6d 00:19 ago)
    # Artificially reboot 90s ago
    elif "System booted: " in uptime_str:
        uptime_str = "90 seconds"

    time_list = uptime_str.split(",")
    for element in time_list:
        if re.search("year", element):
            years = int(element.split()[0])         
        elif re.search("week", element):
            weeks = int(element.split()[0])         
        elif re.search("day", element):
            days = int(element.split()[0])         
        elif re.search("hour", element):
            hours = int(element.split()[0])         
        elif re.search("minute", element):
            minutes = int(element.split()[0])         
        elif re.search("second", element):
            seconds = int(element.split()[0])         
        
    uptime_sec = (
        (years * YEAR_SECONDS)
        + (weeks * WEEK_SECONDS)
        + (days * DAY_SECONDS)
        + (hours * 3600)
        + (minutes * 60)
        + (seconds)
    )
    return uptime_sec


def get_uptime(task):
    all_cmds = {
        "eos": "show version | inc Uptime",
        "ios": "show version | inc uptime",
        "junos": "show system uptime | match System",
        "nxos": "show version | inc uptime"
    }
    cmd = all_cmds[task.host.platform] 
    multi_result = task.run(task=netmiko_send_command, command_string=cmd)
    uptime_str = multi_result[0].result
    uptime_sec = parse_uptime(uptime_str)

    if uptime_sec < DAY_SECONDS:
        print()
        print('> ' * 10)
        print(f"WARNING! {task.host} rebooted {uptime_sec} second(s) ago")
        print('< ' * 10)
    else:
        print(f"\nWorking on {task.host}:") 
        print('-' * 20)
        print(f"{uptime_sec}")

      
print("\nGathering uptime from all devices...")

nr = InitNornir(config_file="../../config.yaml")
nr.run(task=get_uptime)
