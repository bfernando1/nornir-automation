"""
Author: Bradley Fernando
Propose: Use Naplam getters to compare the startup and running configs.

Usage:
    python exercise6d.py

Output:

    Getting device statistics from NX-OS devices:
    ------------------------------------------------------------
    {'nxos1': {'model': 'Nexus9000 9000v Chassis',
               'start_running_match': True,
               'uptime': 12058413,
               'vendor': 'Cisco'},
     'nxos2': {'model': 'Nexus9000 9000v Chassis',
               'start_running_match': True,
               'uptime': 12057908,
               'vendor': 'Cisco'}}
    
"""
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import napalm_get
from pprint import pprint
import re

nr = InitNornir(config_file="../../config.yaml")
nxos_filt = F(name__contains="nxos")
nr = nr.filter(nxos_filt)

agg_result = nr.run(
    task=napalm_get,
    getters=['config', 'facts'],
    getters_options={'config': {'retrieve':'all'}}
)

combined_data = {}
for host, multi_result in agg_result.items():
    combined_data[host] = {}
    device_stats = {}
    device_results = multi_result[0].result
    running = device_results['config']['running'] 
    startup = device_results['config']['startup'] 
   
    # Remove any initial timestamp from the configs 
    startup_filt = re.sub(".+\\n\\n", '', startup)
    running_filt = re.sub(".+\\n\\n", '', running)
    startup_running_match = (startup_filt == running_filt)
   
    device_stats['model'] = device_results['facts']['model'] 
    device_stats['start_running_match'] = startup_running_match
    device_stats['uptime'] = device_results['facts']['uptime'] 
    device_stats['vendor'] = device_results['facts']['vendor'] 
    combined_data[host] = device_stats 

print("\nGetting device statistics from NX-OS devices:")
print('-' * 60)
pprint(combined_data)
print()
