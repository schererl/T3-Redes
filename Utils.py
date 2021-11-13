from Topology import Node
from Topology import Router
from Topology import Routertable
from Topology import Topology

def bin_dec(bin):
    decimal = int(bin, 2)
    return decimal
   
'''
example
ip: 192.168.0.2 str_cidr: 24
    mask = [ int([11111111]), int([11111111]), int([11111111]), int([00000000]) ]
    result = ip & mask
'''
def apply_mask(ip_addr, cidr):
    mask_r = mask(cidr)
    ip = ip_addr.split(".")
    result = []
    for i in range(len(ip)):
        result.append( str(int(ip[i]) & mask_r[i]) )
        
    return '.'.join(result)
        
def mask(cidr):
    mask_2 = []
    mask_10 = []
    splitter = 0
    mask_2.append([])
    
    for it in range(32): # size ip address = 32
        if(splitter == 8):
            splitter = 0
            mask_10.append(bin_dec(''.join(mask_2[-1])))
            mask_2.append([])
        
        if it < cidr:
            mask_2[-1].append('1')
        else:
            mask_2[-1].append('0')
        
        splitter+=1
    
    mask_10.append(bin_dec( ''.join( mask_2[-1] ) ))
            
    return mask_10

def getMask(ip):
    aux = ip.split("/")
    return "/" + aux[1]

def ipsAreInTheSameNetwork(ip1, ip2):
    # 127.255.52.10/17 127.255.53.15/16 
    aux = ip1.split("/")
    ip1, cidr1 = aux[0], aux[1]
    aux = ip2.split("/")
    ip2, cidr2 = aux[0], aux[1]
    
    return apply_mask(ip1, int(cidr1)) == apply_mask(ip2, int(cidr1))

def readTopologyFile(filePath):
    nodesList = []
    routersList = []
    routerTable = None
    nodesNames = {}

    f = open(filePath, 'r')

    # Nodes loader
    line = f.readline()
    while True:
        line = f.readline().replace("\n", "")
        if line == "#ROUTER":
            break
        n = line.split(",")
        nodesList.append(Node(n[0], n[1], n[2], n[3], {}))
        nodesNames[n[1]] = n[0]

    # Routers loader
    while True:
        line = f.readline().replace("\n", "")
        if line == "#ROUTERTABLE":
            break
        r = line.split(",")
        macIpList = []
        for i in range(2, len(r), 2):
            macIpList.append([r[i], r[i+1]])
            nodesNames[r[i]] = r[0]

        routersList.append(Router(r[0], r[1], macIpList))

    # RouterTable loader
    routsNames = []
    routsIps = []
    routsHops = []
    routsPorts = []
    while True:
        line = f.readline().replace("\n", "")
        if not line:
            break
        r = line.split(",")

        routsNames.append(r[0])
        routsIps.append(r[1])
        routsHops.append(r[2])
        routsPorts.append(r[3])
    
    routerTable = Routertable(routsNames, routsIps, routsHops, routsPorts)
    return Topology(nodesList, routersList, routerTable, nodesNames)