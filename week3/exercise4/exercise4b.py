#! /usr/bin/env python3

from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
import ipdb

nr = InitNornir(config_file="../../config.yaml")
eos_filt = F(groups__contains="eos")
nr = nr.filter(eos_filt)

results = nr.run(task=netmiko_send_command,
                 command_string="show interface status",
                 use_textfsm=True 
)

print_result(results)
