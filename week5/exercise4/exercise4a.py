"""
Author: Bradley Fernando
Purpose: Use jinja2 template string to generate ACL rules from a yaml file

Usage:
    python exercise4a.py

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
from pprint import pprint

acl_template = """\
{% for acl_name, rules in acl_rules.items() %}
    {%- for rule in rules %}

{% set data = 'set firewall family inet filter ' + acl_name  + ' term ' + rule['term_name'] %}
{{ data }} from protocol {{ rule['protocol'] }}
{{ data }} from destination-port {{ rule['destination_port'] }}
{{ data }} from destination-address {{ rule['destination_address'] }}
{{ data }} then {{ rule['state'] }}
    {% endfor %}
{% endfor %}
"""

def build_acl(task, file_data):
    rendered = task.run(task=text.template_string, template=acl_template, acl_rules=file_data)
    print(rendered[0].result)

def load_file(task):
    file_data = task.run(task=data.load_yaml, file="acl.yaml")    
    file_data = file_data[0].result
    acl_config = task.run(task=build_acl, file_data=file_data)

def main():
    nr = InitNornir(config_file="../../config.yaml")
    nr = nr.filter(name="srx2")
    nr.run(task=load_file) 
    
if __name__ == "__main__":
    main()
