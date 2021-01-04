"""
Author: Bradley Fernando
Purpose: Retrieve all configs using Napalm getter for all NX-OS devices.

Usage:
    python exercise6a.py

Output:

    Retrieving configs for NX-OS devices:
    ----------------------------------------
    vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    { 'config': { 'candidate': '',
                  'running': '!Running configuration last done at: Mon Jan  4 '
                             '05:24:06 2021\n'
                             '\n'
                             'version 9.2(3) Bios:version  \n'
                             'hostname nxos2\n'
                             'vdc nxos2 id 1\n'
    <!--- Snipped --->
"""
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import napalm_get

nr = InitNornir(config_file="../../config.yaml")
nxos_filt = F(groups__contains="nxos")
nr = nr.filter(nxos_filt)

def get_all_config(task):
    results = task.run(task=napalm_get,
                     getters=['config']
    )
    print_result(results)

print("\nRetrieving configs for NX-OS devices:")
print('-' * 40)
nr.run(task=get_all_config)
