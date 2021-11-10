import Utils
import Protocols
from Topology import Node
from Topology import Router
from Topology import Routertable
from Topology import Topology

def send(packet, topology):
    # send for every node at the same network
    if packet.MAC_dst == ":FF": #mac_broadcast:
        arp = packet.unpack()
        for n in topology.nodes:
            #envia pra todo mundo menos pra sí mesmo
            if Utils.ipsAreInTheSameNetwork(n.ip_prefix, arp.IP_dst) and n.ip_prefix != arp.IP_src:
                receive(n, packet, topology)
                
        for n in topology.routers[0].node_routers:
            #envia pra todo mundo menos pra sí mesmo
            if Utils.ipsAreInTheSameNetwork(n.ip_prefix, arp.IP_dst) and n.ip_prefix != arp.IP_src:
                receive(n, packet, topology)
                
    # send to a specific mac address
    else:
        arp = packet.unpack()
        for n in topology.nodes:
            if (n.mac == arp.MAC_dst):
                receive(n, packet, topology)
                break

        for n in topology.routers[0].node_routers:
            if (n.mac == arp.MAC_dst):
                receive(n, packet, topology)
                #update arp_taple from router
                break

def receive(node, packet, topology):
    if packet.isArp():
        arp = packet.unpack()
        
        if arp.IP_dst != node.ip_prefix:
            print("NODO DESCARTOU PACOTE:", str(node))
            print(packet)
        else:
            print("NODO RECEBEU PACOTE:", str(node))
            print(packet)
        
            if arp.isArpRequest():
                node.arp_table[arp.IP_src] = arp.MAC_src
                new_ARP_packet = Protocols.ARP_Reply(node, arp) 
                new_Eth_packet = Protocols.Ethernet(new_ARP_packet.MAC_dst, new_ARP_packet.MAC_src, "ARP" , new_ARP_packet, None)
                send(new_Eth_packet, topology)
            elif arp.isArpReply():
                node.arp_table[arp.IP_src] = arp.MAC_src