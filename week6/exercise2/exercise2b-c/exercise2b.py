"""
Author: Bradley Fernando
Purpose: Returns a custom message when handling NornirSubTask errors.

Usage:
    python exercise2b.py

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
    Something happened, check templates or input sources
    ---- template_file ** changed : False ------------------------------------------ ERROR
    </-- snipped -->
    jinja2.exceptions.UndefinedError: 'loopbacks' is undefined
"""


from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks import text
from nornir.plugins.functions.text import print_result
from nornir.core.exceptions import NornirSubTaskError


def render_config(task):
    try:
        template = "loopback_int.j2"
        task.run(
            task=text.template_file, path=".", template=template, **task.host)
    except NornirSubTaskError:
        return "Something happened, check templates or input sources"


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    agg_result = nr.run(task=render_config)
    print_result(agg_result)


if __name__ == "__main__":
    main()
