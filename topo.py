from mininet.topo import Topo
import sys

class Topo(Topo):
    def build(self, num_switches=2):
        switches = [self.addSwitch(f's{i}') for i in range(1, num_switches + 1)]
        for i in range(num_switches - 1):
            self.addLink(switches[i], switches[i + 1])
        host1 = self.addHost('h1')
        self.addLink(switches[0], host1)
        host2 = self.addHost('h2')
        self.addLink(switches[-1], host2)

topos = { 'customTopo': Topo }