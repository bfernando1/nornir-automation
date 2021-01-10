"""
Author: Bradley Fernando
Propose: Checks for the requested vlan before configuring it making it 
         idempotent

Usage: 
    python exercise3b.py 5 mgmt

Output: 
    vlan_config*********************************************************************
    * arista1 ** changed : False ***************************************************
    vvvv vlan_config ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    No changes made
    ---- netmiko_send_command ** changed : False ----------------------------------- INFO
    5     mgmt                             active    Et5
    ^^^^ END vlan_config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_config
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from sys import argv
from nornir.core.task import Result

def vlan_config(task, vlan_id, vlan_name):
    config_cmds = [f"vlan {vlan_id}", f"name {vlan_name}"]
    
    # Verify config 
    show_cmds = f"show vlan | i {vlan_name}" 
    results = task.run(task=netmiko_send_command,
             command_string=show_cmds)
    #import ipdb; ipdb.set_trace() 
    if vlan_id in results[0].result.split() and \
       vlan_name in results[0].result.split():
        msg = "No changes made"
    else:
        task.run(task=netmiko_send_config, config_commands=config_cmds)
        msg = "Configurations sent"
    
    return Result(host=task.host, result=msg)

def main():
    nr = InitNornir(config_file="../../config.yaml")
    ios_eos_filt = F(groups__contains="nxos") | \
                   F(groups__contains="eos")
    nr = nr.filter(ios_eos_filt)
    
    script, vlan_id, vlan_name = argv

    results = nr.run(task=vlan_config,
                     vlan_id=vlan_id,
                     vlan_name=vlan_name,
                     num_workers=10
    )

    print_result(results) 

if __name__ == "__main__":
    main()

