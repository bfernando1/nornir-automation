"""
Author: Bradley Fernando
Purpose: Configure a loopback interace using Napalm configure plugin

Usage:
    python exercise5b.py

Output:
    config_interface****************************************************************
    * arista4 ** changed : True ****************************************************
    vvvv config_interface ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- napalm_configure ** changed : True ---------------------------------------- INFO
    @@ -51,6 +51,9 @@
     interface Loopback99
        ip address 172.31.1.13/30
     !
    +interface Loopback123
    +   description Hello
    +!
     interface Management1
        shutdown
     !
    ^^^^ END config_interface ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import napalm_configure

def config_interface(task):
    int_config = f"""interface Loopback123
        description Hello"""

    task.run(task=napalm_configure,configuration=int_config)

def main():
    nr = InitNornir(config_file="../../config.yaml")
    nr = nr.filter(name="arista4")
    results = nr.run(task=config_interface)
    print_result(results)

if __name__ == "__main__":
    main()
