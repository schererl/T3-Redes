class Topology:
    def __init__(self, nodes, routers, routertable):
        self.nodes = nodes
        self.routers = routers
        self.routertable = routertable
    def __str__(self):
        output = "NODES: \n"
        for n in self.nodes:
            output += '\t' + str(n) + '\n'
        
        output += "ROUTERS: \n" 
        for r in self.routers:
            output += '\t' + str(r) + '\n'

        #output += "ROUTER TABLE \n" + str(routertable)
        #output += '\n'

        return output


class Node:
    def __init__(self, name, mac, ip_prefix, mtu, gateway):
        self.name = name
        self.mac = mac
        self.ip_prefix = ip_prefix
        self.mtu = mtu
        self.gateway = gateway
        self.arp_table = []

    def __str__(self):
        output = "<" + self.name + "><" + str(self.mac) + "><" + str(self.ip_prefix) + "><" + str(self.mtu) + "><" + str(self.gateway) + ">"
        
        for elem in self.arp_table:
            output+= elem + '\n'
        return output

class Router:
    def __init__(self, name, num_ports, node_routers):
        self.name = name
        self.num_ports = num_ports
        self.node_routers = node_routers
        self.arp_table = []

    def __str__(self):
        
        output = "<" + self.name + "><" + str(self.num_ports) + ">" 
        
        for elem in self.node_routers:
            output += str(elem)
        for elem in self.arp_table:
            output += elem
        
        return output

class Routertable:
    def __init__(self, name, dest_prefix, nexthop ,port):
        self.name = name
        self.dest_prefix = dest_prefix
        self.nexthop = nexthop
        self.port = port

    def __str__(self):
        return "<" + self.name + "><" + str(self.dest_prefix) + "><" + str(self.nexthop) + "><" + str(self.port) + ">" 
        
