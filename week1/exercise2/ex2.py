#!/usr/bin/env python3

from nornir import InitNornir

nr = InitNornir()
nr_hosts = nr.inventory.hosts

for key in nr_hosts:
    print()
    print(nr_hosts[key])
    print('-' * 20)
    print(f"hostname: {nr_hosts[key].hostname}")
    print(f"groups: {nr_hosts[key].groups}")
    print(f"platform: {nr_hosts[key].platform}")
    print(f"username: {nr_hosts[key].username}")
    print(f"password: {nr_hosts[key].password}")
    print(f"port: {nr_hosts[key].port}")
    print()
