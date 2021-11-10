def bin_dec(bin):
    decimal = int(bin, 2)
    return decimal
   
'''
example
ip: 192.168.0.2 str_cidr: 24
    mask = [ int([11111111]), int([11111111]), int([11111111]), int([00000000]) ]
    result = ip & mask
'''
def apply_mask(ip__cidr):
    aux = ip__cidr.split("/")
    ip_addr = aux[0]
    cidr = int(aux[1])
    
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

def ipsAreInTheSameNetwork(ip1, ip2):
    return apply_mask(ip1) == apply_mask(ip2)