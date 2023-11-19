from nis import match
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
import pox.forwarding.l2_learning
from pox.lib.addresses import EthAddr
import pox.lib.packet as pkt
import json

log = core.getLogger()

class Firewall(EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        self.rules = self._import_rules()
        log.debug("Enabling Firewall Module")

    def _import_rules(self):
        with open("./ext/rules.rules", "r") as f:
            return json.load(f)
        
    def _handle_PacketIn(self, event):
        packet = event.parsed
        log.debug("Received packet: %s", packet)

    def _handle_ConnectionUp(self, event):
        log.debug("Switch %s has come up.", dpidToStr(event.dpid))
        # Agregar reglas al switch cuando se establece la conexión
        for rule in self.rules:
            self.add_rule(rule, event)

    def add_rule(self, rule, event):
        
        match = of.ofp_match()
        match.dl_type = pkt.ethernet.IP_TYPE
        match.dl_src = EthAddr(rule["dl_src"]) if "dl_src" in rule else EthAddr("00:00:00:00:00:00")
        match.dl_dst = EthAddr(rule["dl_dst"]) if "dl_dst" in rule else EthAddr("00:00:00:00:00:00")
        match.tp_dst = int(rule["tp_dst"]) if "tp_dst" in rule else of.OFPFW_ALL
        if "nw_proto" in rule:
            if rule["nw_proto"] == "UDP":    
                match.nw_proto = pkt.ipv4.UDP_PROTOCOL
            elif rule["nw_proto"] == "TCP":
                match.nw_proto = pkt.ipv4.TCP_PROTOCOL
        msg = of.ofp_flow_mod(match=match)
        log.debug("Adding rule: %s", str(rule))
        log.debug("Sending flow mod: %s", str(msg))
        event.connection.send(msg)
        log.debug("Rule added and flow mod sent.")
        

def launch():
    '''
    Starting the Firewall module
    '''
    pox.forwarding.l2_learning.launch()
    core.registerNew(Firewall)