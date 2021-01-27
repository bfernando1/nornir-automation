from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking, text
import ipdb


def render_config(task):
    loopback_template = "loopback_int.j2"
    rendered_data = task.run(task=text.template_file,
                             path=".", 
                             template=loopback_template,
                             **task.host)


def main():
    nr = InitNornir(config_file="config.yaml")
    #nr = nr.filter(name="nxos1")
    nr = nr.filter(F(groups__contains="nxos"))
    agg_result = nr.run(task=render_config)
    print_result(agg_result)
    #ipdb.set_trace()

if __name__ == "__main__":
    main()
