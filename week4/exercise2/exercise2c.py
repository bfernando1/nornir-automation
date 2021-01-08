"""
Author: Bradley Fernando
Purpose: Retrieve a file from a remote device and save it locally.

Usage:
    python exercise2c.py

Output:
    arista4: arista_test.txt
      retrieved - Success
    arista1: arista_test.txt
      retrieved - Success
    arista2: arista_test.txt
      retrieved - Success
    arista3: arista_test.txt
      retrieved - Success
"""
from nornir.plugins.tasks.networking import netmiko_file_transfer
from nornir.core.filter import F
import colorama

def file_transfer(task):
    group_name = task.host.platform
    source_file = "arista_test.txt"
    dest_file = f"{group_name}/{task.host}-saved.txt"
 
    # Use Netmiko to retrieve file
    results = task.run(task=netmiko_file_transfer,
                    source_file=source_file,
                    dest_file=dest_file,
                    overwrite_file=True,
                    direction="get"
    )
    
    if results[0].result is False:
        print(f"File retriival failed")
    else:
        colorama.init()
        print(task.host, end='')
        print(": ", end='')
        print(source_file)
        print("  retrieved - ", end='')
        print(colorama.Fore.GREEN + "Success" + 
              colorama.Style.RESET_ALL)


if __name__ == "__main__":

    nr = InitNornir(config_file="config.yaml")
    eos_filt = F(groups__contains="eos")
    nr = nr.filter(eos_filt)
    results = nr.run(task=file_transfer)
