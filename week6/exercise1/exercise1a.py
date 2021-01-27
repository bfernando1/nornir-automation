"""
Author: Bradley Fernando
Purpose: Display that a Nornir task will successfully run when sending a 
         invalid command.

Usage:
    python exercise1a.py

Output:
    send_command********************************************************************
    * srx2 ** changed : False ******************************************************
    vvvv send_command ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- netmiko_send_command ** changed : False ----------------------------------- INFO
    Disabling complete-on-space
    
    ---- netmiko_send_command ** changed : False ----------------------------------- INFO
    ^
    syntax error, expecting <command>.
    
    ^^^^ END send_command ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
import ipdb

def send_command(task):
    
    task.run(task=netmiko_send_command, 
             command_string="set cli complete-on-space off"
    )
    task.run(task=netmiko_send_command, command_string="show ip interface")
    
    

def main():
    nr = InitNornir(config_file="../../config.yaml")    
    nr = nr.filter(name="srx2")
    agg_result = nr.run(task=send_command)
    print_result(agg_result)
    
if __name__ == "__main__":
    main()
