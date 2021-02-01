from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from nornir.core.exceptions import NornirSubTaskError
import random
import os


BAD_PASSWORD = "bananapie"


def send_command(task):
    cmd_mapper = {"junos": "show system uptime"}
    cmd = cmd_mapper.get(task.host.platform, "show clock")
    try:
        task.run(task=netmiko_send_command, command_string=cmd)
    except NornirSubTaskError:
        if "NetmikoAuthenticationException" in task.results[0].result:
            task.host.password = os.environ["NORNIR_PASSWORD"]
    
            # Force close failed connections in Nornir
            try:
                task.host.close_connections()
            except ValueError:
                pass

            # Remove previous results before retrying the task
            task.results.pop()
            task.run(task=netmiko_send_command, command_string=cmd)


def main():
    nr = InitNornir(config_file="../../config.yaml")
    for host, data in nr.inventory.hosts.items():
        if random.choice([True, False]):
            data.password = BAD_PASSWORD
    agg_result = nr.run(task=send_command)
    print_result(agg_result)


if __name__ == "__main__":
    main()
