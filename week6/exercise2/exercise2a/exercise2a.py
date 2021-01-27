"""
Author: Bradley Fernando
Purpose: Uses a loopback interface template to create a config for NX-OS.

Usage:
    python exercise2a.py

Output:
    render_config*******************************************************************
    * nxos1 ** changed : False *****************************************************
    vvvv render_config ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- template_file ** changed : False ------------------------------------------ INFO
    loopback 111
      description vEdge_1
      ip address 1.1.1.1 255.255.255.255
    ^^^^ END render_config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    * nxos2 ** changed : False *****************************************************
    vvvv render_config ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
    ---- template_file ** changed : False ------------------------------------------ INFO
    loopback 222
      description vEdge_2
      ip address 2.2.2.2 255.255.255.255
    ^^^^ END render_config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""


from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import text


def render_config(task):
    template = "loopback_int.j2"
    task.run(
        task=text.template_file, path=".", template=template, **task.host)


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    agg_result = nr.run(task=render_config)
    print_result(agg_result)


if __name__ == "__main__":
    main()
