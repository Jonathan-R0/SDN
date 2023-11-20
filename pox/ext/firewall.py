# coding: utf-8
from nis import match
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
import pox.forwarding.l2_learning
from pox.lib.addresses import EthAddr, IPAddr
import pox.lib.packet as pkt
import json

log = core.getLogger()

class Firewall(EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        json_file = self._import_json()
        self.switch_dpid = int(json_file["switch_dpid"]) if "switch_dpid" in json_file else None
        self.rules = json_file["rules"] if "rules" in json_file else []
        log.debug("Enabling Firewall Module")

    def _import_json(self):
        with open("./ext/rules.rules", "r") as f:
            return json.load(f)
    
    def _handle_PacketIn(self, event):
        packet = event.parsed
        if packet.type == pkt.ethernet.IP_TYPE:
            log.debug("Packet from %s to %s, with data %s",  packet.find("ipv4").srcip, packet.find("ipv4").dstip, packet.payload)

    def _handle_ConnectionUp(self, event):
        if event.dpid == self.switch_dpid or self.switch_dpid == None:
            log.debug("Switch %s has come up.", dpidToStr(event.dpid))
            # Agregar reglas al switch cuando se establece la conexión
            for rule in self.rules:
                self.add_rule(rule, event)

    def add_rule(self, rule, event):
        match = of.ofp_match()
        match.dl_type = pkt.ethernet.IP_TYPE
        if "dl_src" in rule:
            match.dl_src = EthAddr(rule["dl_src"])
        if "dl_dst" in rule:
            match.dl_dst = EthAddr(rule["dl_dst"])
        if "tp_src" in rule:
            match.tp_src = rule["tp_src"]
        if "tp_dst" in rule:
            match.tp_dst = rule["tp_dst"]
        if "nw_proto" in rule:
            if rule["nw_proto"] == "UDP":    
                match.nw_proto = pkt.ipv4.UDP_PROTOCOL
            elif rule["nw_proto"] == "TCP":
                match.nw_proto = pkt.ipv4.TCP_PROTOCOL
        if "nw_src" in rule:
            match.nw_src = IPAddr(rule["nw_src"])
        if "nw_dst" in rule:
            match.nw_dst = IPAddr(rule["nw_dst"])
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
