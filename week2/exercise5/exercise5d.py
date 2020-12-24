#! /usr/bin/env python3

from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
import os
import ipdb

nr = InitNornir(config_file="../../config.yaml")
ios_filt = F(groups__contains="ios")
nr = nr.filter(ios_filt)

# Intentionally set a wrong password for cisco3
nr.inventory.hosts["cisco3"].password = "bogus"

print("\nRunning a task that's expected to fail for cisco3")
print("-" * 60)
results = nr.run(task=netmiko_send_command,
                 command_string="show ip int brief"
)
print_result(results)

# Close the connection for cisco3
try:
    nr.inventory.hosts["cisco3"].close_connections()
except ValueError:
    pass

# Set the correct password for cisco3
nr.inventory.hosts["cisco3"].password = os.environ["NORNIR_PASSWORD"]

print(f"\nFailed global hosts: {nr.data.failed_hosts}")
print(f"Failed task hosts: {results.failed_hosts}\n")
print("Re-run task on cisco3 only")
print("-" * 60)


# Rerun tasks on failed hosts
results = nr.run(task=netmiko_send_command,
                 command_string="show ip int brief",
                 on_failed=True,
                 on_good=False
)
print_result(results)

print(f"\nFailed global host: {nr.data.failed_hosts}")
print(f"Failed task hosts: {results.failed_hosts}\n")

print("Recovering failed global host... \n")
nr.data.recover_host("cisco3")
print(f"Check for failed global hosts: {nr.data.failed_hosts}\n")

