# SDN

## Software Defined Network POX &amp; Mininet - TP2

Requisitos previos respecto a POX, por única vez, copiar del repositorio a la carpeta original de POX en la computadora:

- Logueo adicional en el controlador: copiar del repositorio `pox/ls_learning_custom.py` a `pox/pox/forwarding/` (quedará junto a `ls_learning.py` que ya está ahí).
- Firewall: copiar del repositorio `pox/ext/firewall.py` a `pox/ext/`.   
- Reglas para el firewall: copiar del repositorio `pox/ext/rules.rules` a `pox/ext`.
- Bug fix ("ERROR:packet:(dns) parsing questions: ord() expected string of length 1, but int found..."): copiar del repositorio `pox/pox/lib/packet/dns.py` a `pox/pox/lib/packet/`.


Explicación para Linux Ubuntu.
1) Abrir una terminal.
    - Entrar en la carpeta de POX `cd path/to/pox`.
    
    - Ejecutar `./pox.py log.level --DEBUG firewall` o `python2 ./pox.py log.level --DEBUG firewall`.
 
2) Abrir otra terminal, para Mininet.
    - Entrar en la carpeta del repositorio: `cd path/to/SDN`.

    - Ejecutar `sudo mn --custom topo.py --topo customTopo,num_switches=4 --mac --arp --switch ovsk --controller remote,ip=127.0.0.1,port=6633` (se puede cambiar la cantidad de switches).

3) Ejecutar en la terminal de mininet:

    - `xterm host_1 host_2`. Esto abrirá 2 terminales, tienen que estar en modo root, sino a los comandos de `iperf` les falta permisos.

    - El archivo `rules.rules` es un json que tiene las reglas, se puede cambiar para probar con otros switches. Se pueden agregar reglas al gusto agregando otro objeto a la lista de reglas.

4) Pruebas:
    - _Descartar mensajes del puerto 80:_
        - En host_1: `iperf -s -p 80` (servidor)
        - En host_2: `iperf -c 10.0.0.1 -p 80` (cliente)

    - _Descartar mensajes de UDP con puerto de salida 5001 del host 1:_
        - En host_1: `iperf -s -u -p 5001` (servidor)
        - En host_2: `iperf -c 10.0.0.1 -u -p 5001` (cliente)

    - _Descartar mensajes de 2 hosts cualquiera:_ (O sino con pingall es mas directa la prueba)
        - En host_1: `iperf -s -u -p 6969` (servidor)
        - En host_2: `iperf -c 10.0.0.3 -u -p 6969` (cliente)

(LAUCHA)

python2 ./pox.py firewall

sudo mn --custom topo.py --topo customTopo,4 --mac --arp --switch ovsk --controller remote (entiendo que es lo mimso que la que estamos usando)


TODO:
- verificar que la rule 3 funciona
- desharcodear las direcciones para las rules
- agregar los logs
- terminar informe.
