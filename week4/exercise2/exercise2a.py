"""
Author: Bradley Fernando
Purpose: Transfer a local file to a remote device

Usage:
    python exercise2a.py

Output:
    arista1: Transferring BF_arista_test.txt
    arista2: Transferring BF_arista_test.txt
    arista3: Transferring BF_arista_test.txt
    arista4: Transferring BF_arista_test.txt
    arista2: Success
    arista1: Success
    arista3: Success
    arista4: Success
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
 
    # Work around, printing with f-string terminates the Nornir task
    print(task.host, end='') 
    print(": Transferring ", end='')
    print(base_file)
    
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
        print(": " + colorama.Fore.GREEN + "Success" + 
              colorama.Style.RESET_ALL)


if __name__ == "__main__":

    nr = InitNornir(config_file="config.yaml")
    eos_filt = F(groups__contains="eos")
    nr = nr.filter(eos_filt)
    results = nr.run(task=file_transfer)
