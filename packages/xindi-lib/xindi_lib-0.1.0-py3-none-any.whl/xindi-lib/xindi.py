from ipaddress import IPv4Network
import json

class ManagedNetwork():
    def __init__(self, indict=None, injson=None):
        if injson is not None:
            self.readJson(injson)
        if indict is not None:
            self.read(indict)
    
    def read(self, indict):
        if not 'managed_network' in indict.keys(): 
            raise ValueError('Key managed_network not found in input dict (indict)')
        
        self.free_netspace = [IPv4Network(indict['managed_network'])]
        self.managed_network = indict['managed_network']
        self.assigned_networks = list()
        for net in indict.get('assigned_subnets', list()):
            assign_network(net)

    def readJson(self, injson):
        self.read(json.loads(injson))

    def export(self):
        out_dict = dict()
        out_dict['managed_network'] = self.managed_network
        out_dict['assigned_subnets'] = list()
        for net_dict in self.assigned_networks:
            net_dict['cidr'] = str(net_dict['cidr'])
            out_dict['assigned_subnets'].append(net_dict)
        return out_dict

    def exportJson(self):
        return json.dumps(self.export())

    def assign_network(self, net_dict):
        self.unfree_network(net_dict['cidr'])
        self.assigned_networks.append(net_dict)

    def unfree_network(self, remove):
        if type(self.free_netspace) is str:
            self.free_netspace = list().append(self.free_netspace)
        else:
            self.free_netspace = [anet for anet in self.free_netspace]
        remain = list()
        for net in self.free_netspace:
            try: 
                remain += list(
                    IPv4Network(net).address_exclude(IPv4Network(remove))
                    )
            except ValueError:
                remain.append(net)
        self.free_netspace = remain

    def free(self, cidr):
        new_list = list()
        for net in self.assigned_networks:
            if str(net['cidr']) not in str(cidr):
                new_list.append(net)
        self.assigned_networks = new_list

    def next_free_subnet(self, size, metadata=dict()):
        # first look for leftovers in the right size
        for net in self.free_netspace:
            if net.prefixlen == size:
                net_dict = dict(cidr=net)
                net_dict.update(metadata)
                self.assign_network(net_dict)
                return net
        # if no leftovers, cut a piece of a larger free net
        for net in self.free_netspace:
            this = [newnet for newnet in net.subnets(new_prefix=size)]
            if len(this) > 1:
                net_dict = dict(cidr=this[0])
                net_dict.update(metadata)
                self.assign_network(net_dict)
                return this[0]
        return False

