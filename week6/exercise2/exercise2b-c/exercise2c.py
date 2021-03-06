"""
Author: Bradley Fernando
Purpose: Modifies the failed multi-result object with a custom message. 

Usage:
    python exercise2c.py

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
    Encountered Jinja2 error
    ^^^^ END render_config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks import text
from nornir.plugins.functions.text import print_result
from nornir.core.exceptions import NornirSubTaskError
from nornir.core.task import Result


def render_config(task):
    try:
        template = "loopback_int.j2"
        task.run(
            task=text.template_file, path=".", template=template, **task.host)
    except NornirSubTaskError:
        task.results.pop()
        msg = "Encountered Jinja2 error"
        return Result(
            changed=False,
            diff=None,
            result=msg,
            host=task.host,
            failed=False,
            exception=None
        )


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    agg_result = nr.run(task=render_config)
    print_result(agg_result)


if __name__ == "__main__":
    main()
