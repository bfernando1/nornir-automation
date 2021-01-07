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

nr = InitNornir(config_file="../../config.yaml")
#junos_filt = F(groups__contains="junos")
#nr = nr.filter(junos_filt)

def get_uptime(task):
    all_cmds = {
        "eos": "show version | inc Uptime",
        "ios": "show version | inc uptime",
        "junos": "show system uptime | match System",
        "nxos": "show version | inc uptime"
    }
    cmd = all_cmds[task.host.platform] 
    task.run(task=netmiko_send_command, command_string=cmd)

def parse_uptime_ios(uptime_str):
    """
    Extract the uptime string from the given Cisco IOS Device.

    Return the uptime in seconds as an integer.
    """
    # Initialize to zero
    (years, weeks, days, hours, minutes) = (0, 0, 0, 0, 0)
    uptime_str = uptime_str.strip()
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
        
    uptime_sec = (
        (years * YEAR_SECONDS)
        + (weeks * WEEK_SECONDS)
        + (days * DAY_SECONDS)
        + (hours * 3600)
        + (minutes * 60)
    )
    return uptime_sec

 
def parse_uptime_nxos(uptime_str):
    """
    Extract the uptime string from the given NX-OS Device.

    Return the uptime in seconds as an integer.
    """
    # Initialize to zero
    (days, hours, minutes, seconds) = (0, 0, 0, 0, 0)
    uptime_str = uptime_str.strip()
    time_list = uptime_str.split(",")
    for element in time_list:
        if re.search("day", element):
            days = int(element.split()[0])         
        elif re.search("hour", element):
            hours = int(element.split()[0])         
        elif re.search("minute", element):
            minutes = int(element.split()[0])         
        elif re.search("second", element):
            seconds  = int(element.split()[0])         
        
    uptime_sec = (
        (days * DAY_SECONDS)
        + (hours * 3600)
        + (minutes * 60)
        + (seconds)
    )
    return uptime_sec

def parse_uptime_eos(uptime_str):
    """
    Extract the uptime string from the given Arista Device.

    Return the uptime in seconds as an integer.
    """
    # Initialize to zero
    (weeks, days, hours, minutes) = (0, 0, 0, 0)
    uptime_str = uptime_str.strip()
    time_list = uptime_str.split(",")
    for element in time_list:
        if re.search("weeks", element):
            weeks = int(element.split()[0])         
        elif re.search("days", element):
            days  = int(element.split()[0])         
        elif re.search("hour", element):
            hours = int(element.split()[0])         
        elif re.search("minute", element):
            minutes = int(element.split()[0])         
        
    uptime_sec = (
        (weeks * WEEK_SECONDS)
        + (days * DAY_SECONDS)
        + (hours * 3600)
        + (minutes * 60)
    )
    return uptime_sec

       
print("\nGathering uptime from all devices...\n")
agg_result = nr.run(task=get_uptime)
print("{:>10} {:>10}".format("Device", "Uptime (sec)"))
print(('-' * 10 + ' ') * 2)


for host, line in agg_result.items():
    raw_uptime = line[1].result
    # Uptime string for IOS devices
    if " uptime is " in raw_uptime and "Kernal" not in raw_uptime: 
        _, uptime_str = raw_uptime.split(" uptime is ")
        uptime = parse_uptime_ios(uptime_str)
        print("{:>10} {:>10}".format(host, uptime))

    # Uptime string in NXOS devices
    elif " uptime is " in raw_uptime and "Kernal" in raw_uptime: 
        _, uptime_str = raw_uptime.split(" uptime is ")
        uptime = parse_uptime_nxos(uptime_str)
        print("{:>10} {:>10}".format(host, uptime))

    # Uptime string in EOS devices
    elif "Uptime" in raw_uptime:
        _, uptime_str = raw_uptime.split("Uptime: ")
        uptime = parse_uptime_eos(uptime_str)
        print("{:>10} {:>10}".format(host, uptime))

    # Artifically reboot JUNOS devices
    elif "System booted" in raw_uptime:
        uptime = 90
    
    if uptime < DAY_SECONDS:
        print(f"\nWARNING! {host} rebooted {uptime} second(s) ago\n")
