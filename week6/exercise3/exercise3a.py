"""
Author: Bradley Fernando
Purpose: Prompts the user for the device password before executing the task.

Usage:
    python exercise3a.py

Output:
    Password:
    2021-01-29 08:42:22,314 -  nornir.core -     INFO -        run() - Running task 'send_to_device' with args {} on 1 hosts
    2021-01-29 08:42:22,315 - nornir.core.task -    DEBUG -      start() - Host 'arista1': running task 'send_to_device'
    2021-01-29 08:42:22,315 - nornir.core.task -    DEBUG -      start() - Host 'arista1': running task 'netmiko_send_command'
    send_to_device******************************************************************
    * arista1 ** changed : False ***************************************************
    vvvv send_to_device ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- netmiko_send_command ** changed : False ----------------------------------- INFO
    VRF: default
    Codes: C - connected, S - static, K - kernel,
           O - OSPF, IA - OSPF inter area, E1 - OSPF external type 1,
           E2 - OSPF external type 2, N1 - OSPF NSSA external type 1,
           N2 - OSPF NSSA external type2, B I - iBGP, B E - eBGP,
           R - RIP, I L1 - IS-IS level 1, I L2 - IS-IS level 2,
           O3 - OSPFv3, A B - BGP Aggregate, A O - OSPF Summary,
           NG - Nexthop Group Static Route, V - VXLAN Control Service,
           DH - DHCP client installed default route, M - Martian
    
    Gateway of last resort:
     S      0.0.0.0/0 [1/0] via 10.220.88.1, Vlan1
    
     C      10.220.88.0/24 is directly connected, Vlan1
    
    ^^^^ END send_to_device ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""


from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
import getpass


PASSWORD = getpass.getpass()


def send_to_device(task):
    cmd = "show ip route"
    task.host.password = PASSWORD
    task.run(task=netmiko_send_command, command_string=cmd)


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="arista1")
    agg_result = nr.run(task=send_to_device)
    print_result(agg_result)


if __name__ == "__main__":
    main()
