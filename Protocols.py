import Utils
from enum import Enum
from Topology import Node
from Topology import Router
from Topology import Routertable
from Topology import Topology

class Ethernet:
    def __init__(self, MAC_dst, MAC_src, protocolType, data, crc):
        self.MAC_src = MAC_src
        self.MAC_dst = MAC_dst
        self.protocolType = protocolType # IP or ARP
        self.data = data 
        self.crc = crc     # não sei ao certo

    def isArp(self):
        return self.protocolType == "ARP"

    def unpack(self):
        return self.data

    def __str__(self):
        output = "[ eth_packet:\n"
        output += "\t mac source:  " + str(self.MAC_src) + "\n"
        output += "\t mac destiny: " + str(self.MAC_dst) + "\n"
        output += "\t type: " + str(self.protocolType) + "\n"
        output += "\t data: " + str(self.data) + "\n"
        output += "]"
        return output
        
class IP:
    def __init__(self, IP_dst, IP_src, data, protocolType="ICMP", ttl=8):
        self.IP_src = IP_src
        self.IP_dst = IP_dst
        self.data = data #ICMP
        self.protocolType = protocolType
        self.ttl = ttl

    def unpack(self):
        return self.data

class ICMPType(Enum):
    NOTIFICAO_DE_ERRO = 1
    CONSULTA = 2

class ICMPCode(Enum):
    DESTINATION_UNREACHBLE = 3
    TIME_EXEEDED = 11
    ECHO_REQUEST = 8
    ECHO_REPLY = 0

class ICMP:
    def __init__(self, typeMessage, code):
        self.typeMessage = typeMessage 
        self.code = code
    
class ARP:
    def __init__(self, src_name, MAC_src, MAC_dst, IP_dst, IP_src, operation):
        self.src_name = src_name
        self.MAC_src  = MAC_src
        self.MAC_dst  = MAC_dst 
        self.IP_dst   = IP_dst
        self.IP_src    = IP_src
        self.operation = operation # 1 request 2 reply 

    def isArpRequest(self):
        return self.operation == 1

    def isArpReply(self):
        return self.operation == 2
        
    def __str__(self):
        output = "[ arp_packet:\n"
        output += "\t\t\t mac source:  " + str(self.MAC_src)   + "\n"
        output += "\t\t\t mac destiny: " + str(self.MAC_dst)   + "\n"
        output += "\t\t\t ip source:   " + str(self.IP_src)    + "\n"
        output += "\t\t\t ip destiny:  " + str(self.IP_dst)    + "\n"
        output += "\t\t\t operation:   " + str(self.operation) + "\n"
        output += "\t\t]"
        return output

    
def ARP_Request(src_node, dst_ip):
    src_mac = src_node.mac
    dst_mac = None
    
    # first, check if they are in the same network
    if Utils.ipsAreInTheSameNetwork(src_node.ip_prefix, dst_ip):
        return ARP(src_node.name, src_node.mac, None, dst_ip, src_node.ip_prefix, 1) #ARP Request to destiny
    else: #TODO: I believe that you cant send ARP to a node outside
        cidr = (src_node.ip_prefix.split("/"))[1] #apply src_node's mask at gateway's ip addr
        return ARP(src_node.name, src_node.mac, None, src_node.gateway + "/" + cidr, src_node.ip_prefix, 1)  #ARP Request to default Router

def ARP_Reply(node, arp):
    return ARP(node.name, node.mac, arp.MAC_src, arp.IP_src, node.ip_prefix, 2) # reply