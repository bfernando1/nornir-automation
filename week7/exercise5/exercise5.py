from nornir import InitNornir
from nornir.plugins.functions.text import print_result

def retrieve_checkpoint(task):
    napalm_connect = task.host.get_connection("napalm", task.nornir.config) 
    backup = napalm_connect._get_checkpoint_file()
    task.host['backup'] = backup 
    return backup
    
def main():
    nr = InitNornir(config_file="../../config.yaml")
    nr = nr.filter(name="nxos1")
    agg_result = nr.run(task=retrieve_checkpoint)
    print_result(agg_result)
    
if __name__ == "__main__":
    main()
