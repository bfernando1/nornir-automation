#! /usr/bin/env python3
"""
Author: Bradley Fernando
Purpose: Prints the show command "show ip int brief" against the ios devices using the 
         netmiko_send_command plugin.

Usage:
    python exercise5a.py

Output:
    netmiko_send_command************************************************************
    * cisco3 ** changed : False ****************************************************
    vvvv netmiko_send_command ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    Interface              IP-Address      OK? Method Status                Protocol
    GigabitEthernet0/0/0   10.220.88.22    YES NVRAM  up                    up
    GigabitEthernet0/0/1   unassigned      YES unset  administratively down down
    GigabitEthernet0/1/0   unassigned      YES unset  down                  down
    GigabitEthernet0/1/1   unassigned      YES unset  down                  down
    GigabitEthernet0/1/2   unassigned      YES unset  down                  down
    GigabitEthernet0/1/3   unassigned      YES unset  down                  down
    Virtual-Access1        unassigned      YES unset  down                  down
    Vlan1                  unassigned      YES unset  up                    down
    ^^^^ END netmiko_send_command ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    * cisco4 ** changed : False ****************************************************
    vvvv netmiko_send_command ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    Interface              IP-Address      OK? Method Status                Protocol
    GigabitEthernet0/0/0   10.220.88.23    YES NVRAM  up                    up
    GigabitEthernet0/0/1   unassigned      YES NVRAM  administratively down down
    GigabitEthernet0/1/0   unassigned      YES unset  down                  down
    GigabitEthernet0/1/1   unassigned      YES unset  down                  down
    GigabitEthernet0/1/2   unassigned      YES unset  down                  down
    GigabitEthernet0/1/3   unassigned      YES unset  down                  down
    Vlan1                  unassigned      YES manual up                    down
    ^^^^ END netmiko_send_command ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result

nr = InitNornir(config_file="../../config.yaml")

ios_filt = F(groups__contains="ios")
nr = nr.filter(ios_filt)

results = nr.run(task=netmiko_send_command,
                 command_string="show ip int brief"
)

print_result(results)
