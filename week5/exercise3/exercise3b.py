"""
Author: Bradley Fernando
Purpose: Loads a yaml file and generates a ACL rule-set for a juniper device.

Usage:
    python exercise3b.py

Output:
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
"""
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import data
import ipdb

def build_acl(task, elements):
    for key in elements[0].result:
        rule_name = key

    for index, rule_val in enumerate(elements[0].result[rule_name]):
        data = f"set firewall family inet filter {rule_name} term {rule_val['term_name']}"
        print(f"{data} from protocol {rule_val['protocol']}")
        print(f"{data} from destination-port {rule_val['destination_port']}")
        print(f"{data} from destination-address {rule_val['destination_address']}")
        print(f"{data} then {rule_val['state']}")

def load_config(task):
    in_yaml = task.run(task=data.load_yaml, file="my_acl.yaml")
    task.run(task=build_acl, elements=in_yaml) 

def main():
    nr = InitNornir(config_file="../../config.yaml")
    nr = nr.filter(name="srx2")
    agg_result = nr.run(load_config) 


if __name__ == "__main__":
    main()
