from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from nornir.core.task import Result
from nornir.core.filter import F

nr = InitNornir(config_file="../../config.yaml")

def get_uptime(task):
    all_cmds = {
        "eos": "show version | inc Uptime",
        "ios": "show version | inc uptime",
        "junos": "show system uptime | match System",
        "nxos": "show version | inc uptime"
    }
    cmd = all_cmds[task.host.platform] 
    task.run(task=netmiko_send_command, command_string=cmd)

print("\nGathering uptime from all devices...\n")
agg_result = nr.run(task=get_uptime)
for host, uptime in agg_result.items():
    print(f"Working on {host}:")
    print('-' * 60)
    print(f"{uptime[1].result.strip()}\n")
