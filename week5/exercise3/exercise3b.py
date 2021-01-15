"""
Author: Bradley Fernando
Purpose: Loads a yaml file and generates a ACL rule-set for a juniper device.

Usage:
    python exercise3b.py

Output:
    --------------------------------------------------------------------------------
    set firewall family inet filter my_acl term rule1 from protocol tcp
    set firewall family inet filter my_acl term rule1 from destination-port 22
    set firewall family inet filter my_acl term rule1 from destination-address 1.2.3.4/32
    set firewall family inet filter my_acl term rule1 then accept
    set firewall family inet filter my_acl term rule2 from protocol tcp
    set firewall family inet filter my_acl term rule2 from destination-port 443
    set firewall family inet filter my_acl term rule2 from destination-address 1.2.3.4/32
    set firewall family inet filter my_acl term rule2 then accept
    set firewall family inet filter my_acl term rule3 from protocol tcp
    set firewall family inet filter my_acl term rule3 from destination-port 80
    set firewall family inet filter my_acl term rule3 from destination-address 1.2.3.4/32
    set firewall family inet filter my_acl term rule3 then discard
    --------------------------------------------------------------------------------
"""
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import data
import ipdb

def build_acl(task, elements):
    acl_config = []

    for acl_name, acl_rule in elements.items():
        for rule in acl_rule:
            data = f"set firewall family inet filter {acl_name} term {rule['term_name']}"
            acl_config.append(f"{data} from protocol {rule['protocol']}")
            acl_config.append(f"{data} from destination-port {rule['destination_port']}")
            acl_config.append(f"{data} from destination-address {rule['destination_address']}")
            acl_config.append(f"{data} then {rule['state']}")
   
    print('-' * 80) 
    for line in acl_config:
        print(line)
    print('-' * 80) 
    
def load_config(task):
    in_yaml = task.run(task=data.load_yaml, file="my_acl.yaml")
    in_yaml = in_yaml[0].result
    task.run(task=build_acl, elements=in_yaml) 

def main():
    nr = InitNornir(config_file="../../config.yaml")
    nr = nr.filter(name="srx2")
    agg_result = nr.run(load_config) 


if __name__ == "__main__":
    main()
