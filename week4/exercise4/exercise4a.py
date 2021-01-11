"""
Author: Bradley Fernando
Purpose: Uses napalm_configure plugin to create vlans

Usage: 
    python exercise4a.py

Output:
    config_vlan*********************************************************************
    * arista1 ** changed : True ****************************************************
    vvvv config_vlan ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- napalm_configure ** changed : True ---------------------------------------- INFO
    @@ -21,7 +21,10 @@
     !
     clock timezone America/Los_Angeles
     !
    -vlan 2-7
    +vlan 2-4,6-7
    +!
    +vlan 5
    +   name mgmt
     !
     interface Ethernet1
        spanning-tree portfast
    ^^^^ END config_vlan ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import napalm_configure
from nornir.core.filter import F

def config_vlan(task, vlan_id, vlan_name):
    vlan_config = f"""vlan {vlan_id}
        name {vlan_name}"""

    task.run(task=napalm_configure, configuration=vlan_config)

def main():
    
    _vlan_id = "5"
    _vlan_name = "mgmt"

    nr = InitNornir(config_file="../../config.yaml")
    eos_ios_filt = F(groups__contains="nxos") | F(groups__contains="eos")
    nr = nr.filter(eos_ios_filt)    
    
    results = nr.run(task=config_vlan, 
                     vlan_id=_vlan_id, 
                     vlan_name=_vlan_name
    ) 
    print_result(results)
    

if __name__ == "__main__":
    main()
