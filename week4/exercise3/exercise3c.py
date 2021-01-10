from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_config
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from sys import argv
from nornir.core.task import Result

def vlan_config(task, vlan_id, vlan_name):
    config_cmds = [f"vlan {vlan_id}", f"name {vlan_name}"]
    changed = False    
    failed = False
 
    # Verify config 
    show_cmds = f"show vlan | i {vlan_name}" 
    results = task.run(task=netmiko_send_command,
             command_string=show_cmds)
    #import ipdb; ipdb.set_trace() 
    if vlan_id in results[0].result.split() and \
       vlan_name in results[0].result.split():
        result = "No changes made"
    else:
        result = task.run(task=netmiko_send_config, 
                           config_commands=config_cmds)
        changed = True
    
    return Result(host=task.host, result=result, changed=changed, 
                  failed=failed)

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
    
    #import ipdb; ipdb.set_trace() 
    print_result(results) 

if __name__ == "__main__":
    main()

