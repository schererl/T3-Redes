import Utils
from Topology import Node
from Topology import Router
from Topology import Routertable
from Topology import Topology

class Ethernet:
    def __init__(self, MAC_dst, MAC_src, type_, data, crc):
        self.MAC_src = MAC_src
        self.MAC_dst = MAC_dst
        self.type_ = type_ # IP or ARP
        self.data = data 
        self.crc = crc     # não sei ao certo

    def unpack(self):
        return self.data

    def __str__(self):
        output = "[ eth_packet:\n"
        output += "\t mac source:  " + str(self.MAC_src) + "\n"
        output += "\t mac destiny: " + str(self.MAC_dst) + "\n"
        output += "\t type: " + str(self.type_) + "\n"
        output += "\t data: " + str(self.data) + "\n"
        output += "]"
        return output
        
class IP:
    def __init__(self, IP_dst, IP_src, data, crc):
        self.IP_src = IP_src
        self.IP_src = IP_src
        self.data = data    # ICMP 
        self.crc =  crc     # Echo Request | Echo Reply 
    def unpack(self):
        return self.data
class ARP:
    def __init__(self, src_name, MAC_src, MAC_dst, IP_dst, IP_src, operation):
        self.src_name = src_name
        self.MAC_src  = MAC_src
        self.MAC_dst  = MAC_dst 
        self.IP_dst   = IP_dst
        self.IP_src    = IP_src
        self.operation = operation # 1 request 2 reply 
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
    if Utils.apply_mask(src_node.ip_prefix) == Utils.apply_mask(dst_ip):
        return ARP(src_node.name, src_node.mac, None,  dst_ip, src_node.ip_prefix, 1) #ARP Request to destiny
    else: #TODO: I believe that you cant send ARP to a node outside
        cidr = (src_node.ip_prefix.split("/"))[1] #apply src_node's mask at gateway's ip addr
        return ARP(src_node.name, src_node.mac, None,  src_node.gateway + "/" + cidr, src_node.ip_prefix, 1)  #ARP Request to default Router

def ARP_Reply(node, arp):
    return ARP(node.name, node.mac, arp.MAC_src, arp.IP_src, node.ip_prefix, 2) # reply
        
    

    

