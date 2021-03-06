"""
Author: Bradley Fernando
Purpose: Transfer a local file to a remote device

Usage:
    python exercise2a.py

Output:
    arista1: BF_arista_test.txt
      transferring - Success
    arista2: BF_arista_test.txt
      transferring - Success
    arista4: BF_arista_test.txt
      transferring - Success
    arista3: BF_arista_test.txt
      transferring - Success
"""

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_file_transfer
from nornir.core.filter import F
import colorama

def file_transfer(task):
    group_name = task.host.platform
    base_file = task.host['file_name']
    source_file = f"{group_name}/{base_file}"
    dest_file = base_file
 
    # Use Netmiko to transfer file
    results = task.run(task=netmiko_file_transfer,
                    source_file=source_file,
                    dest_file=dest_file,
                    overwrite_file=True,
                    direction="put"
    )
    
    if results[0].result is False:
        print(f"File transfer failed")
    else:
        colorama.init()
        print(task.host, end='')
        print(": " + base_file)
        print("  transferring - ", end='')
        print(colorama.Fore.GREEN + "Success" + 
              colorama.Style.RESET_ALL)


if __name__ == "__main__":

    nr = InitNornir(config_file="config.yaml")
    eos_filt = F(groups__contains="eos")
    nr = nr.filter(eos_filt)
    results = nr.run(task=file_transfer)
