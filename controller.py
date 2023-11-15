from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class L2LearningSwitch(object):
    def __init__(self):
        core.openflow.addListeners(self)

        # Diccionario para almacenar la dirección MAC de los hosts y sus puertos asociados
        self.mac_to_port = {}

    def _handle_PacketIn(self, event):
        packet = event.parsed
        in_port = event.port
        switch = event.connection
        dpid = switch.dpid

        # Aprender la dirección MAC del host
        src_mac = packet.src
        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src_mac] = in_port

        # Determinar el puerto de salida para el paquete
        if packet.dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][packet.dst]
        else:
            out_port = of.OFPP_FLOOD

        # Crear un mensaje de flujo para reenviar el paquete al puerto de salida
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, in_port)
        msg.idle_timeout = 10
        msg.hard_timeout = 30
        msg.actions.append(of.ofp_action_output(port=out_port))
        switch.send(msg)

        # Reenviar el paquete al puerto de salida
        out_packet = of.ofp_packet_out()
        out_packet.data = event.ofp
        out_packet.actions.append(of.ofp_action_output(port=out_port))
        switch.send(out_packet)

        log.info("dpid %s, MAC %s, port %s", dpid, src_mac, in_port)

def launch():
    core.registerNew(L2LearningSwitch)
