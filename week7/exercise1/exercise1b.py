"""
Author: Bradley Fernando
Purpose: Uses Napalm to retrieve the NTP server information. Ansible style inventory is
         still used. 

Usage:
    python exercise1b.py

Output:
    
          Host: nxos1
      Username: pyclass
      Password: 88newclass
          Port: None
      Platform: nxos
        Napalm: 8443

    send_command********************************************************************
    * nxos1 ** changed : False *****************************************************
    vvvv send_command ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- napalm_get ** changed : False --------------------------------------------- INFO
    {'ntp_servers': {'130.126.24.24': {}, '152.2.21.1': {}}}
    ^^^^ END send_command ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
          

from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result


def send_command(task):
    task.run(task=napalm_get, getters=['ntp_servers'])


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="nxos1")

    nxos_host = nr.inventory.hosts["nxos1"]
    nxos_group = nr.inventory.groups["nxos"]
    print("\n{:>10}: {}".format("Host", nxos_host))
    print("{:>10}: {}".format("Username", nxos_host.username))
    print("{:>10}: {}".format("Password", nxos_host.password))
    print("{:>10}: {}".format("Port", nxos_host.port))
    print("{:>10}: {}".format("Platform", nxos_host.platform))
    print("{:>10}: {}\n".format("Napalm",
          nxos_group.get_connection_parameters("napalm").port))

    agg_result = nr.run(send_command)
    print_result(agg_result)


if __name__ == "__main__":
    main()
