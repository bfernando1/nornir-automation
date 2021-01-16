from nornir import InitNornir
from nornir.plugins.tasks import data, text
import ipdb
from pprint import pprint

#def render_config(task, acl_template):
        
    #ipdb.set_trace()

def build_acl(task, file_data):
    full_config = []
    for acl_name, rules in file_data.items():
        for rule in rules:
            acl_config = """\
set firewall family inet filter {{ acl_name }} term {{ term_name }} from protocol {{ protocol }}
set firewall family inet filter {{ acl_name }} term {{ term_name }} from destination-port {{ port }}
set firewall family inet filter {{ acl_name }} term {{ term_name }} from destination-address {{ address }}
set firewall family inet filter {{ acl_name }} term {{ term_name }} then {{ state }}
"""

            rendered = task.run(task=text.template_string, 
                     template=acl_config,
                     acl_name=acl_name,
                     term_name=rule['term_name'],
                     protocol=rule['protocol'],
                     port=rule['destination_port'],
                     address=rule['destination_address'],
                     state=rule['state']
            ) 
            full_config.append(rendered)

    for line in full_config:
        print(line[0].result)
 
def load_file(task):
    file_data = task.run(task=data.load_yaml, file="acl.yaml")    
    file_data = file_data[0].result
    acl_config = task.run(task=build_acl, file_data=file_data)
    #task.run(task=render_config, acl_template=acl_config)

def main():
    nr = InitNornir(config_file="../../config.yaml")
    nr = nr.filter(name="srx2")
    nr.run(task=load_file) 
    
    
    
    
if __name__ == "__main__":
    main()
