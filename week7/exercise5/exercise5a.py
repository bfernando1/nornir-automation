"""
Author: Bradley Fernando
Purpose: Retrieves the current configs on nxos devices and prints the output. 

Usage:
    python exercise5a.py

Output:
    retrieve_checkpoint*************************************************************
    * nxos1 ** changed : False *****************************************************
    vvvv retrieve_checkpoint ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    
    !Command: Checkpoint cmd vdc 1
    !Time: Sun Feb  7 14:33:59 2021
    
    version 9.2(3) Bios:version
    hostname nxos1
<!-- snipped for brevity-->
"""


from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F


def retrieve_checkpoint(task):
    napalm_connect = task.host.get_connection("napalm", task.nornir.config)
    backup = napalm_connect._get_checkpoint_file()
    task.host['backup'] = backup
    return backup


def main():
    nr = InitNornir(config_file="../../config.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    agg_result = nr.run(task=retrieve_checkpoint)
    print_result(agg_result)


if __name__ == "__main__":
    main()
