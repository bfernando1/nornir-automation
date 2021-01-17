"""
Author: Bradley Fernando
Purpose: Retrieves a yaml file and sends it to a separate jinja template file
         to generate ACLs for a juniper device. 

Usage:
    python exercise4b.py

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
    print(rendered[0].result) 

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
