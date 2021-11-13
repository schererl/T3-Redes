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
        print("Note over "+ topology.nodes_names[pkg.MAC_src] +" : ARP Request<br/>Who has "+ arp.IP_dst.split("/")[0] +"? Tell "+ arp.IP_src.split("/")[0])
        for n in topology.nodes:
            #envia pra todo mundo menos pra sí mesmo
            if Utils.ipsAreInTheSameNetwork(arp.IP_src, n.ip_prefix) and n.ip_prefix != arp.IP_src:
                receive(n, pkg, topology)
                
        for router in topology.routers:
            for n in router.node_routers:
            #envia pra todo mundo menos pra sí mesmo
                if Utils.ipsAreInTheSameNetwork(arp.IP_src, n.ip_prefix) and n.ip_prefix != arp.IP_src:
                    receive(n, pkg, topology)


    else: # send to a specific mac address ARP REPLY
        print(topology.nodes_names[pkg.MAC_src] +" ->> "+ topology.nodes_names[pkg.MAC_dst] +" : ARP Reply<br/>"+ arp.IP_src.split("/")[0] +" is at "+ arp.MAC_src)
        for n in topology.nodes:
            if (n.mac == arp.MAC_dst):
                receive(n, pkg, topology)
                break

        for router in topology.routers:
            for n in router.node_routers:
                
                if (n.mac == arp.MAC_dst):
                    receive(n, pkg, topology)
                    break

def sendIp(pkg, topology):
    for n in topology.nodes:
        if (n.mac == pkg.MAC_dst):
            receive(n, pkg, topology)
            break
    for router in topology.routers:
            for n in router.node_routers:
                if (n.mac == pkg.MAC_dst):
                    receive(n, pkg, topology)
                    break

def receive(node, pkg, topology):
    if pkg.isArp():
        receiveArp(node, pkg, topology)
    elif pkg.isIp():
        receiveIp(node, pkg, topology)

def receiveArp(node, pkg, topology):
    # print("NODE: " + str(node) + " RECEIVED PKG: ")
    # print(pkg)
    
    arp = pkg.unpack()
    if arp.isArpRequest():
        if arp.IP_dst == node.ip_prefix:
            node.arp_table[arp.IP_src] = arp.MAC_src
            new_ARP_pkg = Protocols.ARP_Reply(node, arp) #source é o nodo e o destino é o source do que está no package
            new_Eth_pkg = Protocols.Ethernet(new_ARP_pkg.MAC_src, new_ARP_pkg.MAC_dst, "ARP" , new_ARP_pkg)
            send(new_Eth_pkg, topology)
    elif arp.isArpReply():
        node.arp_table[arp.IP_src] = arp.MAC_src

def receiveIp(node, pkg, topology):
    # print("NODE: " + str(node) + " RECEIVED PKG: ")
    # print(pkg)
    ip = pkg.unpack()
    if ip.unpack().typeMessage == Protocols.ICMPType.CONSULTA: 
        if ip.unpack().code == Protocols.ICMPCode.ECHO_REQUEST:
            print(topology.nodes_names[pkg.MAC_src] + " ->> " + topology.nodes_names[pkg.MAC_dst] +
            " : ICMP Echo Request<br/>src=" + ip.IP_src.split("/")[0] +" dst=" + ip.IP_dst.split("/")[0] +" ttl=" + str(ip.ttl))
        else:
            print(topology.nodes_names[pkg.MAC_src] + " ->> " + topology.nodes_names[pkg.MAC_dst] +
            " : ICMP Echo Reply<br/>src=" + ip.IP_src.split("/")[0] +" dst=" + ip.IP_dst.split("/")[0] +" ttl=" + str(ip.ttl))
    else:
        print(topology.nodes_names[pkg.MAC_src] + " ->> " + topology.nodes_names[pkg.MAC_dst] +
            " : ICMP Time Exceeded<br/>src=" + ip.IP_src.split("/")[0] +" dst=" + ip.IP_dst.split("/")[0] +" ttl=" + str(ip.ttl))
    
    # TTL = 0 Send icmp timeout to ip.ip_source
    if ip.ttl == 0 and ip.protocolType == "ICMP":
        ip = Protocols.IP(node.ip_prefix, ip.IP_src, "ICMP", Protocols.ICMP(Protocols.ICMPType.NOTIFICAO_DE_ERRO, Protocols.ICMPCode.TIME_EXEEDED))

    # if the node that received the pkg isnt in the same network of ip_destiny there is two option:
    #   1 the node must redirect its message to its gateway
    #   2 the node is a gateway and it must search on router_table where it must sends the package
    if not Utils.ipsAreInTheSameNetwork(node.ip_prefix, ip.IP_dst):
        if topology.check_if_node_is_router(node):
            redirect_newtwork(node, ip, topology)
        else:
            redirect_default_gateway(node, ip, topology)

    else: # else the package has arrived to its destiny
        receiveICMP(node, pkg, topology) # unpack icmp

def receiveICMP(node, pkg, topology):
    ip = pkg.unpack()
    icmp = ip.unpack()
        
    # unpack icmp and send echo_reply
    if icmp.typeMessage == Protocols.ICMPType.CONSULTA: 
        if icmp.code == Protocols.ICMPCode.ECHO_REQUEST:
            new_ip_src = ip.IP_dst
            new_ip_dst = ip.IP_src
            new_mac_src = node.mac
            new_mac_dst = None
            
            icmp_pkg = Protocols.ICMP_Echo_Reply()
            IP_packet = Protocols.IP(new_ip_src, new_ip_dst, "ICMP", icmp_pkg) #não muda nada
            
            # when it receives the message, there is two options:
            #   1 node.ip and new_ip_destiny are from  different networks, must send to node's gateway
            #   2 the node and new_ip_destiny are from the same network, send echo reply directply to destiny
            if not Utils.ipsAreInTheSameNetwork(new_ip_src, new_ip_dst):
                redirect_default_gateway(node, IP_packet, topology)
            else:
                if not ip.IP_src in node.arp_table:
                    ARP_packet = Protocols.ARP_Request(node, ip.IP_src)
                    Ethernet_packet = Protocols.Ethernet(node.mac, ":FF", "ARP", ARP_packet)
                    send(Ethernet_packet, topology)
                eth_packet = Protocols.Ethernet(node.mac, node.arp_table[ip.IP_src], "IP", IP_packet)
                send(eth_packet, topology)

        elif icmp.code == Protocols.ICMPCode.ECHO_REPLY:
            #message received do something here
            return
    else:
        #message received do something here
        return

#redirects the mac_destiny to gatey's mac
def redirect_default_gateway(node, ip, topology):
    dst_ip = node.gateway + Utils.getMask(node.ip_prefix) # set mac_adress to gateway and apply node's ip cidr
    if not dst_ip in node.arp_table: # if dont know gateway's mac adress, discover it 
        ARP_packet = Protocols.ARP_Request(node, dst_ip)
        Ethernet_packet = Protocols.Ethernet(node.mac, ":FF", "ARP", ARP_packet)
        
    
    Ethernet_packet = Protocols.Ethernet(node.mac, node.arp_table[dst_ip], "IP", ip)
    send(Ethernet_packet, topology)
    
#redirects to another network using the router
def redirect_newtwork(node, ip, topology):
    router = topology.get_router_by_node(node)
    IP_packet = None

    for rt_line in range(topology.routertable.size): 
        rt_name = topology.routertable.name[rt_line]
        rt_ip = topology.routertable.dest_prefix[rt_line]
        rt_interface = topology.routertable.nexthop[rt_line]
        rt_porta = topology.routertable.port[rt_line]

        # search for the right line at router_table (same name and same network from ip_destiny)
        if rt_name == node.name and Utils.ipsAreInTheSameNetwork(ip.IP_dst, rt_ip):
            router_node = router.node_routers[int(rt_porta)] # get the right node form router by the port number at router_table
            arp_ip = None
            
            #two options: 1) next network is the same of the destiny
                        # 2) must use the hop to the next network pointed as the one that you must go to achieve destiny's network
            if rt_interface == "0.0.0.0": 
                arp_ip = ip.IP_dst # next mac is the destiny 
            else:
                arp_ip = rt_interface + Utils.getMask(router_node.ip_prefix) # next mac is the next hop

            IP_packet = Protocols.IP(ip.IP_src, ip.IP_dst, "ICMP", ip.data, ip.ttl-1) #decrementa ttl já que passou por um roteador
                
            if not arp_ip in router.arp_table:
                ARP_packet = Protocols.ARP_Request(router_node, arp_ip)
                Ethernet_packet = Protocols.Ethernet(router_node.mac, ":FF", "ARP", ARP_packet)
                send(Ethernet_packet, topology)
            
            Ethernet_packet = Protocols.Ethernet(router_node.mac, router.arp_table[arp_ip], "IP", IP_packet)
            send(Ethernet_packet, topology)
            
            '''    
                #envia ICMP direto para o destino
                if not ip.IP_dst in router.arp_table:
                    ARP_packet = Protocols.ARP_Request(router_node, ip.IP_dst)
                    Ethernet_packet = Protocols.Ethernet(router_node.mac, ":FF", "ARP", ARP_packet)
                    send(Ethernet_packet, topology)
                IP_packet = Protocols.IP(ip.IP_src, ip.IP_dst, "ICMP", ip.data, ip.ttl-1) #decrementa ttl já que passou por um roteador
                Ethernet_packet = Protocols.Ethernet(router_node.mac, router.arp_table[ip.IP_dst], "IP", IP_packet)
                send(Ethernet_packet, topology)
                return
            else:
                #envia ICMP para o proximo hop
                hop_ip = rt_interface + Utils.getMask(router_node.ip_prefix)
                
                if not hop_ip in router.arp_table:
                    ARP_packet = Protocols.ARP_Request(router_node, hop_ip)
                    Ethernet_packet = Protocols.Ethernet(router_node.mac, ":FF", "ARP", ARP_packet)
                    send(Ethernet_packet, topology)
                
                IP_packet = Protocols.IP(ip.IP_src, ip.IP_dst, "ICMP", ip.data, ip.ttl-1) #decrementa ttl já que passou por um roteador
                Ethernet_packet = Protocols.Ethernet(router_node.mac, router.arp_table[hop_ip], "IP", IP_packet)
                send(Ethernet_packet, topology)
                return
            '''

