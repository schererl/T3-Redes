import Utils
import Protocols
from Topology import Node
from Topology import Router
from Topology import Routertable
from Topology import Topology

def send(pkg, topology):
    # send for every node at the same network ARP REQUEST
    if pkg.MAC_dst == ":FF": #mac_broadcast:
        arp = pkg.unpack()
        print("Note over "+ arp.src_name +" : ARP Request<br/>Who has "+ arp.IP_dst.split("/")[0] +"? Tell "+ arp.IP_src.split("/")[0])
        for n in topology.nodes:
            #envia pra todo mundo menos pra sí mesmo
            if Utils.ipsAreInTheSameNetwork(n.ip_prefix, arp.IP_dst) and n.ip_prefix != arp.IP_src:
                receive(n, pkg, topology)
                
        for n in topology.routers[0].node_routers:
            #envia pra todo mundo menos pra sí mesmo
            if Utils.ipsAreInTheSameNetwork(n.ip_prefix, arp.IP_dst) and n.ip_prefix != arp.IP_src:
                receive(n, pkg, topology)
                
    # send to a specific mac address ARP REPLY
    else:
        arp = pkg.unpack()
        print(arp.src_name +" ->> "+ arp.dst_name +" : ARP Reply<br/>"+ arp.IP_src.split("/")[0] +" is at "+ arp.MAC_src)
        for n in topology.nodes:
            if (n.mac == arp.MAC_dst):
                receive(n, pkg, topology)
                break

        for n in topology.routers[0].node_routers:
            if (n.mac == arp.MAC_dst):
                receive(n, pkg, topology)
                #update arp_taple from router
                break

def receive(node, pkg, topology):
    if pkg.isArp():
        arp = pkg.unpack()
        
        if arp.IP_dst != node.ip_prefix:
            pass
            # Tem que passar para outros routers caso n seja esse?
            # print("NODO DESCARTOU PACOTE:", str(node))
            # print(pkg)
        else:
            # print("NODO RECEBEU PACOTE:", str(node))
            # print(pkg)
        
            if arp.isArpRequest():
                node.arp_table[arp.IP_src] = arp.MAC_src
                new_ARP_pkg = Protocols.ARP_Reply(node, arp, arp.src_name) 
                new_Eth_pkg = Protocols.Ethernet(new_ARP_pkg.MAC_dst, new_ARP_pkg.MAC_src, "ARP" , new_ARP_pkg, None)
                send(new_Eth_pkg, topology)
            elif arp.isArpReply():
                node.arp_table[arp.IP_src] = arp.MAC_src