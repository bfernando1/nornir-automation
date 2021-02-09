from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks import networking
import ipdb


def config_interfaces(task):
    print(task.host)
    ipdb.set_trace()
    
def main():
    nr = InitNornir(config_file="config.yaml")
    #nr = nr.filter(F(groups__contains="nxos"))
    nr = nr.filter(name="nxos1")
    nr.run(task=config_interfaces, num_workers=1)


if __name__ == "__main__":
    main()
