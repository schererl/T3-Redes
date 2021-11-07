# T3-Redes

# Integrantes 
Victor Putrich e Bruno Lippert

# Enunciado

O trabalho consiste em desenvolver um simulador de rede. O simulador deve receber como parâmetros de execução o nome de um arquivo de descrição de topologia (conforme formato especificado), um comando (ping ou traceroute), um nó origem e um nó destino. O simulador deve apresentar na saída as mensagens enviadas pelos nós e roteadores da topologia conforme o formato estabelecido.

Formato do arquivo de descrição de topologia

#NODE
<node_name>,<MAC>,<IP/prefix>,<gateway>
#ROUTER
<router_name>,<num_ports>,<MAC0>,<IP0/prefix>,<MAC1>,<IP1/prefix>,<MAC2>,<IP2/prefix> …
#ROUTERTABLE
<router_name>,<net_dest/prefix>,<nexthop>,<port>
Formato de saída

Pacotes ARP Request: Note over <src_name> : ARP Request<br/>Who has <dst_IP>? Tell <src_IP>
Pacotes ARP Reply: <src_name> ->> <dst_name> : ARP Reply<br/><src_IP> is at <src_MAC>
Pacotes ICMP Echo Request: <src_name> ->> <dst_name> : ICMP Echo Request<br/>src=<src_IP> dst=<dst_IP> ttl=<TTL>
Pacotes ICMP Echo Reply: <src_name> ->> <dst_name> : ICMP Echo Reply<br/>src=<src_IP> dst=<dst_IP> ttl=<TTL>
Pacotes ICMP Time Exceeded: <src_name> ->> <dst_name> : ICMP Time Exceeded<br/>src=<src_IP> dst=<dst_IP> ttl=<TTL>

Modo de execução do simulador

$ simulador <topologia> <comando> <origem> <destino>

EXEMPLO:

Arquivo topologia.txt

#NODE
n1,00:00:00:00:00:01,192.168.0.2/24,192.168.0.1
n2,00:00:00:00:00:02,192.168.0.3/24,192.168.0.1
n3,00:00:00:00:00:03,192.168.1.2/24,192.168.1.1
n4,00:00:00:00:00:04,192.168.1.3/24,192.168.1.1
#ROUTER
r1,2,00:00:00:00:00:05,192.168.0.1/24,00:00:00:00:00:06,192.168.1.1/24
#ROUTERTABLE
r1,192.168.0.0/24,0.0.0.0,0
r1,192.168.1.0/24,0.0.0.0,1
Exemplos de execução:

$ simulador topologia.txt ping n1 n2
Note over n1 : ARP Request<br/>Who has 192.168.0.3? Tell 192.168.0.2
n2 ->> n1 : ARP Reply<br/>192.168.0.3 is at 00:00:00:00:00:02
n1 ->> n2 : ICMP Echo Request<br/>src=192.168.0.2 dst=192.168.0.3 ttl=8
n2 ->> n1 : ICMP Echo Reply<br/>src=192.168.0.3 dst=192.168.0.2 ttl=8
$ simulador topologia.txt ping n1 n3
Note over n1 : ARP Request<br/>Who has 192.168.0.1? Tell 192.168.0.2
r1 ->> n1 : ARP Reply<br/>192.168.0.1 is at 00:00:00:00:00:05
n1 ->> r1 : ICMP Echo Request<br/>src=192.168.0.2 dst=192.168.1.2 ttl=8
Note over r1 : ARP Request<br/>Who has 192.168.1.2? Tell 192.168.1.1
n3 ->> r1 : ARP Reply<br/>192.168.1.2 is at 00:00:00:00:00:03
r1 ->> n3 : ICMP Echo Request<br/>src=192.168.0.2 dst=192.168.1.2 ttl=7
n3 ->> r1 : ICMP Echo Reply<br/>src=192.168.1.2 dst=192.168.0.2 ttl=8
r1 ->> n1 : ICMP Echo Reply<br/>src=192.168.1.2 dst=192.168.0.2 ttl=7
$ simulador topologia.txt traceroute n1 n3
Note over n1 : ARP Request<br/>Who has 192.168.0.1? Tell 192.168.0.2
r1 ->> n1 : ARP Reply<br/>192.168.0.1 is at 00:00:00:00:00:05
n1 ->> r1 : ICMP Echo Request<br/>src=192.168.0.2 dst=192.168.1.2 ttl=1
r1 ->> n1 : ICMP Time Exceeded<br/>>src=192.168.0.1 dst=192.168.0.2 ttl=8
n1 ->> r1 : ICMP Echo Request<br/>src=192.168.0.2 dst=192.168.1.2 ttl=2
Note over r1 : ARP Request<br/>Who has 192.168.1.2? Tell 192.168.1.1
n3 ->> r1 : ARP Reply<br/>192.168.1.2 is at 00:00:00:00:00:03
r1 ->> n3 : ICMP Echo Request<br/>src=192.168.0.2 dst=192.168.1.2 ttl=1
n3 ->> r1 : ICMP Echo Reply<br/>src=192.168.1.2 dst=192.168.0.2 ttl=8
r1 ->> n1 : ICMP Echo Reply<br/>src=192.168.1.2 dst=192.168.0.2 ttl=7
Detalhes para construção do simulador:

TTL inicial dos pacotes IP deve ser igual a 8
o simulador deverá suportar o uso de subredes na composição da topologia
a topologia poderá apresentar loops de roteamento
a tabela de roteamento pode conter uma rota default representada por 0.0.0.0/0
o simulador deve ser executado a partir de um terminal por linha de comando de acordo com o exemplo apresentado - não deve ser necessário utilizar uma IDE para executar o simulador!!!
o simulador pode ser implementado em qualquer linguagem
a entrada e saída devem respeitar EXATAMENTE os formatos apresentados (inclusive espaços)
o formato de saída é baseado na linguagem mermaid (https://mermaid-js.github.io/mermaid). Sugere-se verificar se a saída está correta através do site https://mermaid-js.github.io/mermaid-live-editor/ (incluir "sequenceDiagram" no topo da saída)
