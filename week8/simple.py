from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_result
from nornir.core.task import Result
from ciscoconfparse import CiscoConfParse
from pathlib import Path
import ipdb
import re


CONFIG_PATH = "nxos/"
PRE_DEPLOY = "pre_deployment"
POST_DEPLOY = "post_deployment"


def show_interfaces(task):
    cmd = "show ip int brief"
    int_brief = task.run(
        networking.netmiko_send_command, command_string=cmd, use_genie=True
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
    result = ""

    for intf in task.host.data["interfaces"]:
        check_interface = intf["int_name"]
        if (
            check_interface in int_config['interface'] 
            and "admin-up" 
            in int_config["interface"][check_interface]["interface_status"] 
            and intf["ip_address"] 
            == int_config["interface"][check_interface]['ip_address']
        ):
            pass 
        else:
            changed = True
            result = "correcting 1 or more interface configuration"
    return Result(host=task.host, changed=changed, result=result)
    

def render_int_config(task):
    rendered_interface = task.run(
        task=text.template_file, template="int.j2", path=CONFIG_PATH, **task.host
    ) 


def config_interface(task):
    config = task.run(task=render_int_config)
    config = config[-1].result
    config_interface = task.run(
        task=networking.napalm_configure, configuration=config
    )

def set_config_flags(task):
    show_prefix = task.run(
        task=networking.netmiko_send_command, command_string="show ip prefix-list"
    )
    show_map = task.run(
        task=networking.netmiko_send_command, command_string="show route-map"
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
        task=text.template_file, 
        template="base_config.j2", 
        path=CONFIG_PATH, 
        **task.host
    )
    bgp_base_config = bgp_base_config.result
    task.run(task=networking.napalm_configure, configuration=bgp_base_config)
    
    
def get_checkpoint(task):
    napalm_connect = task.host.get_connection("napalm", task.nornir.config)
    checkpoint = napalm_connect._get_checkpoint_file()
    task.host["checkpoint"] = checkpoint

  
def save_backup(task, config_type):
    Path(f"{CONFIG_PATH}backups").mkdir(parents=True, exist_ok=True)     
    with open(f"{CONFIG_PATH}backups/{task.host}_checkpoint_{config_type}", "w") as f:
        f.write(task.host["checkpoint"])


def render_configs(task):
    bgp_rendered = task.run(
        task=text.template_file, template="bgp_config.j2", path=CONFIG_PATH, **task.host
    )
    prefix_rendered = task.run(
        task=text.template_file, template="prefix_list.j2", path=CONFIG_PATH, **task.host
    )
    map_rendered = task.run( 
        task=text.template_file, template="route_map.j2", path=CONFIG_PATH, **task.host
    )
    task.host["bgp_rendered"] = bgp_rendered.result.strip()
    task.host["prefix_rendered"] = prefix_rendered.result.strip()
    task.host["map_rendered"] = map_rendered.result.strip()


def merge_configs(task, search_str, rendered_conf):
    parse = CiscoConfParse(
        "nxos/backups/nxos1_checkpoint_pre_deployment", syntax="nxos", factory=True
    )
    parse_text = ""
    changed = False

    # Parse current config 
    for parent_OBJ in parse.find_objects(search_str):
        parse_text += f"\n{parent_OBJ.parent.text}"
        try:
            for child_OBJ in parent_OBJ.all_children:
                parse_text += f"\n{child_OBJ.text}"
        except AttributeError:
            pass 
    parse_text = parse_text.strip()
    
    # Comapare current config and rendered configs
    if parse_text == task.host[rendered_conf]:
        pass
    else:
        updated_config = re.sub(
            parse_text, task.host[rendered_conf], task.host["checkpoint"]
        ) 
        changed = True
        task.host["checkpoint"] = updated_config

    return Result(host=task.host, changed=changed)


def push_configs(task):
    with open(f"{CONFIG_PATH}backups/{task.host}_checkpoint_{POST_DEPLOY}") as f:
        cfg_file = f.read()

    check_config = task.run(
        task=networking.napalm_configure, 
        replace=True, 
        configuration=cfg_file, 
        dry_run=True
    )

    # Check for changes before replacing config
    if check_config[0].diff == "":
        pass
    else:
        push_config = task.run(
            task=networking.napalm_configure, replace=True, configuration=cfg_file
        )


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="nxos1")

    # Configure interfaces
    check_int_results = nr.run(task=show_interfaces)
    for _, hosts in enumerate(nr.inventory.hosts):
        if check_int_results[hosts].changed:
            print(check_int_results[hosts].result)
            config_int_results = nr.run(task=config_interface)
            print_result(config_int_results)
        else:
            print_result(check_int_results)

    # Set config flags
    flag_results = nr.run(task=set_config_flags)
    print_result(flag_results)
    
    # Get checkpoint 
    checkpoint_results = nr.run(task=get_checkpoint)
    print_result(checkpoint_results) 
    
    # Save config locally
    pre_deploy_config = nr.run(task=save_backup, config_type=PRE_DEPLOY)
    print_result(pre_deploy_config)

    # Render configs
    render_results = nr.run(task=render_configs)
    print_result(render_results)

    # Merge config
    merge_dict = [
        {"search": "RM_BGP\w+ permit|deny", "rendered": "map_rendered"},
        {"search": "PL_BGP.* permit|deny", "rendered": "prefix_rendered"},
        {"search": "router bgp 22", "rendered": "bgp_rendered"}
    ]
    for parse in merge_dict:
        merge_results = nr.run(
            task=merge_configs, 
            search_str=parse["search"], 
            rendered_conf=parse["rendered"],
        )
        print_result(merge_results)
    deploy_config_results = nr.run(task=save_backup, config_type=POST_DEPLOY)
    print_result(deploy_config_results)
    
    # Push configs
    push_config_results = nr.run(task=push_configs)  
    print_result(push_config_results)
    
    
if __name__ == "__main__":
    main()
