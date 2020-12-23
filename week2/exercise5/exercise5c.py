#! /usr/bin/env python3 
"""
Author: Bradley Fernando
Purpose: Attempts to run a task on all hosts using netmiko_send_command 
         plugin. Attempts to run the task again on failed hosts only
         after correcting the error. 
Usage: 
    python exercise5c.py

Output:
netmiko_send_command************************************************************
* cisco3 ** changed : False ****************************************************
vvvv netmiko_send_command ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv ERROR

</--snipped-->

paramiko.ssh_exception.AuthenticationException: Authentication failed.

During handling of the above exception, another exception occurred:
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
"""

import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result

nr = InitNornir(config_file="../../config.yaml")
ios_filt = F(groups__contains="ios")
nr = nr.filter(ios_filt)

# Intentionally set a invalid password
nr.inventory.hosts["cisco3"].password = "bogus"

results = nr.run(task=netmiko_send_command,
                 command_string="show ip int brief"
)
print_result(results)

# Clear the failed hosts from the connections table
try:
    nr.inventory.hosts["cisco3"].close_connections()
except ValueError:
    pass

# Correct the password
nr.inventory.hosts["cisco3"].password = os.environ["NORNIR_PASSWORD"]

# Only run the task on the failed host
results = nr.run(task=netmiko_send_command,
                 command_string="show ip int brief",
                 on_failed=True,
                 on_good=False
)
print_result(results)
