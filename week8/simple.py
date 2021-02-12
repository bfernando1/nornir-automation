from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_result
from nornir.core.task import Result
import ipdb

config_path = "nxos/"

def show_interfaces(task):
    cmd = "show ip int brief"
    int_brief = task.run(networking.netmiko_send_command,
                command_string=cmd,
                use_genie=True
    )
    result = int_brief[0].result
            
    # Check if zero interfaces configured
    if type(result) == str:
        changed = True
        result = "adding new interfaces"
    # Check if interfaces are configured correctly
    elif type(result) != str:
        int_checker_result = task.run(task=interface_checker, int_config=result)
        changed = int_checker_result.changed
        result = int_checker_result.result
    else:
        changed = False
        result = "no interface changes"
    return Result(host=task.host, result=result, changed=changed)


def interface_checker(task, int_config):
    changed = False
    result = "no interface changes"

    for intf in task.host.data["interfaces"]:
        check_interface = intf["int_name"]
        if check_interface in int_config['interface'] and \
            "admin-up" in int_config["interface"][check_interface]["interface_status"] and \
            intf["ip_address"] == int_config["interface"][check_interface]['ip_address']:
            pass 
        else:
            changed = True
            result = "correcting 1 or more interface configuration"
    return Result(host=task.host, changed=changed, result=result)
    

def render_int_config(task):
    rendered_interface = task.run(
        task=text.template_file, template="int.j2", path=config_path, **task.host
    ) 


def config_interface(task):
    config = task.run(task=render_int_config)
    config = config[-1].result
    config_interface = task.run(
        task=networking.napalm_configure, configuration=config
    )

def set_config_flags(task):
    show_prefix = task.run(task=networking.netmiko_send_command, 
                           command_string="show ip prefix-list"
    )
    show_map = task.run(task=networking.netmiko_send_command,
                        command_string="show route-map"
    )
    config_prefix = "ip prefix-list PL_BGP_BOGUS permit 1.1.1.1/32"
    config_map = "route-map RM_BGP_BOGUS"
    
    # Create bogus prefix-list if none exist
    if "PL_BGP" in show_prefix.result:
        pass
    else:
        task.run(task=networking.netmiko_send_config, config_commands=config_prefix)
    
    # Create bogus route-map if none exists 
    if "RM_BGP" in show_map.result:
        pass
    else:
        task.run(task=networking.netmiko_send_config, config_commands=config_map)
   
    # Add remaining base configs for bgp  
    bgp_base_config = task.run(
        task=text.template_file, template="base_config.j2", path=config_path, **task.host)
    bgp_base_config = bgp_base_config.result
    task.run(task=networking.napalm_configure, configuration=bgp_base_config)

def get_checkpoint(task):
    napalm_connect = task.host.get_connection("napalm", task.nornir.config)
    checkpoint = napalm_connect._get_checkpoint_file()
    task.host["checkpoint"] = checkpoint
   

def render_configs(task):

    bgp_config = task.run(
        task=text.template_file, template="bgp_config.j2", path=config_path, **task.host
    )
    prefix_config = task.run(
        task=text.template_file, template="prefix_list.j2", path=config_path, **task.host
    )
    map_config = task.run( 
        task=text.template_file, template="route_map.j2", path=config_path, **task.host
    )
    task.host["bgp_config"] = bgp_config.result
    task.host["map_config"] = prefix_config.result + map_config.result

    ipdb.set_trace()
    


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="nxos1")

    # Configure interfaces
    """
    check_int_results = nr.run(task=show_interfaces)
    for _, hosts in enumerate(nr.inventory.hosts):
        if check_int_results[hosts].changed:
            print(check_int_results[hosts].result)
            config_int_results = nr.run(task=config_interface)
            print_result(config_int_results)
        else:
            print_result(check_int_results)
    """
    # Set config flags
    
    flag_results = nr.run(task=set_config_flags)
    print_result(flag_results)
   

    # Retrieve checkpoint
    """
    nr.run(task=get_checkpoint)
    """ 
    nr.run(task=render_configs)
    
if __name__ == "__main__":
    main()
