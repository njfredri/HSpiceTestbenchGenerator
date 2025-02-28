* 2-Input NAND Gate Subcircuit using CMOS
.include "ptm_22nm_bulk_hp.l"

.SUBCKT nand_gate A B Y VDD VSS
* PMOS Pull-up Network
M1 Y A VDD VDD pmos W=45n L=22n
M2 Y B VDD VDD pmos W=45n L=22n

* NMOS Pull-down Network
M3 N1 A 0 0 nmos W=45n L=22n
M4 Y B N1 0 nmos W=45n L=22n

.ENDS nand_gate
