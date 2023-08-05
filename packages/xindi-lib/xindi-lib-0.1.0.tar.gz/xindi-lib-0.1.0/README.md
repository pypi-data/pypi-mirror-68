# xindi-lib

allows you to manage subnets of a network.
```
from xindi import ManagedNetwork
```

You can start with a dictionary
```
input_data = dict()
input_data['managed_network'] = '10.0.0.0/26'
managed_network = ManagedNetwork(indict=input_data)

```
or with JSON
```
input_data = '{"managed_network": "10.0.0.0/26"}'
managed_network = ManagedNetwork(injson=input_data)
```
assign new subnets of the needed size
```
my_first_net = dict(
    usecase='first network', 
    owner='Wolfgang Wangerin', 
    department='ITA'
    )
managed_network.next_free_subnet(27, my_first_net)
```
or free an existing subnet
```
managed_network.free('10.0.0.0/27')
```
list all assigned subnets:
```
managed_network.assigned_networks()
```
and export the configuration
```
outdict = managed_network.export()
outjson = managed_network.exportJson()
```

It is now up to you to set up an API or Webfrontend and use this library. Let me know, if you use this in an FOSS project, because I may have a usecase for it.
