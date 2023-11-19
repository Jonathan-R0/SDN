# coding: utf-8
# Coursera :
# - Software Defined Networking ( SDN ) course
# -- Programming Assignment : Layer -2 Firewall Application Professor : Nick Feamster
# Teaching Assistant : Arpit Gupta

from nis import match
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
import pox.forwarding.l2_learning
from pox.lib.addresses import EthAddr
from collections import namedtuple
import pox.lib.packet as pkt
import os
import json

log = core.getLogger()


# Add your global variables here ...

class Firewall(EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        self.h1 = EthAddr("00:00:00:00:00:01")
        self.h2 = EthAddr("00:00:00:00:00:02")
        self.rules = self._import_rules()
        log.debug("Enabling Firewall Module")

    def _import_rules(self):
        with open("./ext/rules.rules", "r") as f:
            return json.load(f)

    def _handle_ConnectionUp(self, event):
        # Add your logic here ...
        log.debug("Switch %s has come up.", dpidToStr(event.dpid))

        # Agregar reglas al switch cuando se establece la conexión
        if self.rules["rule_1"]:
            self.filter_port_80(event)
        elif self.rules["rule_2"]:
            self.filter_UDP_h1_5001(event)
        elif self.rules["rule_3"]:
            # self.filter_hosts(event)
            exit(1)

    def filter_UDP_h1_5001(self, event):
        # Regla 2: Descartar mensajes que provengan del host 1, tengan como puerto destino el 5001 y usen UDP
        match = of.ofp_match()
        match.dl_type = pkt.ethernet.IP_TYPE
        match.dl_src = EthAddr('00:00:00:00:00:01')
        match.tp_dst = 5001
        match.nw_proto = pkt.ipv4.UDP_PROTOCOL
        self.add_drop_rule(event.connection, match)

    def filter_port_80(self, event):
        match = of.ofp_match()
        match.dl_type = pkt.ethernet.IP_TYPE
        match.nw_proto = pkt.ipv4.TCP_PROTOCOL
        match.tp_dst = 80
        msg_port = of.ofp_flow_mod(match=match)
        event.connection.send(msg_port)

    def filter_hosts(self, event):
        # Regla 3: Bloquear la comunicación entre dos hosts específicos
        match = of.ofp_match()
        match.dl_type = pkt.ethernet.IP_TYPE
        match.nw_src = self.h1
        match.nw_dst = self.h2
        self.add_drop_rule(event.connection, match)

    def add_drop_rule(self, connection, match):
        msg = of.ofp_flow_mod()
        msg.match = match
        connection.send(msg)


def launch():
    '''
    Starting the Firewall module
    '''
    pox.forwarding.l2_learning.launch()
    core.registerNew(Firewall)