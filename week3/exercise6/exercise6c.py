"""
Author: Bradley Fernando
Purpose: Uses Napalm getter to fact gather on all NX-OS devices.

Usage:
    python exercise6c.py

Output:

    Retrieving running configs and facts for NX-OS devices:
------------------------------------------------------------
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'config': { 'candidate': '',
              'running': '!Running configuration last done at: Mon Jan  4 '
                         '05:16:03 2021\n'
                         '\n'
<!--- snipped --->

"""
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import napalm_get

nr = InitNornir(config_file="../../config.yaml")
nxos_filt = F(groups__contains="nxos")
nr = nr.filter(nxos_filt)

def get_running_config(task):
    results = task.run(
                task=napalm_get,
                getters=['config', 'facts'],
                getters_options={'config': {'retrieve': 'running'}}
    )
    print_result(results)

print("\nRetrieving running configs and facts for NX-OS devices:")
print('-' * 60)
nr.run(task=get_running_config)
