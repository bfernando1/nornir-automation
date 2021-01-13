"""
Author: Bradley Fernando
Purpose: Configures snmp on devices using data stored in inventory

Usage:
    python exercise1c.py

Output:
    snmp_config*********************************************************************
    * arista1 ** changed : True ****************************************************
    vvvv snmp_config ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- netmiko_send_config ** changed : True ------------------------------------- INFO
    configure terminal
    arista1(config)#snmp-server chassis-id 8765-arista1
    arista1(config)#end
    arista1#
    ^^^^ END snmp_config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    * arista2 ** changed : True ****************************************************
    vvvv snmp_config ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- netmiko_send_config ** changed : True ------------------------------------- INFO
    configure terminal
    arista2(config)#snmp-server chassis-id 8765-arista2
    arista2(config)#end
    arista2#
      1 from nornir import InitNornir
    ^^^^ END snmp_config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    * arista3 ** changed : True ****************************************************
    vvvv snmp_config ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- netmiko_send_config ** changed : True ------------------------------------- INFO
    configure terminal
    arista3(config)#snmp-server chassis-id 8765-arista3
    arista3(config)#end
    arista3#
    ^^^^ END snmp_config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    * arista4 ** changed : True ****************************************************
    vvvv snmp_config ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- netmiko_send_config ** changed : True ------------------------------------- INFO
    configure terminal
    arista4(config)#snmp-server chassis-id 8765-arista4
    arista4(config)#end
    arista4#
    ^^^^ END snmp_config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    * cisco3 ** changed : True *****************************************************
    vvvv snmp_config ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- netmiko_send_config ** changed : True ------------------------------------- INFO
    configure terminal
    Enter configuration commands, one per line.  End with CNTL/Z.
    cisco3(config)#snmp-server chassis-id 5309
    cisco3(config)#end
    cisco3#
    ^^^^ END snmp_config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    * cisco4 ** changed : True *****************************************************
    vvvv snmp_config ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- netmiko_send_config ** changed : True ------------------------------------- INFO
    configure terminal
    Enter configuration commands, one per line.  End with CNTL/Z.
    cisco4(config)#snmp-server chassis-id 5309
    cisco4(config)#end
    cisco4#
    ^^^^ END snmp_config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_config
import ipdb

def snmp_config(task):
    snmp_cmd = {
        "ios": f"snmp-server chassis-id {task.host['snmp_id']}",
        "eos": f"snmp-server chassis-id {task.host['snmp_id']}-{task.host}"
    }
    task.run(task=netmiko_send_config, 
             config_commands=snmp_cmd[task.host.platform],
    )
def main():
    nr = InitNornir(config_file="config.yaml")
    device_filter = F(groups__contains="ios") | F(groups__contains="eos")
    nr = nr.filter(device_filter)
    
    results = nr.run(snmp_config) 
    print_result(results)

if __name__ == "__main__":
    main()
