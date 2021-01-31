from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
import os


def set_session_name(task):
    filename = f"{task.host}-output.log"
    group_object = task.host.groups.refs[0]
    group_object.connection_options["netmiko"].extras["session_log"] = filename


def send_command(task):
    task.run(task=set_session_name)
    cmd = "show feature | grep enabled"
    task.host.password = os.environ["BF_PASSWORD"]
    task.run(task=netmiko_send_command, command_string=cmd)


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    agg_result = nr.run(task=send_command)
    print_result(agg_result)


if __name__ == "__main__":
    main()
