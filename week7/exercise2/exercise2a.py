from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command


def transform_nornir(host):
    # Mapping for Netmiko plugin
    group_mapper = {
        "arista": "arista_eos",
        "cisco": "cisco_ios",
        "nxos": "cisco_nxos",
        "juniper": "juniper_junos"
    }
    host.password = host['ansible_ssh_pass']
    netmiko_params = host.get_connection_parameters('netmiko')
    netmiko_params.platform = \
        group_mapper.get(host.groups[0], "no_platform_id")
    if 'arista' in host.name:
        netmiko_params.extras['global_delay_factor'] = 2
    host.connection_options['netmiko'] = netmiko_params


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(~F(name='localhost'))
    agg_result = nr.run(
        task=netmiko_send_command, command_string="show version"
    )
    print_result(agg_result)


if __name__ == "__main__":
    main()
