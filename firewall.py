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

log = core.getLogger()

# Add your global variables here ...

class Firewall(EventMixin) :

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp(self, event):
        # Add your logic here ...
        log.debug("Switch %s has come up.", dpidToStr(event.dpid))

        # Agregar reglas al switch cuando se establece la conexión
        self.add_firewall_rules(event.connection)
    
    def add_firewall_rules(self, connection):
        # Regla 1: Descartar todos los mensajes cuyo puerto destino sea 80
        match = of.ofp_match()
        match.dl_type = ethernet.IP_TYPE
        match.tp_dst = 80
        self.add_drop_rule(connection, match)

        # Regla 2: Descartar mensajes que provengan del host 1, tengan como puerto destino el 5001 y usen UDP
        match = of.ofp_match()
        match.dl_type = ethernet.IP_TYPE
        match.nw_src = "10.0.0.1"  # Reemplaza con la dirección IP del host 1
        match.tp_dst = 5001
        match.nw_proto = ipv4.UDP_PROTOCOL
        self.add_drop_rule(connection, match)

        # Regla 3: Bloquear la comunicación entre dos hosts específicos
        # Reemplaza estas direcciones IP con las de los hosts que no deben comunicarse
        src_host = "10.0.0.2"
        dst_host = "10.0.0.3"
        match = of.ofp_match()
        match.dl_type = ethernet.IP_TYPE
        match.nw_src = src_host
        match.nw_dst = dst_host
        self.add_drop_rule(connection, match)
    
    def add_drop_rule(self, connection, match):
        msg = of.ofp_flow_mod()
        msg.match = match
        connection.send(msg)

    def add_drop_rule(self, connection, match):
        msg = of.ofp_flow_mod()
        msg.match = match
        connection.send(msg)

    def launch():
        # Starting the Firewall module
        core.registerNew(Firewall)
