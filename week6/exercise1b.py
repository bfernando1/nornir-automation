"""
Author: Bradley Fernando
Purpose: Displays a value error when the Nornir result is an unexpected 
         output. 

Usage:
    python exercise1b.py

Output:

    Host 'srx2': task 'send_command' failed with traceback:
    Traceback (most recent call last):
      File "/home/bradfernan/VENV/py3_venv/lib64/python3.7/site-packages/nornir/core/task.py", line 85, in start
        r = self.task(self, **self.params)
      File "exercise1b.py", line 15, in send_command
        raise ValueError("The command wasn't accepted")
    ValueError: The command wasn't accepted
"""
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
import ipdb

def send_command(task):
    
    task.run(task=netmiko_send_command, 
             command_string="set cli complete-on-space off"
    )
    output = task.run(task=netmiko_send_command,
                      command_string="show ip interface")

    if "syntax error" in output.result:
        raise ValueError("The command wasn't accepted")
    
def main():
    nr = InitNornir(config_file="../../config.yaml")    
    nr = nr.filter(name="srx2")
    agg_result = nr.run(task=send_command)
    print_result(agg_result)
    
if __name__ == "__main__":
    main()
