from nornir import InitNornir
from nornir.plugins.tasks import data, text
from nornir.core.filter import F
import ipdb

def render_config(task):
    config_path = f"{task.host.platform}/"

    # Interface config
    int_config = task.run(
        task=text.template_file, template="interface.j2", path=config_path, **task.host
    )
    int_config = int_config[0].result
    task.host['int_rendered_config'] = int_config

    # BGP config
    bgp_config = task.run(
        task=text.template_file, template="bgp.j2", path=config_path, **task.host
    )
    bgp_config = bgp_config[0].result
    task.host['bgp_rendered_config'] = bgp_config
    
def main():
    nr = InitNornir(config_file="config.yaml")
    nxos_filt = F(groups__contains="nxos")
    nr = nr.filter(nxos_filt)
    agg_result = nr.run(task=render_config)    
    ipdb.set_trace() 

if __name__ == "__main__":
    main()
