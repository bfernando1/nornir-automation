"""
Author: Bradley Fernando
Purpose: Retrieve running configuration from a device using Napalm getters

Usage:
    python exercise5a.py

Output:
    * arista4 ** changed : False ***************************************************
    vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    { 'config': { 'candidate': '',
                  'running': '! Command: show running-config\n'
                             '! device: arista4 (vEOS, EOS-4.20.10M)\n'
                             '!\n'
                             '! boot system flash:/vEOS-lab.swi\n'
                             '!\n'
                             'transceiver qsfp default-mode 4x10G\n'
                             '!\n'
                             'hostname arista4\n'
                             '!\n'
                             'ntp server 130.126.24.24\n'
                             '!\n'
                             'spanning-tree mode rapid-pvst\n'
                             '!\n'
                             'aaa authorization exec default local\n'
                             '!\n'
                             'no aaa root\n'
                             '!\n'
                             'username admin privilege 15 role network-admin '
                             'secret 5 $1$aM6w809x$tgkc6ZGhcScvELVKVHq3n0\n'
                             'username admin1 privilege 15 secret 5 '
                             '$1$7kD0oS/t$wXhtTFwnWwnlPFKWwXoJ70\n'
                             'username eapi secret 5 '
                             '$1$kGsls/wg$brwRo1OGS0OaTdnKuWHQG/\n'
                             'username pyclass privilege 15 secret 5 '
                             '$1$C3VfUfcO$86t4iqCX60yW.NIR8d2Lh0\n'
                             '!\n'
                             'clock timezone America/Los_Angeles\n'
                             '!\n'
                             'vlan 2-4,6-7\n'
                             '!\n'
                             'vlan 5\n'
                             '   name mgmt\n'
                             '!\n'
                             'interface Ethernet1\n'
                             '   spanning-tree portfast\n'
                             '   spanning-tree cost 1\n'
                             '!\n'
                             'interface Ethernet2\n'
                             '   switchport access vlan 2\n'
                             '!\n'
                             'interface Ethernet3\n'
                             '   switchport access vlan 3\n'
                             '!\n'
                             'interface Ethernet4\n'
                             '   switchport access vlan 4\n'
                             '!\n'
                             'interface Ethernet5\n'
                             '   switchport access vlan 5\n'
                             '!\n'
                             'interface Ethernet6\n'
                             '   switchport access vlan 6\n'
                             '!\n'
                             'interface Ethernet7\n'
                             '   switchport access vlan 7\n'
                             '!\n'
                             'interface Management1\n'
                             '   shutdown\n'
                             '!\n'
                             'interface Vlan1\n'
                             '   ip address 10.220.88.31/24\n'
                             '!\n'
                             'ip route 0.0.0.0/0 10.220.88.1\n'
                             '!\n'
                             'ip routing\n'
                             '!\n'
                             'management api http-commands\n'
                             '   no shutdown\n'
                             '!\n'
                             'end\n',
                  'startup': ''}}
    ^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
from nornir.plugins.tasks import networking

def main():
    nr = InitNornir(config_file="../../config.yaml")
    arista4 = nr.filter(name="arista4")
    results = arista4.run(task=networking.napalm_get, 
                     getters=["config"], 
                     retrieve="running" 
    )
    
    #import ipdb; ipdb.set_trace()
    print_result(results)

if __name__ == "__main__":
    main()
