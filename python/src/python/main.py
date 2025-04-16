import json
from pytket import Circuit, Qubit
from pytket.pauli import Pauli, QubitPauliTensor
from pytket.tableau import UnitaryTableau
from clifford import synthesise_clifford
from pytket.circuit import PhasePolyBox
from pytket.passes import CustomPass
from pytket import OpType


cnot_t_circ = Circuit(3).CX(0, 1).CX(0, 2).CX(2, 1).CX(1, 0).Z(1).T(2).CX(0, 2).CX(0, 1)


def build_goto_circuit() -> Circuit:
    goto = Circuit()
    data_reg = goto.add_q_register("q", 7)
    ancilla = goto.add_q_register("z", 1)

    goto.CX(1, 0)
    goto.T(1)
    goto.CX(3, 5)
    goto.CX(2, 6)
    goto.Z(4)
    goto.CX(1, 4)
    goto.CX(2, 0)
    goto.T(0)
    goto.CX(2, 0)
    goto.CX(3, 6)
    goto.CX(1, 5)
    goto.T(5)
    goto.CX(1, 5)
    goto.CX(6, 4)
    goto.CX(data_reg[0], ancilla[0])
    goto.CX(data_reg[5], ancilla[0])
    goto.CX(data_reg[6], ancilla[0])
    return goto


def tensor_from_pauli_index(
    pauli: Pauli, index: int, n_qubits: int
) -> QubitPauliTensor:
    pauli_list = [Pauli.I] * n_qubits

    pauli_list[index] = pauli

    qubit_list = [Qubit(n) for n in range(n_qubits)]

    return QubitPauliTensor(paulis=pauli_list, qubits=qubit_list)


def generate_circuit_json(circ: Circuit, file_path: str) -> None:
    with open(file_path, "w") as fp:
        json.dump(circ.to_dict(), fp)


cnot_t_circ = Circuit(3).CX(0, 1).CX(0, 2).CX(2, 1).CX(1, 0).Z(1).T(2).CX(0, 2).CX(0, 1)

generate_circuit_json(cnot_t_circ, "../test_files/input_circuits/phase_poly.json")


def load_tket1_circuit_input(file_path: str) -> Circuit:
    with open(file_path, "r") as fp:
        circ_json = json.load(fp)
    circ = Circuit.from_dict(circ_json)
    return circ


def convert_t_to_rz(circ: Circuit) -> Circuit:
    circ_prime = Circuit(circ.n_qubits)

    for cmd in circ:
        if cmd.op.type == OpType.T:
            circ_prime.Rz(0.25, cmd.qubits[0])
        else:
            circ_prime.add_gate(cmd.op.type, cmd.op.params, cmd.qubits)

    return circ_prime


REPLACE_T_WITH_RZ = CustomPass(convert_t_to_rz)

from pytket.circuit.display import view_browser as draw


def main():
    draw(build_goto_circuit())
    circ = load_tket1_circuit_input(
        "../test_files/output_circuits/t_doped_subcircuit.json"
    )
    draw(circ)
    print(circ.get_commands())
    REPLACE_T_WITH_RZ.apply(circ)
    print(circ.get_commands())

    pauli_z_error = tensor_from_pauli_index(Pauli.Z, index=1, n_qubits=3)
    u_slice = PhasePolyBox(circ)
    terminal_error = synthesise_clifford(u_slice, pauli_z_error)
    # slice_tableau = UnitaryTableau(circ)
    # terminal_error = slice_tableau.get_row_product(pauli_z_error)
    print(terminal_error)


if __name__ == "__main__":
    # t_doped_goto = build_goto_circuit()
    # generate_circuit_json(
    #    t_doped_goto, "../test_files/input_circuits/t_doped_goto.json"
    # )
    main()
