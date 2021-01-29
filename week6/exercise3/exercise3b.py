from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
import getpass
import logging


PASSWORD = getpass.getpass()
logger = logging.getLogger("nornir")

def send_to_device(task):
    cmd = "show ip route"
    task.host.password = PASSWORD 
    task.run(task=netmiko_send_command, command_string=cmd)


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="arista1")

    # Add logging test statements
    logger.debug("Flat is better than nested")

    agg_result = nr.run(task=send_to_device)
    print_result(agg_result)


if __name__ == "__main__":
    main()
