# SDN
Software Defined Network POX &amp; Mininet - TP2

Requisito previo: copiar del repo **ls_learning_custom.py** a **pox/pox/forwarding/** (quedará junto a
    **ls_learning.py** que ya está ahí).

Explicación para Linux Ubuntu.
1) Abrir una terminal.
    * Entrar en la carpeta de POX
    cd "[carpeta]/pox"
    
    * Ejecutar POX
        El original se ejecuta así: **./pox.py forwarding.l2_learning**
 
        Pero estamos haciendo uno custom que hereda de aquel e incorpora logs extra, de tipo INFO, que en principio
        salen por pantalla junto a los originales, si quieren correr ese ejecutar 
        **./pox.py log.level --DEBUG forwarding.l2_learning_custom**
 
2) Abrir otra terminal, para Mininet.
   * Entrar en la carpeta del repo:
   **cd "[carpeta]/SDN"**

    * Ejecutar **sudo mn --custom topo.py --topo customTopo,num_switches=4 --controller=remote,ip=127.0.0.1,port=6633**
    (se puede cambiar la cantidad de switches)
