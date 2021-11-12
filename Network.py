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
        #print("Note over "+ pkg.src_name +" : ARP Request<br/>Who has "+ arp.IP_dst.split("/")[0] +"? Tell "+ arp.IP_src.split("/")[0])
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
        #print(pkg.src_name +" ->> "+ pkg.dst_name +" : ARP Reply<br/>"+ arp.IP_src.split("/")[0] +" is at "+ arp.MAC_src)
        for n in topology.nodes:
            if (n.mac == arp.MAC_dst):
                receive(n, pkg, topology)
                break

        for router in topology.routers:
            for n in router.node_routers:
                
                if (n.mac == arp.MAC_dst):
                    receive(n, pkg, topology)
                    #update arp_taple from router
                    break

def sendIp(pkg, topology):
    for n in topology.nodes:
        if (n.mac == pkg.MAC_dst):
            receive(n, pkg, topology)
            break
    for router in topology.routers:
            print(pkg)
            for n in router.node_routers:
                if (n.mac == pkg.MAC_dst):
                    print("recebeu")
                    receive(n, pkg, topology)
                    #update arp_taple from router
                    break

def receive(node, pkg, topology):
    
    #se o nodo pertence a um roteador, o nodo que recebe deve ser o da mesma rede ou do hop correspondente ao ip_dst do pkg
    if pkg.isArp():
        receiveArp(node, pkg, topology)
    elif pkg.isIp():
        receiveIp(node, pkg, topology)

def receiveArp(node, pkg, topology):
    arp = pkg.unpack()
    print("NODE: " + str(node) + " RECEIVED PKG: ")
    print(pkg)
    if arp.isArpRequest():
        if arp.IP_dst == node.ip_prefix:
            node.arp_table[arp.IP_src] = arp.MAC_src
            new_ARP_pkg = Protocols.ARP_Reply(node, arp) #source é o nodo e o destino é o source do que está no package
            new_Eth_pkg = Protocols.Ethernet(new_ARP_pkg.MAC_src, new_ARP_pkg.MAC_dst, "ARP" , new_ARP_pkg)
            send(new_Eth_pkg, topology)
    elif arp.isArpReply():
        node.arp_table[arp.IP_src] = arp.MAC_src

def receiveIp(node, pkg, topology):
    ip = pkg.unpack()

    print("NODE: " + str(node) + " RECEIVED PKG: ")
    print(pkg)

    # TTL = 0 Send icmp timeout to ip.ip_source
    if ip.ttl == 0 and ip.protocolType == "ICMP":

        new_ICMP_pkg = ICMP(11, 1) # icmp timeout
        new_IP_pkg = IP(node.ip_prefix, ip.src, "ICMP", new_ICMP_pkg, ttl=8) #manda de quem recebeu o pkg para quem enviou ele
        
        if not ip.IP_src in node.arp_table:
            ARP_packet = Protocols.ARP_Request(node, ip.src)
            Ethernet_packet = Protocols.Ethernet(node.mac, ":FF", "ARP", ARP_Packet)
            send(Ethernet_packet, topology)

        # source = node.mac | destiny = pkg.src.mac 
        new_Eth_pkg = (node.mac, node.arp_table[ip.src], "IP", new_IP_pkg)
        send(new_Eth_pkg, topology)

    # CHECK if they arent in the same network
    if not Utils.ipsAreInTheSameNetwork(node.ip_prefix, ip.IP_dst):
        #verifica se foi o roteador que o recebeu pkg
        node_is_router = topology.check_if_node_is_router(node)
        # se foi, redireciona para a rede  do destino e que consta na router_table  *decrementando o ttl
        if node_is_router:
            redirect_newtwork(node, ip, topology)
        #caso contrário, redireciona pro gateway a default
        else:
            redirect_default_gateway(node, ip, topology)

    else: #IF they are in the same network
        receiveICMP(node, pkg, topology)

def receiveICMP(node, pkg, topology):
    ip = pkg.unpack()
    icmp = ip.unpack()
        
    if icmp.typeMessage == Protocols.ICMPType.CONSULTA: #Request or reply
        if icmp.code == Protocols.ICMPCode.ECHO_REQUEST: #Echo request
            new_ip_src = ip.IP_dst
            new_ip_dst = ip.IP_src

            new_mac_src = node.mac
            new_mac_dst = None
            
            icmp_pkg = Protocols.ICMP_Echo_Reply()
            IP_packet = Protocols.IP(new_ip_src, new_ip_dst, "ICMP", icmp_pkg) #não muda nada
            
            #verifica se o reply tem que passar pelo gateway ou não
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
            #message received
            return

#redirects the mac_destiny to gatey's mac
def redirect_default_gateway(node, ip, topology):
    #redireciona o envio do pacote para o gateway
    dst_ip = node.gateway + Utils.getMask(node.ip_prefix) # set mac_adress to gateway
    if not dst_ip in node.arp_table: # if dont know gateway's mac adress, discover it 
        ARP_packet = Protocols.ARP_Request(node, dst_ip)
        Ethernet_packet = Protocols.Ethernet(node.mac, ":FF", "ARP", ARP_packet)
        
    
    Ethernet_packet = Protocols.Ethernet(node.mac, node.arp_table[dst_ip], "IP", ip)
    print("NODE " + str(node) + " SEND PACKAGE TO ROUTER")
    print(Ethernet_packet)
    send(Ethernet_packet, topology)
    
#redirects to another network using the router
def redirect_newtwork(node, ip, topology):
    router = topology.get_router_by_node(node)
        
    for rt_line in range(topology.routertable.size): # pra isso tem que olhar na router_table o que fazer
        
        rt_name = topology.routertable.name[rt_line]
        rt_ip = topology.routertable.dest_prefix[rt_line]
        rt_interface = topology.routertable.nexthop[rt_line]
        rt_porta = topology.routertable.port[rt_line]
            
        if rt_name == node.name and Utils.ipsAreInTheSameNetwork(ip.IP_dst, rt_ip):#se a linha da router_table pertencerem ao roteador que recebeu a mensagem
            router_node = router.node_routers[int(rt_porta)] #pega o nodo correspondente ao ip da router_table
            if rt_interface == "0.0.0.0": # se não precisa de salto
            #envia ICMP direto para o destino
                if not ip.IP_dst in router.arp_table:
                    ARP_packet = Protocols.ARP_Request(router_node, ip.IP_dst)
                    Ethernet_packet = Protocols.Ethernet(router_node.mac, ":FF", "ARP", ARP_packet)
                    send(Ethernet_packet, topology)
                
                IP_packet = Protocols.IP(ip.IP_src, ip.IP_dst, "ICMP", ip.data, ip.ttl-1) #decrementa ttl já que passou por um roteador
                Ethernet_packet = Protocols.Ethernet(router_node.mac, router.arp_table[ip.IP_dst], "IP", IP_packet)
                
                print("SEND PACKAGE FROM ROUTER")
                print(Ethernet_packet)
                send(Ethernet_packet, topology)
                return
            else:
                #envia ICMP para o proximo hop
                return


#TODO: VER PORQUE O PACOTE DO ECHO REPLY ESTA ENVIADO PARA DO :03 PARA O :06 E O PACOTE NÃO ESTÁ CHEGANDO