from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def reset_interfaces(task):
    interfaces = ["e1/4", "lo101-102"]
    cmd = "default int "
    for intf in interfaces:
        task.run(task=networking.netmiko_send_config, config_commands=f"{cmd}{intf}")  


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="nxos1")
    agg_results = nr.run(task=reset_interfaces)
    print_result(agg_results) 


if __name__ == "__main__":
    main()
