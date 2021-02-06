from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def transform_nornir(host):

    host.password = host['ansible_ssh_pass']

    # Mapping for Netmiko plugin
    netmiko_group_mapper = {
        "arista": "arista_eos",
        "cisco": "cisco_ios",
        "nxos": "cisco_nxos",
        "juniper": "juniper_junos"
    }
    netmiko_params = host.get_connection_parameters('netmiko')
    netmiko_params.platform = \
        netmiko_group_mapper.get(host.groups[0], "no_platform_id")
    if 'arista' in host.name:
        netmiko_params.extras['global_delay_factor'] = 2
    host.connection_options['netmiko'] = netmiko_params
    
    # Mapping for Naplam plugin
    napalm_group_mapper = {
        "arista": "eos",
        "cisco": "ios",
        "nxos": "nxos", 
        "juniper": "junos"
    }
    napalm_params = host.get_connection_parameters('napalm')
    napalm_params.platform = \
        napalm_group_mapper.get(host.groups[0], 'no_platform_id')
    if "nxos" in host.name:
        napalm_params.port = 8443
    host.connection_options['napalm'] = napalm_params  


def main():
    nr = InitNornir(config_file="config-b.yaml")
    nr = nr.filter(F(groups__contains="nxos"))

    agg_result = nr.run(
        task=networking.napalm_get, getters=['facts']
    )
    print_result(agg_result)


if __name__ == "__main__":
    main()
