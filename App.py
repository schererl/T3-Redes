import sys
import Utils
import Network
import Protocols


def ping(nodeOrigem, nodeDestino, topologia):
    dst_ip = None
    if Utils.ipsAreInTheSameNetwork(nodeOrigem.ip_prefix, nodeDestino.ip_prefix):
        dst_ip = nodeDestino.ip_prefix
    else:
        dst_ip = nodeOrigem.gateway + "/" +nodeOrigem.ip_prefix.split("/")[1]

    ARP_packet = Protocols.ARP_Request(nodeOrigem, dst_ip)
    Ethernet_packet = Protocols.Ethernet(nodeOrigem.mac, ":FF", "ARP", ARP_packet)
    Network.send(Ethernet_packet, topo)

    icmp_pkg = Protocols.ICMP_Echo_Request()
    ip_package = Protocols.IP(nodeOrigem.ip_prefix, nodeDestino.ip_prefix, "ICMP", icmp_pkg)
    eth_packet = Protocols.Ethernet(nodeOrigem.mac, nodeOrigem.arp_table[dst_ip], "IP", ip_package)
    Network.send(eth_packet, topo)

def traceroute(nodeOrigem, nodeDestino, topologia):
    dst_ip = None
    if Utils.ipsAreInTheSameNetwork(nodeOrigem.ip_prefix, nodeDestino.ip_prefix):
        dst_ip = nodeDestino.ip_prefix
    else:
        dst_ip = nodeOrigem.gateway + "/" +nodeOrigem.ip_prefix.split("/")[1]

    ARP_packet = Protocols.ARP_Request(nodeOrigem, dst_ip)
    Ethernet_packet = Protocols.Ethernet(nodeOrigem.mac, ":FF", "ARP", ARP_packet)
    Network.send(Ethernet_packet, topo)

    ttlCounter = 1
    while ttlCounter <= 8:
        icmp_pkg = Protocols.ICMP_Echo_Request()
        ip_package = Protocols.IP(nodeOrigem.ip_prefix, nodeDestino.ip_prefix, "ICMP", icmp_pkg, ttl=ttlCounter)
        eth_packet = Protocols.Ethernet(nodeOrigem.mac, nodeOrigem.arp_table[dst_ip], "IP", ip_package)
        res = Network.send(eth_packet, topo)
        if res == Protocols.ICMPCode.ECHO_REPLY or res == None:
            break
        ttlCounter += 1

# le linha de comando
arqTopologia = sys.argv[1]
comando = sys.argv[2]
origem = sys.argv[3]
destino = sys.argv[4]

topo = Utils.readTopologyFile(arqTopologia)
nOrigem = [p for p in topo.nodes if p.name == origem][0] 
nDestino = [p for p in topo.nodes if p.name == destino][0]



if comando == "ping":
    ping(nOrigem, nDestino, topo)
elif comando == "traceroute":
    traceroute(nOrigem, nDestino, topo)
else:
    print("Comando invalido", comando)
