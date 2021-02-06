"""
Author: Bradley Fernando
Purpose: Uses Netmiko to connect to devices directly instead of using the
         plugin. Cisco devices also establish connections via SSH keys.

Usage:
    python exercise3.py

Output:

    cisco4#
    cisco3#
    nxos2#
    arista2#
    arista3#
    pyclass@srx1>
    arista1#
    arista4#
    nxos1#

"""
from nornir import InitNornir


def netmiko_direct(task):
    if "ios" in task.host.platform:
        task.host.username = "student1"
    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    print(net_connect.find_prompt())


def main():
    nr = InitNornir(config_file="config.yaml")
    nr.run(task=netmiko_direct)


if __name__ == "__main__":
    main()
