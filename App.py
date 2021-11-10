import Utils
import Network
import Protocols

from Topology import Node
from Topology import Router
from Topology import Routertable
from Topology import Topology

node1 = Node("n1","00:00:00:00:00:01","192.168.0.2/24","5","192.168.0.1")
node2 = Node("n2","00:00:00:00:00:02","192.168.0.3/24","5","192.168.0.1")
node3 = Node("n3","00:00:00:00:00:03","192.168.1.2/24","5","192.168.1.1")
node4 = Node("n4","00:00:00:00:00:04","192.168.1.3/24","5","192.168.1.1")
nodes = [node1, node2, node3, node4]

router = Router("r1", 2, [ ["00:00:00:00:00:05","192.168.0.1/24"], ["00:00:00:00:00:06", "192.168.1.1/24"] ] )
routersList = [router]

router_table = Routertable( ["r1", "r1"], ["192.168.0.0/24", "192.168.1.0/24"], ["0.0.0.0","0.0.0.0"], ["0","1"] )

topo = Topology(nodes, routersList, router_table)

# print(topo)

arp_packet = Protocols.ARP_Request(node1, node3.ip_prefix)
eth_packet = Protocols.Ethernet(":FF", node1.mac, "ARP", arp_packet, None)
Network.send(eth_packet, topo)
# print(node1.arp_table)
# print(router.arp_table)

'''

arp_packet = Protocols.ARP_Request(node2, node3.ip_prefix)
eth_packet = Protocols.Ethernet(":FF", node2.mac, "ARP", arp_packet, None)
Network.send(eth_packet, topo)
print(node2.arp_table)
'''


'''
exemplo 2

#NODE
n1,00:00:00:00:00:01,192.168.0.2/24,192.168.0.1
n2,00:00:00:00:00:02,192.168.0.3/24,192.168.0.1
n3,00:00:00:00:00:03,192.168.1.2/24,192.168.1.1
n4,00:00:00:00:00:04,192.168.1.3/24,192.168.1.1
#ROUTER
r1,2,00:00:00:00:00:05,192.168.0.1/24,00:00:00:00:00:06,192.168.1.1/24
#ROUTERTABLE
r1,192.168.0.0/24,0.0.0.0,0
r1,192.168.1.0/24,0.0.0.0,1



exemplo 1

node0 = Node("n1","00:00:00:00:01:01","10.0.0.1/16", "5", "10.0.0.3")
node1 = Node("n2","00:00:00:00:01:02","10.0.0.2/16","5","10.0.0.3")
node2 = Node("n3","00:00:00:00:02:01","10.20.0.1/16","5","10.20.0.2")
nodes = [node0, node1, node2]

router = Router("r1", "2", [("00:00:00:00:01:03", "10.0.0.3/16"), ("00:00:00:00:02:02", "10.20.0.2/16")])
router_table = Routertable(["r1", "r1"], ["10.0.0.0/16", "10.20.0.0/16"], ["0.0.0.0", "0.0.0.0"], ["0","1"])
topo = Topology(nodes, [router], router_table)


n1,00:00:00:00:01:01,10.0.0.1/16,5,10.0.0.3
n2,00:00:00:00:01:02,10.0.0.2/16,5,10.0.0.3
n3,00:00:00:00:02:01,10.20.0.1/16,5,10.20.0.2
#ROUTER
r1,2,00:00:00:00:01:03,10.0.0.3/16,5,00:00:00:00:02:02,10.20.0.2/16
#ROUTERTABLE
r1,10.0.0.0/16,0.0.0.0,0
r1,10.20.0.0/16,0.0.0.0,1

'''