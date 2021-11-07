import Utils
from Topology import Node
from Topology import Router
from Topology import Routertable
from Topology import Topology

node0 = Node("n1","00:00:00:00:01:01","10.0.0.1/16", "5", "10.0.0.3")
node1 = Node("n2","00:00:00:00:01:02","10.0.0.2/16","5","10.0.0.3")
node2 = Node("n3","00:00:00:00:02:01","10.20.0.1/16","5","10.20.0.2")

router = Router("r1", "2", [("00:00:00:00:01:03", "10.0.0.3/16"), ("00:00:00:00:02:02", "10.20.0.2/16")])

topo = Topology([node0, node1, node2], [router], None)

print(topo)
print(Utils.apply_mask("196.175.5.4/16"))

'''
n1,00:00:00:00:01:01,10.0.0.1/16,5,10.0.0.3
n2,00:00:00:00:01:02,10.0.0.2/16,5,10.0.0.3
n3,00:00:00:00:02:01,10.20.0.1/16,5,10.20.0.2
#ROUTER
r1,2,00:00:00:00:01:03,10.0.0.3/16,5,00:00:00:00:02:02,10.20.0.2/16
#ROUTERTABLE
r1,10.0.0.0/16,0.0.0.0,0
r1,10.20.0.0/16,0.0.0.0,1

'''