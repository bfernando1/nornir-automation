from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def reset_interfaces(task):
    interfaces = ["e1/4", "lo101-102"]
    cmd = "default int "
    for intf in interfaces:
        task.run(task=networking.netmiko_send_config, config_commands=f"{cmd}{intf}")


def reset_map(task):
    mapping = [
        "ip prefix-list PL_BGP_BOGUS",
        "ip prefix-list PL_BGP_Loopback101",
        "route-map RM_BGP_BOGUS",
        "route-map RM_BGP_NXOS2_Peer",
    ]
    for maps in mapping:
        task.run(task=networking.netmiko_send_config, config_commands=f"no {maps}")


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="nxos1")
    int_agg_results = nr.run(task=reset_interfaces)
    print_result(int_agg_results)

    map_agg_results = nr.run(task=reset_map)
    print_result(map_agg_results)


if __name__ == "__main__":
    main()
