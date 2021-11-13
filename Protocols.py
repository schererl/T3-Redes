import Utils
from enum import Enum
from Topology import Node
from Topology import Router
from Topology import Routertable
from Topology import Topology

class Ethernet:
    def __init__(self, MAC_src, MAC_dst,  protocolType, data):
        self.MAC_src = MAC_src
        self.MAC_dst = MAC_dst
        self.protocolType = protocolType # IP or ARP
        self.data = data 

    def isArp(self):
        return self.protocolType == "ARP"
    
    def isIp(self):
        return self.protocolType == "IP"

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
    def __init__(self, IP_src, IP_dst, protocolType, data, ttl=8):
        self.IP_src = IP_src
        self.IP_dst = IP_dst
        self.data = data #ICMP
        self.protocolType = protocolType
        self.ttl = ttl

    def unpack(self):
        return self.data

    def __str__(self):
        output = "[ ip_packet:\n"
        output += "\t\t\t ip source:   " + str(self.IP_src)    + "\n"
        output += "\t\t\t ip destiny:  " + str(self.IP_dst)    + "\n"
        output += "\t\t\t ttl: " + str(self.ttl) + "\n"
        output += "\t\t\t protocolType:   " + str(self.protocolType) + "\n"
        output += "\t\t\t data: " + str(self.data) + "\n"
        output += "\t\t]"
        return output

class ICMPType(Enum):
    NOTIFICAO_DE_ERRO = 1
    CONSULTA = 2

class ICMPCode(Enum):
    TIME_EXCEED = 11
    ECHO_REQUEST = 8
    ECHO_REPLY = 0

class ICMP:
    def __init__(self, typeMessage, code):
        self.typeMessage = typeMessage 
        self.code = code
    def __str__(self):
        output_msg = ""
        if self.code == ICMPCode.TIME_EXCEED:
            output_msg = "TIME EXCEEDED"
        elif self.code == ICMPCode.ECHO_REQUEST:
            output_msg = "ECHO_REQUEST"
        elif self.code == ICMPCode.ECHO_REPLY:
            output_msg = "ECHO_REPLY"
        return "[ICMP "+ output_msg + "]"
    
class ARP:
    def __init__(self, MAC_src, MAC_dst, IP_src, IP_dst, operation):
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
    
    return ARP(src_node.mac, None, src_node.ip_prefix, dst_ip,  1) #ARP Request to destiny

def ARP_Reply(node, arp):
    return ARP(node.mac, arp.MAC_src, node.ip_prefix, arp.IP_src, 2) # reply

def ICMP_Echo_Request():
   return ICMP(ICMPType.CONSULTA, ICMPCode.ECHO_REQUEST)

def ICMP_Echo_Reply():
   return ICMP(ICMPType.CONSULTA, ICMPCode.ECHO_REPLY)
