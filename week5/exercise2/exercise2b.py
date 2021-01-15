from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result     
from nornir.plugins.tasks.networking import napalm_get
import ipdb

def main():
    nr = InitNornir(config_file="config.yaml")
    eos_filt = F(groups__contains="eos")
    nr = nr.filter(eos_filt) 
    agg_results = nr.run(task=napalm_get, 
                getters=['config'] 
    )
    ipdb.set_trace()
    

if __name__== "__main__":
    main()

