from mininet.topo import Topo

class CustomTopo(Topo):
    def __init__(self, num_switches=2):
        Topo.__init__(self)
        switches = [self.addSwitch(f'switch_{i}') for i in range(1, num_switches + 1)]
        for i in range(num_switches - 1):
            self.addLink(switches[i], switches[i + 1])
        host1 = self.addHost('host_1')
        self.addLink(switches[0], host1)
        host2 = self.addHost('host_2')
        self.addLink(switches[0], host2)
        host3 = self.addHost('host_3')
        self.addLink(switches[-1], host3)
        host4 = self.addHost('host_4')
        self.addLink(switches[-1], host4)

topos = { 'customTopo': CustomTopo }