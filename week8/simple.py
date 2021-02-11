from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_result
from nornir.core.task import Result
import ipdb


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
    config_path = f"{task.host.platform}/"
    rendered_interface = task.run(
        task=text.template_file, template="int.j2", path=config_path, **task.host
    ) 


def config_interface(task):
    config = task.run(task=render_int_config)
    config = config[-1].result
    config_interface = task.run(
        task=networking.napalm_configure, configuration=config
    )


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="nxos1")
    check_int_results = nr.run(task=show_interfaces)
    for _, hosts in enumerate(nr.inventory.hosts):
        if check_int_results[hosts].changed:
            print(check_int_results[hosts].result)
            config_int_results = nr.run(task=config_interface)
            print_result(config_int_results)
        else:
            print_result(check_int_results)


if __name__ == "__main__":
    main()
