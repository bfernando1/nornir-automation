from nornir import InitNornir
from nornir.plugins.tasks import data, text
import ipdb

def render_config(task):
    config_path = f"{task.host.platform}/"
    int_config = task.run(
        task=text.template_file, template="interface.j2", path=config_path, **task.host
    )
#    bgp_config = task.run(
#        task=text.template_file, template="bgp.j2", path=config_path, **task.host
#    )
    ipdb.set_trace() 

def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="nxos1")
    agg_result = nr.run(task=render_config)    
    #ipdb.set_trace() 

if __name__ == "__main__":
    main()
