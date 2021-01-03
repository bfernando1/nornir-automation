from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import napalm_get

nr = InitNornir(config_file="../../config.yaml")
nxos_filt = F(groups__contains="nxos")
nr = nr.filter(nxos_filt)

def get_running_config(task):
    results = task.run(task=napalm_get,
                     getters=['config'],
                     retrieve='running'
    )
    print_result(results)

print("\nRetrieving running configs for NX-OS devices:")
print('-' * 60)
nr.run(task=get_running_config)

