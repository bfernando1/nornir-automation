from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks import text, networking
from nornir.plugins.functions.text import print_result
import ipdb

def verify_interfaces(task):
    int_to_config = []
    
    # Check for interfaces that are already configured
    cmd = "show ip int brief"
    int_brief = task.run(task=networking.netmiko_send_command, 
                         command_string=cmd,
                         use_genie=True
                )
    int_brief = int_brief[0].result
    
    # If no interfaces configured, then go straight to rendering
    if type(int_brief) == str:
        INT_CONFIG = task.run(task=render_int_config)

    # Check if interface is configured and up. Otherwise mark interface for config
    else:
        for intf in task.host.data["interfaces"]:
            check_int = intf["int_name"]
            if check_int in int_brief['interface'] and \
                "admin-up" in int_brief['interface'][check_int]["interface_status"]:
                pass
            else:
                int_to_config.append(check_int) 
        INT_CONFIG = task.run(task=manual_config_int, int_to_config=int_to_config)
    
    return INT_CONFIG[-1].result

def manual_config_int(task, int_to_config):
    # Execute when interfaces are partially configured
    int_string = ""
    config_path = f"{task.host.platform}/"

    for intf in task.host.data['interfaces']:
        if intf['int_name'] in int_to_config:
            int_string += f"""interface {intf['int_name']}
  ip address {intf['ip_address']} {intf['subnet_mask']}
  no shut

"""
    return int_string


def render_int_config(task):
    # Execute when no interfaces are configured
    config_path = f"{task.host.platform}/"
    rendered_int = task.run(
        task=text.template_file, template="int.j2", path=config_path, **task.host
    ) 
    return rendered_int

def config_interfaces(task, config):
    config = config[task.host.name][-1].result
    task.run(task=networking.napalm_configure, configuration=config)

def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="nxos1")
    INT_CONFIG = nr.run(task=verify_interfaces)
    #int_to_config = nr.run(task=verify_interfaces)
    #int_to_config = int_to_config['nxos1'][0].result
    #INT_CONFIG = nr.run(task=manual_config_int, int_to_config=int_to_config) 
    int_result = nr.run(task=config_interfaces, config=INT_CONFIG)
    print_result(int_result)
    
    


if __name__ == "__main__":
    main()
