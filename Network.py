import Utils
import Protocols
from Topology import Node
from Topology import Router
from Topology import Routertable
from Topology import Topology

def send(pkg, topology):
    if pkg.isArp():
        sendArp(pkg, topology)
    elif pkg.isIp():
        sendIp(pkg, topology)

def sendArp(pkg, topology):
    arp = pkg.unpack()

    # send for every node at the same network ARP REQUEST
    if pkg.MAC_dst == ":FF": # mac_broadcast:
        print("Note over "+ pkg.src_name +" : ARP Request<br/>Who has "+ arp.IP_dst.split("/")[0] +"? Tell "+ arp.IP_src.split("/")[0])
        for n in topology.nodes:
            #envia pra todo mundo menos pra sí mesmo
            if Utils.ipsAreInTheSameNetwork(n.ip_prefix, arp.IP_dst) and n.ip_prefix != arp.IP_src:
                receive(n, pkg, topology)
                
        for n in topology.routers[0].node_routers:
            #envia pra todo mundo menos pra sí mesmo
            if Utils.ipsAreInTheSameNetwork(n.ip_prefix, arp.IP_dst) and n.ip_prefix != arp.IP_src:
                receive(n, pkg, topology)
    else: # send to a specific mac address ARP REPLY
        print(pkg.src_name +" ->> "+ pkg.dst_name +" : ARP Reply<br/>"+ arp.IP_src.split("/")[0] +" is at "+ arp.MAC_src)
        for n in topology.nodes:
            if (n.mac == arp.MAC_dst):
                receive(n, pkg, topology)
                break

        for n in topology.routers[0].node_routers:
            if (n.mac == arp.MAC_dst):
                receive(n, pkg, topology)
                #update arp_taple from router
                break

def sendIp(pkg, topology):
    ip = pkg.unpack()
    icmp = ip.unpack()

    if icmp.typeMessage == Protocols.ICMPType.CONSULTA: #Request or reply
        if icmp.code == Protocols.ICMPCode.ECHO_REQUEST: #Echo request
            print(pkg.src_name + " ->> " + pkg.dst_name + " : ICMP Echo Request<br/>src=" + ip.IP_src.split("/")[0] + " dst=" + ip.IP_dst.split("/")[0] + " ttl=" + str(ip.ttl))
            for n in topology.nodes:
                if n.ip_prefix == ip.IP_dst:
                    receive(n, pkg, topology)
                    break
        if icmp.code == Protocols.ICMPCode.ECHO_REPLY: #Echo reply
            print(pkg.src_name + " ->> " + pkg.dst_name + " : ICMP Echo Reply<br/>src=" + ip.IP_src.split("/")[0] + " dst=" + ip.IP_dst.split("/")[0] + " ttl=" + str(ip.ttl))

def receive(node, pkg, topology):
    if pkg.isArp():
        receiveArp(node, pkg, topology)
    elif pkg.isIp():
        receiveIp(node, pkg, topology)

def receiveArp(node, pkg, topology):
    arp = pkg.unpack()
    
    if arp.isArpRequest():
        if arp.IP_dst == node.ip_prefix:
            node.arp_table[arp.IP_src] = arp.MAC_src
            new_ARP_pkg = Protocols.ARP_Reply(node, arp, pkg.src_name) 
            new_Eth_pkg = Protocols.Ethernet(new_ARP_pkg.MAC_dst, new_ARP_pkg.MAC_src, "ARP" , new_ARP_pkg, None, node.name, pkg.src_name)
            send(new_Eth_pkg, topology)
    elif arp.isArpReply():
        node.arp_table[arp.IP_src] = arp.MAC_src

def receiveIp(node, pkg, topology):
    ip = pkg.unpack()
    
    #TODO verifica ttl do ip, se for 0, empacota icmp com erro e envia pro endereço source
    if ip.ttl == 0:
        new_ICMP_pkg = ICMP(1, 11)
        new_Eth_pkg = (node.mac, node.arp_table[ip.src], )
    # senão, verifica se o nodo.ip == pkg.ip.destino, se for, decrementa o ttl
    
    icmp = ip.unpack()
    if icmp.typeMessage == Protocols.ICMPType.CONSULTA: #Request or reply
        if icmp.code == Protocols.ICMPCode.ECHO_REQUEST: #Echo request
            icmp_pkg = Protocols.ICMP_Echo_Reply()
            ip_package = Protocols.IP(node.ip_prefix, ip.IP_src, icmp_pkg)
            eth_packet = Protocols.Ethernet(node.mac, pkg.MAC_src, "IP", ip_package, None, node.name, pkg.src_name)
            send(eth_packet, topology)
    elif arp.isArpReply():
        node.arp_table[arp.IP_src] = arp.MAC_src