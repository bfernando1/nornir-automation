from nornir import InitNornir
from nornir.plugins.tasks import data, text, files, networking
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
import ipdb
import time

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

def deploy_config(task):
    for cfg in to_configure:
        with open(f"rendered_configs/{task.host}_{cfg}_config") as f:
            cfg_file = f.read()
        deployed_config = task.run(task=networking.napalm_configure, configuration=cfg_file)
    
def main():
    nr = InitNornir(config_file="config.yaml")
    nxos_filt = F(groups__contains="nxos")
    nr = nr.filter(nxos_filt)

    render_result = nr.run(task=render_config)    
    print_result(render_result)

    write_result = nr.run(task=write_config)
    print_result(write_result)
    
    deploy_result = nr.run(task=deploy_config)
    print_result(deploy_result)

    print("checking bgp neighborship in ...")
    for i in range(10, 0, -1):
        print(i)
        time.sleep(1)
    bgp_neighbors = nr.run(task=networking.napalm_get, getters=["bgp_neighbors"])
    print_result(bgp_neighbors)

if __name__ == "__main__":
    main()
