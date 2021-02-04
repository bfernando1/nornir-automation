"""
Author: Bradley Fernando
Purpose: Retrieve parameters from Ansible inventory plugin

Usage:
    python exercise1a.py

Output:
    
          Host: nxos1
      Username: pyclass
      Password: bogus
          Port: None
      Platform: nxos
        Napalm: 8443

"""


from nornir import InitNornir


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


if __name__ == "__main__":
    main()
