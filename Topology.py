class Topology:
    def __init__(self, nodes, routers, routertable, nodes_names):
        self.nodes = nodes
        self.routers = routers
        self.routertable = routertable
        self.nodes_names = nodes_names

    def check_if_node_is_router(self, node):
        for router in self.routers:
            if node in router.node_routers:
                return True
        return False

    def get_router_by_node(self, node):
        for router in self.routers:
            if node in router.node_routers:
                return router
        return None

    def __str__(self):
        output = "NODES: \n"
        for n in self.nodes:
            output += '\t' + str(n) + '\n'
        
        output += "ROUTERS: \n" 
        for r in self.routers:
            output += '\t' + str(r) + '\n'

        output += "ROUTER TABLE: \n" + str(self.routertable)
        output += '\n'

        return output

class Node:
    # IMPORTANT:
        # nodes must pass {} as parameter at arp_table the instance must be different for each node
        # routers.node_routers share the same arp_table so it passes a reference of the same instance
    def __init__(self, name, mac, ip_prefix, gateway, arp_table):
        self.name = name
        self.mac = mac
        self.ip_prefix = ip_prefix
        self.gateway = gateway
        self.arp_table = arp_table 

    def __str__(self):
        output = "<" + self.name + "><" + str(self.mac) + "><" + str(self.ip_prefix) + "><" + str(self.gateway) + ">"
        for elem in self.arp_table:
            output+= elem + '\n'
        return output

class Router:
    def __init__(self, name, num_ports, node_routers):
        self.name = name
        self.num_ports = num_ports
        self.node_routers = []
        self.arp_table = {} #this arp_table is the same for each intern_node instanced at "node_routers"

        for router in node_routers:
            self.node_routers.append(Node(name, router[0], router[1], None, self.arp_table))

    def __str__(self):
        
        output = "<" + self.name + "><" + str(self.num_ports) + "> \n\t" 
        
        for elem in self.node_routers:
            output += str(elem) + ' \n\t'
        for elem in self.arp_table:
            output += elem
        
        return output

class Routertable:
    def __init__(self, name, dest_prefix, nexthop, port):
        self.name = name
        self.dest_prefix = dest_prefix
        self.nexthop = nexthop
        self.port = port
        self.size = len(name)

    def __str__(self):
        output = ""
        for i in range(len(self.name)):
            output += "\t<" + self.name[i] + "><" + str(self.dest_prefix[i]) + "><" + str(self.nexthop[i]) + "><" + str(self.port[i]) + ">\n" 
        return output
        
