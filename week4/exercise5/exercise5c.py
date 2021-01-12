"""
Author: Bradley Fernando
Purpose: Retrieves the running config, configures a interface, and then restore the original config

Usage:
    python exercise5c.py

Output:

    </---Only showing end result for brevity--->

    * arista4 ** changed : True ****************************************************
    vvvv restore_config ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- napalm_configure ** changed : True ---------------------------------------- INFO
    @@ -54,9 +54,6 @@
     interface Loopback111
        description Hello
     !
    -interface Loopback112
    -   description Hello
    -!
     interface Loopback123
        description Hello
     !
    ^^^^ END restore_config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking

def get_config(task):
    config = task.run(task=networking.napalm_get, 
                 getters=['config'],
                 retrieve="running"
    ) 

    running_config = config[0].result['config']['running']
    return running_config
   
def config_interface(task, int_config):
    task.run(task=networking.napalm_configure, 
                configuration=int_config
    )                  

def restore_config(task, saved_config):
    task.run(task=networking.napalm_configure,
                configuration=saved_config,
                replace=True
    )

def main():
    int_config = f"""interface Loopback112
        description Hello"""
    device = "arista4"

    nr = InitNornir(config_file="../../config.yaml")
    nr = nr.filter(name=device)

    # Retrieve the running configuration
    config = nr.run(task=get_config)    
    print_result(config)
    running_config=config[device][0].result

    # Configure a loopback interface
    interface_result = nr.run(task=config_interface, 
                                int_config=int_config
    )
    print_result(interface_result)

    # Restore configurations 
    config_result = nr.run(task=restore_config, 
                                saved_config=running_config
    )  
    print_result(config_result)

    
if __name__ == "__main__":
    main()
