from nornir import InitNornir
from nornir.core.filter import F


def netmiko_direct(task):
    if "ios" in task.host.platform:
        task.host.username = "student1"
    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    print(net_connect.find_prompt())

    
def main():
    nr = InitNornir(config_file="config.yaml")
    agg_result = nr.run(task=netmiko_direct)
    

if __name__ == "__main__":
    main()
