from nornir import InitNornir
from nornir.plugins.tasks import data, text, files
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
import ipdb

to_configure = ["bgp", "int"]

def render_config(task):
    config_path = f"{task.host.platform}/"
     
    for cfg in to_configure: 
        render_config = task.run(
            task=text.template_file, template=f"{cfg}.j2", path=config_path, **task.host
        )
        render_config = render_config[0].result
        task.host[f"{cfg}_rendered_config"] = render_config

def write_config(task):
    for cfg in to_configure:
        cfg_path = "rendered_configs/"
        filename = f"{cfg_path}/{task.host}_{cfg}_config"
        content = task.host[f"{cfg}_rendered_config"]
        task.run(task=files.write_file, filename=filename, content=content)
    
def main():
    nr = InitNornir(config_file="config.yaml")
    nxos_filt = F(groups__contains="nxos")
    nr = nr.filter(nxos_filt)

    render_result = nr.run(task=render_config)    
    print_result(render_result)

    write_result = nr.run(task=write_config)
    print_result(write_result)

if __name__ == "__main__":
    main()
