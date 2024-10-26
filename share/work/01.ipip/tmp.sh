
iptables -A FORWARD -p ipip -d 10.10.2.2 -j DROP

iptables -A FORWARD -p ipip -d 10.10.2.2 -j ACCEPT


sysctl -w net.ipv4.conf.all.rp_filter=0
sysctl -w net.ipv4.conf.default.rp_filter=0
sysctl -w net.ipv4.conf.eth0.rp_filter=0
sysctl -w net.ipv4.conf.lo.rp_filter=0
sysctl -w net.ipv4.conf.peer1.rp_filter=0
sysctl -w net.ipv4.conf.peer2.rp_filter=0
sysctl -w net.ipv4.conf.tunl0.rp_filter=0


net.ipv4.conf.all.rp_filter=0
net.ipv4.conf.default.rp_filter=0
sysctl net.ipv4.conf.eth0.rp_filter=0
sysctl net.ipv4.conf.eth1.rp_filter=0
sysctl net.ipv4.conf.gre0.rp_filter=0
sysctl net.ipv4.conf.gre1.rp_filter=0