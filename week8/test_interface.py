from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking


def bogus_interface(task):
    cmd = """interface lo101
  ip address 1.1.1.1 255.255.255.255"""
    task.run(task=networking.napalm_configure, configuration=cmd)
  

def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="nxos1")
    agg_results = nr.run(task=bogus_interface)
    print_result(agg_results) 


if __name__ == "__main__":
    main()
