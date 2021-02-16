from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
from nornir.core.task import Result
from ciscoconfparse import CiscoConfParse
from pathlib import Path
import ipdb
import re
import time


CONFIG_PATH = "nxos/"
TEMPLATES = f"{CONFIG_PATH}/templates/"
PRE_DEPLOY = "pre_deployment"
POST_DEPLOY = "post_deployment"


def show_interfaces(task):
    """
    Nornir task that gets the output from "show ip int brief" to see if 
    routed interfaces and loopbacks are present and configured correctly.
    Marks interfaces that have been altered from desired state.

    If an interface has been marked then the interface configurations get
    sent to the function interface_checker for further inspection.

    Args: 
        task: nornir task object

    """
    cmd = "show ip int brief"
    int_brief = task.run(
        networking.netmiko_send_command, command_string=cmd, use_genie=True
    )
    result = int_brief[0].result

    # Check if zero interfaces configured
    if type(result) == str:
        changed = True
        result = f"{task.host.name}: adding new interfaces"
    # Check if interfaces are configured correctly
    elif type(result) != str:
        int_checker_result = task.run(task=interface_checker, int_config=result)
        changed = int_checker_result.changed
        result = int_checker_result.result
    else:
        changed = False
        result = f"{task.host.name}: no interface changes"
    return Result(host=task.host, result=result, changed=changed)


def interface_checker(task, int_config):
    """
    Nornir task that compares the interface configuration against
    the host file in inventory. This function checks to make sure
    that the interface is:
        - admin-up
        - has the correct ip addresss

    Args:
        task: nornir task object
        int_config: The output of "show ip int brief" in a dictionary

    """
    changed = False
    result = ""

    for intf in task.host.data["interfaces"]:
        check_interface = intf["int_name"]
        if (
            check_interface in int_config["interface"]
            and "admin-up"
            in int_config["interface"][check_interface]["interface_status"]
            and intf["ip_address"]
            == int_config["interface"][check_interface]["ip_address"]
        ):
            pass
        else:
            changed = True
            result = f"{task.host.name}: correcting 1 or more interface configuration"
    return Result(host=task.host, changed=changed, result=result)


def render_int_config(task):
    """
    Nornir task that renders a jinja template and produce a interface 
    configuration with values from inventory.

    Args:
        nornir task object

    """
    task.run(
        task=text.template_file, template="int.j2", path=TEMPLATES, **task.host
    )


def config_interface(task):
    """
    Nornir task that uses Naplam to configure the interfaces on the host device.
    The rendered interface configurations are merged to the device. 

    Args:
        task: nornir task object

    """
    config = task.run(task=render_int_config)
    config = config[-1].result
    task.run(task=networking.napalm_configure, configuration=config)


def set_config_flags(task):
    """
    Nornir task to ensure that config markers or "flags" are present in the
    current configuration. 

    For prefix-lists, if a "PL_BGP_" isn't found in the output of "show ip prefix-list",
    then a bogus prefix list will be created. 

    For route-maps, if a "RM_BGP_" isn't found in the output of "show route-maps", 
    then a bogus route-map will be created. 
    
    Args:
        task: nornir task object

    """
    show_prefix = task.run(
        task=networking.netmiko_send_command,
        command_string="show ip prefix-list | i PL_BGP_",
    )
    show_map = task.run(
        task=networking.netmiko_send_command,
        command_string="show route-map | i RM_BGP_",
    )
    config_prefix = "ip prefix-list PL_BGP_BOGUS permit 1.1.1.1/32"
    config_map = "route-map RM_BGP_BOGUS"

    # Create bogus prefix-list if none exist
    if not show_prefix.result:
        task.run(task=networking.netmiko_send_config, config_commands=config_prefix)

    # Create bogus route-map if none exists
    if not show_map.result:
        task.run(task=networking.netmiko_send_config, config_commands=config_map)

    # Add remaining base configs for bgp
    bgp_base_config = task.run(
        task=text.template_file, template="base_config.j2", path=TEMPLATES, **task.host
    )
    bgp_base_config = bgp_base_config.result
    task.run(task=networking.napalm_configure, configuration=bgp_base_config)


def get_checkpoint(task):
    """
    Nornir task that retreives the current checkpoint from the device.

    Args:
        task: nornir task object

    """
    napalm_connect = task.host.get_connection("napalm", task.nornir.config)
    checkpoint = napalm_connect._get_checkpoint_file()
    task.host["checkpoint"] = checkpoint


def save_backup(task, config_type):
    """
    Nornir task that takes the current checkpoint and saves it locally. 

    Args:
        task: nornir task object
    
    """
    Path(f"{CONFIG_PATH}backups").mkdir(parents=True, exist_ok=True)
    with open(f"{CONFIG_PATH}backups/{task.host}_checkpoint_{config_type}", "w") as f:
        f.write(task.host["checkpoint"])


def render_configs(task):
    """
    Nornir task that uses jinja templating to renders configurations for:
        - bgp configurations
        - route-maps
        - prefix-lists 

    Args:
        task: nornir task object

    """
    bgp_rendered = task.run(
        task=text.template_file, template="bgp_config.j2", path=TEMPLATES, **task.host
    )

    prefix_rendered = task.run(
        task=text.template_file, template="prefix_list.j2", path=TEMPLATES, **task.host
    )

    map_rendered = task.run(
        task=text.template_file, template="route_map.j2", path=TEMPLATES, **task.host
    )

    task.host["bgp_rendered"] = bgp_rendered.result
    task.host["prefix_rendered"] = prefix_rendered.result
    task.host["map_rendered"] = map_rendered.result


def merge_configs(task, search_str, rendered_conf):
    """
    Nornir task to search and replace any configurations that deviate from the
    desired state. CiscoConfParse and used to find the config "flag" 
    and regex is used to update the config with rendered configurations.  

    Args:
        serach_str: regex used to search configurations
        rendered_conf: config to replace the current configurations
        task: nornir task object 
    
    """
    parse = CiscoConfParse(
        f"{CONFIG_PATH}backups/{task.host}_checkpoint_{PRE_DEPLOY}",
        syntax="nxos",
        factory=True,
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
    """
    Nornir task that deploys the updated config only if there were changes made.
    
    Args:
        task: nornir task object
    
    """
    with open(f"{CONFIG_PATH}backups/{task.host}_checkpoint_{POST_DEPLOY}") as f:
        cfg_file = f.read()

    check_config = task.run(
        task=networking.napalm_configure,
        replace=True,
        configuration=cfg_file,
        dry_run=True,
    )

    # Check for changes before replacing config
    if check_config[0].diff == "":
        pass
    else:
        push_config = task.run(
            task=networking.napalm_configure, replace=True, configuration=cfg_file
        )


def validate_bgp(task):
    """
    Nornir task that uses Napalm to retrieve the device output from 
    "show bgp ipv4 unicast neighbors" and determines if the peer is up" 

    Args: 
        task: nornir task object

    """
    bgp_result = task.run(task=networking.napalm_get, getters=["bgp_neighbors"])
    print("*" * 80)
    for peer in task.host["bgp"]["neighbors"]:
        bgp_peer = peer["remote_peer"]
        if not bgp_result.result["bgp_neighbors"]["global"]["peers"][bgp_peer]["is_up"]:
            print(f"Failed, BGP peer {bgp_peer} is not up...")
        else:
            print(f"Success, BGP peer {bgp_peer} is up!")
    print("*" * 80)
    print()


def main():
    nr = InitNornir(config_file="config.yaml")
    # nr = nr.filter(name="nxos1")
    nr = nr.filter(F(groups__contains="nxos"))

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
        {"search": "router bgp 22", "rendered": "bgp_rendered"},
    ]
    for parse in merge_dict:
        merge_results = nr.run(
            task=merge_configs,
            search_str=parse["search"],
            rendered_conf=parse["rendered"],
        )
        print_result(merge_results)

    # Save updated config to disk
    deploy_config_results = nr.run(task=save_backup, config_type=POST_DEPLOY)
    print_result(deploy_config_results)

    # Push configs
    push_config_results = nr.run(task=push_configs)
    print_result(push_config_results)

    # Validate BGP
    for i in range(5, 0, -1):
        time.sleep(1)
    nr.run(task=validate_bgp)


if __name__ == "__main__":
    main()
