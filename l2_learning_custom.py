from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import str_to_bool  # Agrega esta línea
from pox.forwarding.l2_learning import LearningSwitch

log = core.getLogger()

_flood_delay = 0


class l2_learning_custom(LearningSwitch):
    def __init__(self, connection, transparent, ignore=None):
        super(l2_learning_custom, self).__init__(connection, transparent)

    def _handle_PacketIn(self, event):
        packet = event.parsed

        # Lógica original de _handle_PacketIn
        super(l2_learning_custom, self)._handle_PacketIn(event)

        # Lógica adicional para registrar pings
        if packet.type == packet.IP_TYPE and packet.find("icmp"):
            ip_src = packet.payload.srcip
            ip_dst = packet.payload.dstip

            if packet.payload.payload.type == 8:  # 8 es el tipo de código para ping request
                log.info("Ping request from %s (%s) to %s (%s)", packet.src, ip_src, packet.dst, ip_dst)
            elif packet.payload.payload.type == 0:  # 0 es el tipo de código para ping reply
                log.info("Ping reply from %s (%s) to %s (%s)", packet.src, ip_src, packet.dst, ip_dst)
            else:
                log.warning("Unknown ICMP type code: %s", packet.payload.payload.type)



def launch(transparent=False, hold_down=_flood_delay, ignore=None):
    global _flood_delay
    _flood_delay = int(str(hold_down), 10)
    assert _flood_delay >= 0

    if ignore:
        ignore = ignore.replace(',', ' ').split()
        ignore = set(str_to_dpid(dpid) for dpid in ignore)

    def start_switch(event):
        log.debug("Controlling %s" % (event.connection,))
        l2_learning_custom(event.connection, transparent, ignore)  # Añade 'ignore'

    core.openflow.addListenerByName("ConnectionUp", start_switch)
