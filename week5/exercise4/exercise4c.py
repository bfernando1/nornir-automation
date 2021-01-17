"""
Author: Bradley Fernando
Purpose: Stores the generated ACLs to the task's host object 

Purpose:
    python exercise4c.py

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
from nornir.plugins.tasks import data, text
import ipdb

def render_config(task, acl_rules):
    rendered = task.run(
        task=text.template_file, template="acl.j2", path=".", acl_rules=acl_rules
    ) 
    # Store the results to task.host
    task.host['acl'] = rendered[0].result 
    print(task.host['acl'])

def load_config(task):
    acl_struct = task.run(task=data.load_yaml, file="acl.yaml")
    acl_struct = acl_struct[0].result 
    task.run(task=render_config, acl_rules=acl_struct)

def main():
    nr = InitNornir(config_file="../../config.yaml")
    nr = nr.filter(name="srx2")
    nr.run(task=load_config)     


if __name__ == "__main__":
    main()
