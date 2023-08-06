
# GENERATED FILE!

import unittest
from dqcsim.plugin import *
from dqcsim.host import *
import tempfile
import os

class Tests(unittest.TestCase):
    _indentation_error = None
    
    def test_gates_toffoli(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_toffoli.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 3\n\nmap q[0], q0\n\nh q0\nh q[1]\n\ntoffoli q0, q[1], q[2]\n\ndisplay\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_x(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_x.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 2\n\nmap q[0], q0\n\nx q[0]\nx q0\nx q[1]\n\ndisplay\n\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_rx(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_rx.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 4\n\nmap q[0], q0\n\nh q0\nh q[1]\n\nrx q[0], 3.14\nrx q0, 0.0\nrx q[1], -0.0\nrx q[1], -1.14\nrx q[2], 10.3E-3\nrx q[3], -10.3E-3\n\ndisplay\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_c_z(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_c_z.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 4\n\nmap q[0], q0\nmap q[1], q1\nmap b[1], b1\nmap q[3], q3\n\nx q0\nx q1\nx q[2]\nx q[3]\n\nmeasure q0\nmeasure q1\n\nc-z b[0], q3\n\ndisplay\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_rz(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_rz.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 4\n\nmap q[0], q0\n\nh q0\nh q[1]\n\nrz q[0], 3.14\nrz q0, 0.0\nrz q[1], -0.0\nrz q[1], -1.14\nrz q[2], 10.3E-3\nrz q[3], -10.3E-3\n\ndisplay\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_y90(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_y90.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 2\n\nmap q[0], q0\n\nh q0\nh q[1]\n\ny90 q[0]\ny90 q0\ny90 q[1]\n\ndisplay\n\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_measure_z(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_measure_z.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 2\n\nh q[0]\nh q[1]\n\nmeasure q[0]\nmeasure_z q[1]\n\ndisplay\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_sdag(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_sdag.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 2\n\nmap q[0], q0\n\nh q0\nh q[1]\n\nsdag q[0]\nsdag q0\nsdag q[1]\n\ndisplay\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_cnot(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_cnot.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 4\n\nmap q[0], q0\nmap q[1], q1\n\nx q[0]\n\ncnot q0, q1\ncnot q1, q[2]\ncnot q[2], q1\ncnot q[2], q[3]\n\ndisplay\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_t(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_t.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 2\n\nmap q[0], q0\n\nh q0\nh q[1]\n\nt q[0]\nt q0\nt q[1]\n\ndisplay\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_c_x(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_c_x.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 4\n\nmap q[0], q0\nmap q[1], q1\nmap b[1], b1\nmap q[3], q3\n\nx q0\nx q1\n\nmeasure q0\nmeasure q1\n\nc-x b[0], q[2]\nc-x b1, q3\n\ndisplay\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_cr(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_cr.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 4\n\nmap q[0], q0\n\nh q0\nh q[1]\n\ncr q0, q[1], 1.0\n\ndisplay\n\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_h(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_h.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 2\n\nmap q[0], q0\n\nh q[0]\nh q0\nh q[1]\n\ndisplay\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_x90(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_x90.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 2\n\nmap q[0], q0\n\nx90 q[0]\nx90 q0\nx90 q[1]\n\ndisplay\n\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_display(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_display.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 2\n\ndisplay\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_measure_all(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_measure_all.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 2\n\nh q[0]\nh q[1]\n\nmeasure_all\n\ndisplay\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_prep_z(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_prep_z.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 2\n\nmap q[0], q0\n\nprep_z q[0]\nprep_z q0\nprep_z q[1]\n\ndisplay\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_y(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_y.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 2\n\nmap q[0], q0\n\nh q0\nh q[1]\n\ny q[0]\ny q0\ny q[1]\n\ndisplay\n\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_swap(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_swap.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 4\n\nmap q[0], q0\nmap q[1], q1\n\nx q0\nx q[2]\n\nswap q0, q[3]\nswap q[2], q1\n\ndisplay\n\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_tdag(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_tdag.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 2\n\nmap q[0], q0\n\nh q0\nh q[1]\n\ntdag q[0]\ntdag q0\ntdag q[1]\n\ndisplay\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_my90(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_my90.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 2\n\nmap q[0], q0\n\nmy90 q[0]\nmy90 q0\nmy90 q[1]\n\ndisplay\n\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_s(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_s.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 2\n\nmap q[0], q0\n\nh q0\nh q[1]\n\ns q[0]\ns q0\ns q[1]\n\ndisplay\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_ry(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_ry.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 4\n\nmap q[0], q0\n\nh q0\nh q[1]\n\nry q[0], 3.14\nry q0, 0.0\nry q[1], -0.0\nry q[1], -1.14\nry q[2], 10.3E-3\nry q[3], -10.3E-3\n\ndisplay\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_z(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_z.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 2\n\nmap q[0], q0\n\nh q[0]\nh q0\n\nz q[0]\nz q0\nz q[1]\n\ndisplay\n\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_gates_mx90(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_gates_mx90.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 2\n\nmap q[0], q0\n\nmx90 q[0]\nmx90 q0\nmx90 q[1]\n\ndisplay\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_examples_example3(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_examples_example3.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 5\nh q[0]\n# measurement outcome in b0\nmeasure_z q[0] \n# simple binary-contolled gate\n# apply Pauli-X to q[1] if b[0]=1\nc-x b[0],q[1] \nmeasure_z q[2]\nmeasure_z q[3]\nmeasure_z q[4]\n# multi-binary controlled gate\n# apply pauli-x to q4 if b2=1 and b3=1 and b4=1\nc-x b[2,3,4],q[4]\n# binary controlled gate using an arbitrary mask :\n# we want to apply a Pauli-X to q[4] if b[0]=0 and b[1]=1\n# negate b0\nnot b[0] \n# multi-bits controlled X gate\nc-x b[0,1],q[4] \n# restore the measurement register\nnot b[0] \ndisplay \n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_examples_example2(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_examples_example2.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\n#define a quantum register of 3 qubits\nqubits 3\n\n# rename qubits\nmap q[0],data\nmap q[1],ancilla\nmap q[2],output\nmap q[1],extra\n\n# address qubits via their names\nprep_z data\nprep_z ancilla\nprep_z output\ncnot data,ancilla\ncnot data,extra\n\n# rename classical bit\nmap b[1],error_syndrome\nmeasure ancilla\n\n#apply binary controlled Pauli-X gate\nc-x error_syndrome,q[2]')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_examples_grover(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_examples_grover.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\n# define a quantum register of 9 qubits\nqubits 9\n\nmap q[4],oracle\n\n# sub-circuit for state initialization\n.init\n    x oracle\n    { h q[0] | h q[1] | h q[2] | h q[3] | h oracle }\n\n# core step of Grover’s algorithm\n# loop with 3 iterations\n.grover(3)\n\n    # search for |x> = |0100>\n\n    # oracle implementation\n\n    x q[2]\n    toffoli q[0],q[1],q[5]\n    toffoli q[1],q[5],q[6] #test of multiline comments\n    #blabla\n    toffoli q[2],q[6],q[7]\n    toffoli q[3],q[7],q[8]\n    cnot q[8],oracle\n    toffoli q[3],q[7],q[8]\n    toffoli q[2],q[6],q[7]\n    toffoli q[1],q[5],q[6]\n    toffoli q[0],q[1],q[5]\n    x q[2]\n\n    # Grover diffusion operator\n    { h q[0] | h q[1] | h q[2] | h q[3] }\n    { x q[0] | x q[1] | x q[2] | x q[3] }\n    h q[3]\n    toffoli q[0],q[1],q[5]\n    toffoli q[1],q[5],q[6]\n    toffoli q[2],q[6],q[7]\n    cnot q[7],q[3]\n    toffoli q[2],q[6],q[7]\n    toffoli q[1],q[5],q[6]\n    toffoli q[0],q[1],q[5]\n    h q[3]\n    { x q[0] | x q[1] | x q[2] | x q[3] }\n    { h q[0] | h q[1] | h q[2] | h q[3] }\n    display\n\n# final measurement\n.final_measurement\n    h oracle\n    measure oracle\n    display ')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_examples_inline_comment(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_examples_inline_comment.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\n# This is a comment\nqubits 10\n\nmap q[0], q0\n\n# comment\nz q0 # Z operation on q[0]\nx q0 # X operation on q[0]\n# comment\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_examples_bell(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_examples_bell.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\n#define a quantum register of 2 qubits\nqubits 2\n\n#Mapping\nmap q[0], q0\nmap q[1], q1\n\n#Prep\n{prep_z q0 | prep_z q1}\n\n# create a Bell pair via a Hadamard rotation\nh q[0]\n# followed by a CNOT gate\n# q[0]: control qubit, q[1]: target qubit\n\ncnot q[0],q[1]\n\n# measure both qubits to test correlations\nmeasure q[0]\nmeasure q[1]\n\n#Parallel measure\n{measure q0 | measure q1}\n\n.display_bits\n    display b[0:2,4:6]\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_examples_example7(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_examples_example7.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\n# define a quantum register of 3 qubits\nqubits 3\n\n# reset the counters for the average procedure\nreset-averaging\n\n# prepare and measure the quantum state 1000 times\n# to accumulate a large outcome statistics\n\n.average(1000)\n\n# state preparation\nprep_z q[0:2]\n{ rx q[0], 3.14 | ry q[1] ,0.23 | h q[2]}\nrx q[2], 3.14\ncnot q[2],q[1]\n{ z q[1] | rx q[2], 1.57 }\n\n# measure of $Z_1$\nmeasure_z q[1]\n\n# the corresponding average is automatically updated\n# measure of $X_0 X_2$\nmeasure_parity q[0],x,q[2],x\n\n# the corresponding average is automatically updated\n# estimate the observable A\n.result\n\n# show the average of $X_0 X_2$ together with its test outcome\ndisplay b[0]\n\n# show the average of $Z_1$ together with its latest outcome\ndisplay b[1]\n\n# the expectation value of $\\hat{A}$ follows\n# from a straightforward postprocess\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_structure_no_subcircuit(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_structure_no_subcircuit.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\n# This is a comment\nqubits 10\n\nmap q[0], q0\n\nx q0\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_structure_single_subcircuit_iterated(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_structure_single_subcircuit_iterated.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\n# This is a comment\nqubits 10\n\nmap q[0], q0\n\n.subcircuit(10)\n  x q0\n  display\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_structure_single_subcircuit(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_structure_single_subcircuit.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\n# This is a comment\nqubits 10\n\nmap q[0], q0\n\n.subcircuit\n  x q0\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_structure_floating_numbers(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_structure_floating_numbers.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 1\n\nrx q[0], 0.0\nrx q[0], 1.0\nrx q[0], 0.1\nrx q[0], 0.01\nrx q[0], 1.0E1\nrx q[0], 1.1E1\nrx q[0], 10.10E10\n\n\nrx q[0], -0.0\nrx q[0], -1.0\nrx q[0], -0.1\nrx q[0], -0.01\nrx q[0], -1.0E1\nrx q[0], -1.1E1\nrx q[0], -10.10E10\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_structure_just_version_and_qubits(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_structure_just_version_and_qubits.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 10\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_structure_just_version_comments_and_qubits(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_structure_just_version_comments_and_qubits.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\n# this is a comment\nqubits 10\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_structure_just_mapping(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_structure_just_mapping.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\n# This is a comment\nqubits 10\n\nmap q[0], r\n')
            with Simulator(fname, 'null') as sim:
                sim.run()
            
    def test_faulty_crk_same_qubit(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_faulty_crk_same_qubit.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 4\n\nmap q[0], q0\nmap q[1], q1\n\ncr q0, q1, 10\ncr q0, q1, -10\n\n\n# --- Faulty code ---\n# Two qubit gate applied on the same qubit\ncr q1, q1, 10\n')
            with self.assertRaises(RuntimeError):
                with Simulator(fname, 'null') as sim:
                    sim.run()
            
    def test_single_subcircuit_iterated(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_single_subcircuit_iterated.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 10\n\nmap q[0], q0\n\n.subcircuit(10)\n\n(20)\n  x q0\n')
            with self.assertRaises(RuntimeError):
                with Simulator(fname, 'null') as sim:
                    sim.run()
            
    def test_faulty_cnot_same_qubit(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_faulty_cnot_same_qubit.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 4\n\nmap q[0], q0\nmap q[1], q1\n\ncnot q0, q1\ncnot q1, q[2]\ncnot q[2], q1\ncnot q[2], q[3]\n\n# --- Faulty code ---\n# CNOT gate applied on the same qubit\ncnot q0, q[0]\n')
            with self.assertRaises(RuntimeError):
                with Simulator(fname, 'null') as sim:
                    sim.run()
            
    def test_qubits_twice(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_qubits_twice.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 10\nqubits 10\n\ndisplay')
            with self.assertRaises(RuntimeError):
                with Simulator(fname, 'null') as sim:
                    sim.run()
            
    def test_inline_comment(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_inline_comment.cq'
            with open(fname, 'w') as f:
                f.write("version 1.0\n# This is a comment\nqubits 10\n\nmap q[0], q0\n\n# comment\nz q0 # Z operation on q[0]\nx q0 # X operation on q[0]\n# comment\n\n# --- Faulty code ---\n# '#' not preceding comment\nerror\n")
            with self.assertRaises(RuntimeError):
                with Simulator(fname, 'null') as sim:
                    sim.run()
            
    def test_faulty_cr_wrong_floating(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_faulty_cr_wrong_floating.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 4\n\nmap q[0], q0\nmap q[1], q1\n\ncr q0, q1, 10\ncr q0, q1, -10\n\n\n# --- Faulty code ---\n# CR applied with invalid floating argument\ncr q0, q1, .1\n')
            with self.assertRaises(RuntimeError):
                with Simulator(fname, 'null') as sim:
                    sim.run()
            
    def test_faulty_floating(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_faulty_floating.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 1\n\nmap q[0], q0\n\nrx q0 .1')
            with self.assertRaises(RuntimeError):
                with Simulator(fname, 'null') as sim:
                    sim.run()
            
    def test_just_version(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_just_version.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0')
            with self.assertRaises(RuntimeError):
                with Simulator(fname, 'null') as sim:
                    sim.run()
            
    def test_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_empty.cq'
            with open(fname, 'w') as f:
                f.write('')
            with self.assertRaises(RuntimeError):
                with Simulator(fname, 'null') as sim:
                    sim.run()
            
    def test_faulty_cr_same_qubit(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fname = tmpdir + os.sep + 'test_faulty_cr_same_qubit.cq'
            with open(fname, 'w') as f:
                f.write('version 1.0\nqubits 4\n\nmap q[0], q0\nmap q[1], q1\n\ncr q0, q1, 10\ncr q0, q1, -10\n\n\n# --- Faulty code ---\n# Two qubit gate applied on the same qubit\ncr q1, q1, 10\n')
            with self.assertRaises(RuntimeError):
                with Simulator(fname, 'null') as sim:
                    sim.run()
            