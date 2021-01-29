"""
Author: Bradley Fernando
Purpose: Display custom logging messages in the log file

Usage:
    python exercise3b.py

Output:
    Password:
    2021-01-29 08:43:48,298 -       nornir -    DEBUG -       main() - Flat is better than nested
    2021-01-29 08:43:48,298 -       nornir - CRITICAL -       main() - Sparse is better than dense
    2021-01-29 08:43:48,298 -       nornir -    ERROR -       main() - Unless explicitly silenced
    2021-01-29 08:43:48,299 -  nornir.core -     INFO -        run() - Running task 'send_to_device' with args {} on 1 hosts
    2021-01-29 08:43:48,299 - nornir.core.task -    DEBUG -      start() - Host 'arista1': running task 'send_to_device'
    2021-01-29 08:43:48,300 - nornir.core.task -    DEBUG -      start() - Host 'arista1': running task 'netmiko_send_command'
"""


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
    logger.critical("Sparse is better than dense")
    logger.error("Unless explicitly silenced")

    agg_result = nr.run(task=send_to_device)
    print_result(agg_result)


if __name__ == "__main__":
    main()
