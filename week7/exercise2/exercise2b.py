"""
Author: Bradley Fernando
Purpose: Use transform function so that both Netmiko and Napalm will work with
         Ansible inventory. 

Usage:
    python exercise2b.py

Output:
napalm_get**********************************************************************
* nxos1 ** changed : False *****************************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'facts': { 'fqdn': 'nxos1.lasthop.io',
             'hostname': 'nxos1',
             'interface_list': [ 'mgmt0',
                                 'Ethernet1/1',
                                 'Ethernet1/2',
                                 'Ethernet1/3',
                                 'Ethernet1/4',
                                 'Ethernet1/5',
                            <!-- snipped -->
                                 'Ethernet1/127',
                                 'Ethernet1/128',
                                 'Vlan1'],
             'model': 'Nexus9000 9000v Chassis',
             'os_version': '9.2(3)',
             'serial_number': '9B2B28CMF9S',
             'uptime': 14909576,
             'vendor': 'Cisco'}}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""


from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def transform_nornir(host):

    host.password = host['ansible_ssh_pass']
    netmiko_params = host.get_connection_parameters('netmiko')
    napalm_params = host.get_connection_parameters('napalm')

    # Mapping for Netmiko plugin
    netmiko_group_mapper = {
        "arista": "arista_eos",
        "cisco": "cisco_ios",
        "nxos": "cisco_nxos",
        "juniper": "juniper_junos"
    }
    netmiko_params.platform = \
        netmiko_group_mapper.get(host.groups[0], "no_platform_id")
    if 'arista' in host.name:
        netmiko_params.extras['global_delay_factor'] = 2
    
    # Mapping for Napalm plugin
    napalm_group_mapper = {
        "arista": "eos",
        "cisco": "ios",
        "nxos": "nxos", 
        "juniper": "junos"
    }
    napalm_params.platform = \
        napalm_group_mapper.get(host.groups[0], 'no_platform_id')
    if "nxos" in host.name:
        napalm_params.port = 8443

    host.connection_options['netmiko'] = netmiko_params
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
