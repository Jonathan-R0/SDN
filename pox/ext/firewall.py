# coding: utf-8
# Coursera :
# - Software Defined Networking ( SDN ) course
# -- Programming Assignment : Layer -2 Firewall Application Professor : Nick Feamster
# Teaching Assistant : Arpit Gupta

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
# Add your imports here ...
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.ipv4 import ipv4
import json

log = core.getLogger()

# Add your global variables here ...

class Firewall(EventMixin) :

    def __init__(self, h1, h2):
        self.listenTo(core.openflow)
        self.h1 = h1
        self.h2 = h2
        self.rules = self._import_rules()
        log.debug("Enabling Firewall Module")
    
    def _import_rules(self):
        with open("rules/rules.rules", "r") as f:
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
            self.filter_hosts(event)

    def filter_port_80(self, event):
        # Regla 1: Descartar todos los mensajes cuyo puerto destino sea 80
        match = of.ofp_match()
        match.dl_type = ethernet.IP_TYPE
        match.tp_dst = 80
        self.add_drop_rule(event.connection, match)

    def filter_UDP_h1_5001(self, event):
        # Regla 2: Descartar mensajes que provengan del host 1, tengan como puerto destino el 5001 y usen UDP
        match = of.ofp_match()
        match.dl_type = ethernet.IP_TYPE
        match.dl_src = ethernet.IPAddr(self.rules["blocked_host"])
        match.tp_dst = 5001
        match.nw_proto = ipv4.UDP_PROTOCOL
        self.add_drop_rule(event.connection, match)

    def filter_hosts(self, event):
        # Regla 3: Bloquear la comunicación entre dos hosts específicos
        match = of.ofp_match()
        match.dl_type = ethernet.IP_TYPE
        match.nw_src = self.h1
        match.nw_dst = self.h2
        self.add_drop_rule(event.connection, match)

    def add_drop_rule(self, connection, match):
        msg = of.ofp_flow_mod()
        msg.match = match
        connection.send(msg)

    def launch(h1 = None, h2 = None):
        # Starting the Firewall module
        core.registerNew(Firewall, h1, h2)
