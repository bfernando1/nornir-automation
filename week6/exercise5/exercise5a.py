from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result


def send_command(task):
    cmd_mapper = {
        "ios": "show clock",
        "eos": "show clock",
        "nxos": "show clock",
        "junos": "show system uptime"
    }
    cmd = cmd_mapper[f"{task.host.groups[0]}"]

    #import ipdb;ipdb.set_trace()    
    task.run(task=netmiko_send_command, command_string=cmd)
    

def main():
    nr = InitNornir(config_file="../../config.yaml")
    #nr = nr.filter(name="cisco3")
    agg_result = nr.run(task=send_command)
    print_result(agg_result)    


if __name__ == "__main__":
    main()
