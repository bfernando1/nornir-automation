"""
Author: Bradley Fernando
Propose: Retrieve the file content after sending a local file to a remote device"

Usage:
    python exercise2b.py

Output:
    arista3 - Transferring BF_arista_test.txt: Success
    File Content:
    Arista Location: 5453 Great America Parkway, Santa Clara, CA 95054
    
    arista2 - Transferring BF_arista_test.txt: Success
    File Content:
    Arista Location: 5453 Great America Parkway, Santa Clara, CA 95054
    
    arista1 - Transferring BF_arista_test.txt: Success
    File Content:
    Arista Location: 5453 Great America Parkway, Santa Clara, CA 95054
    
    arista4 - Transferring BF_arista_test.txt: Success
    File Content:
    Arista Location: 5453 Great America Parkway, Santa Clara, CA 95054

"""
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_file_transfer
from nornir.plugins.tasks.networking import netmiko_send_command
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
        cmd = f"more flash:/{base_file}"
        file_output = task.run(task=netmiko_send_command, 
                            command_string=cmd)
        colorama.init()
        print(task.host, end='') 
        print(" - Transferring ", end='')
        print(base_file, end='')
        print(": " + colorama.Fore.GREEN + "Success" + 
              colorama.Style.RESET_ALL)
        print("File Content: ")
        print(file_output[0].result)
        print()
    

if __name__ == "__main__":

    nr = InitNornir(config_file="config.yaml")
    eos_filt = F(groups__contains="eos")
    nr = nr.filter(eos_filt)
    results = nr.run(task=file_transfer)
