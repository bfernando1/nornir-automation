"""
Author: Bradley Fernando
Purpose: Use Ansible vault to retrieve the correct device password. It
         then executes a task to gather the current clock status. 

Usage:
    python exercise5c.py

Output:
   <!-- Trimmed to a single device for brevity -->
    send_command********************************************************************
    * arista1 ** changed : False ***************************************************
    vvvv send_command ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- netmiko_send_command ** changed : False ----------------------------------- INFO
    Wed Feb  3 10:21:31 2021
    Timezone: America/Los_Angeles
    Clock source: NTP server (130.126.24.24)
    ^^^^ END send_command ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
"""

import os
import random
import yaml
from ansible.parsing.vault import VaultLib, VaultSecret
from ansible.cli import CLI
from ansible. parsing.dataloader import DataLoader
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from nornir.core.exceptions import NornirSubTaskError


BAD_PASSWORD = "bananapie"
VAULT_PASSWORD = os.environ["NORNIR_VAULT_PASSWORD"]
VAULT_FILE = "vaulted_password.yaml"


def decrypt_vault(
    filename, vault_password=None, vault_password_file=None,
    vault_prompt=False
):
    """
    filename: name of your encrypted file that needs to be decrypted.
    vault_password: key that will decrypt the file.
    vault_password_file: file containing key that will decrypt the vault.    vault_prompt: Force vault to prmopt for a password if everything 
                  else fails. 
    """
    
    loader = DataLoader()
    if vault_password:
        vault_secret = [([], VaultSecret(vault_password.encode()))]
    elif vault_password_file:
        vault_secret = CLI.setup_vault_secrets(
            loader=loader, vault_ids=[vault_password_file]
        )
    else:
        vault_secret = CLI.setup_vault_secrets(
            loader=loader, vault_ids=[], auto_prompt=vault_prompt
        )

    vault = VaultLib(vault_secret)

    with open(filename) as f:
        unencrypted_yaml = vault.decrypt(f.read())
        unencrypted_yaml = yaml.safe_load(unencrypted_yaml)
        return unencrypted_yaml


def send_command(task):
    cmd_mapper = {"junos": "show system uptime"}
    cmd = cmd_mapper.get(task.host.platform, "show clock")
    try:
        task.run(task=netmiko_send_command, command_string=cmd)
    except NornirSubTaskError:
        if "NetmikoAuthenticationException" in task.results[0].result:
            vault_contents = decrypt_vault(
                filename=VAULT_FILE, vault_password=VAULT_PASSWORD
            )
            task.host.password = vault_contents["password"]
                      
            # Force close failed connections in Nornir
            try:
                task.host.close_connections()
            except ValueError:
                pass

            # Remove previous results before retrying the task
            task.results.pop()
            task.run(task=netmiko_send_command, command_string=cmd)


def main():
    nr = InitNornir(config_file="../../config.yaml")
    for host, data in nr.inventory.hosts.items():
        if random.choice([True, False]):
            data.password = BAD_PASSWORD
    agg_result = nr.run(task=send_command)
    print_result(agg_result)


if __name__ == "__main__":
    main()
