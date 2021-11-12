import Utils
import Network
import Protocols

from Topology import Node
from Topology import Router
from Topology import Routertable
from Topology import Topology

node1 = Node("n1","00:00:00:00:00:01","192.168.0.2/24","5","192.168.0.1", {})
node2 = Node("n2","00:00:00:00:00:02","192.168.0.3/24","5","192.168.0.1", {})
node3 = Node("n3","00:00:00:00:00:03","192.168.1.2/24","5","192.168.1.1", {})
node4 = Node("n4","00:00:00:00:00:04","192.168.1.3/24","5","192.168.1.1", {})
nodes = [node1, node2, node3, node4]

router = Router("r1", 2, [ ["00:00:00:00:00:05","192.168.0.1/24"], ["00:00:00:00:00:06", "192.168.1.1/24"] ] )
routersList = [router]

router_table = Routertable( ["r1", "r1"], ["192.168.0.0/24", "192.168.1.0/24"], ["0.0.0.0","0.0.0.0"], ["0","1"] )

topo = Topology(nodes, routersList, router_table)

# print(topo)

#arp_packet = Protocols.ARP_Request(node1, node3.ip_prefix)
#eth_packet = Protocols.Ethernet(node1.mac, ":FF", "ARP", arp_packet)
#Network.send(eth_packet, topo)
#print(node1.arp_table)
#print(node3.arp_table)
#print(routersList[0].node_routers[0].arp_table)




ARP_packet = Protocols.ARP_Request(node1, node1.gateway + "/24")
Ethernet_packet = Protocols.Ethernet(node1.mac, ":FF", "ARP", ARP_packet)
Network.send(Ethernet_packet, topo)




icmp_pkg = Protocols.ICMP_Echo_Request()
ip_package = Protocols.IP(node1.ip_prefix, node3.ip_prefix, "ICMP", icmp_pkg)
# O mac de destino tera que pegar do ARP reply ******IMPORTANTE**********
eth_packet = Protocols.Ethernet(node1.mac, node1.arp_table[node1.gateway+"/24"], "IP", ip_package)

Network.send(eth_packet, topo)
'''


def ping(node1, n2_ip):
    dst_ip = None
    # 1: node1 & node2_ip tão na mesma rede ?
    if Utils.ipsAreInTheSameNetwork(node1.ip_prefix, n2_ip):
        dst_ip = n2_ip
    else:
        dst_ip = node1.gateway


    #     tem MAC?
        if not dst_ip in node1.arp_table:
    #     não -> send(ARP_REQUEST(n1.ip, n2.ip)) | send(ICMP_REQUEST(n1, n2))
            arp_packet = Protocols.ARP_REQUEST(n1, dst_ip)
    
    #     sim -> send(ICMP_REQUEST(n1, n2))
        ICMP_packet = Protocols.ICMP_Echo_Request()
        IP_packet = IP(node1.ip_prefix, node2.ip_prefix, icmp_pkg)
        Ethernet_packet = Ethernet(node1.mac, dst.mac, "IP", IP_packet)
        Network.send(Ethernet_packet)

                                

    


'''

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