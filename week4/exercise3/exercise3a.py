"""
Author: Bradley Fernando
Purpose: Takes in a vlan ID and vlan name as command-line 
         arguments and configures them on the devices. 

Usage:
    vlan_id: 
        int, the vlan number
    vlan_name:
        string, the name for the vlan 
    
    ex: python exercise3a.py 5 mgmt

Output:
    vlan_config*********************************************************************
    * arista1 ** changed : True ****************************************************
    vvvv vlan_config ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- netmiko_send_config ** changed : True ------------------------------------- INFO
    configure terminal
    arista1(config)#vlan 5
    arista1(config-vlan-5)#name mgmt
    arista1(config-vlan-5)#end
    arista1#
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

def vlan_config(task, vlan_id, vlan_name):
    config_cmds = [f"vlan {vlan_id}", f"name {vlan_name}"]
    
    task.run(task=netmiko_send_config,
                       config_commands=config_cmds)
  
    # Verify config 
    show_cmds = f"show vlan | i {vlan_name}" 
    task.run(task=netmiko_send_command,
             command_string=show_cmds
    )

def main():
    nr = InitNornir(config_file="../../config.yaml")
    ios_eos_filt = F(groups__contains="eos") | \
                   F(groups__contains="nxos")
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

