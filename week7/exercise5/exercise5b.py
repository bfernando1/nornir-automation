"""
Author: Bradley Fernando
Purpose: Retrieves backup configs on nxos devices and saves a local copy to 
         current directory.

Usage:
    python exercise5b.py

Output:
# Sample of files that will be created on disk.
├── backups
│   └── nxos
│       ├── nxos1_checkpoint_2021-02-07@14:28:24
│       ├── nxos1_checkpoint_2021-02-07@14:32:52
│       └── nxos2_checkpoint_2021-02-07@14:32:52
"""


from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
from pathlib import Path
from time import gmtime, strftime


# Time format as example - 2021-02-07@14:28:24
time = strftime("%Y-%m-%d@%X", gmtime())


def retrieve_checkpoint(task):
    napalm_connect = task.host.get_connection("napalm", task.nornir.config)
    backup = napalm_connect._get_checkpoint_file()
    task.host['backup'] = backup
    return backup


def save_backup(task):
    platform = task.host.platform
    Path(f"backups/{platform}").mkdir(parents=True, exist_ok=True)
    with open(f"backups/{platform}/{task.host}_checkpoint_{time}", 'w') as f:
        f.write(backup)


def main():
    nr = InitNornir(config_file="../../config.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    agg_result = nr.run(task=retrieve_checkpoint)
    print_result(agg_result)
    nr.run(task=save_backup)


if __name__ == "__main__":
    main()
