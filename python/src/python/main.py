import json
from pytket import Circuit, Qubit
from pytket.pauli import Pauli, QubitPauliTensor
from pytket.tableau import UnitaryTableau
from pytket.circuit.display import view_browser as draw

from tket2.circuit import Tk2Circuit
from tket2.passes import lower_to_pytket


def build_goto_circuit() -> Circuit:
    goto = Circuit()
    data_reg = goto.add_q_register("q", 7)
    ancilla = goto.add_q_register("z", 1)

    goto.CX(1, 0)
    goto.CX(3, 5)
    goto.CX(2, 6)
    goto.Z(4)
    goto.CX(1, 4)
    goto.CX(2, 0)
    goto.CX(3, 6)
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


def load_tket2_circuit_input(file_path: str) -> None:
    with open(file_path, "r") as fp:
        circ_json = json.load(fp)
    circ = Tk2Circuit.from_package_json(str(circ_json))
    circ = lower_to_pytket(circ)
    print(circ.to_tket1().get_commands())


def load_tket1_circuit_input(file_path: str) -> Circuit:
    with open(file_path, "r") as fp:
        circ_json = json.load(fp)
    circ = Circuit.from_dict(circ_json)
    return circ


def main():
    circ = load_tket1_circuit_input("../test_files/tket2_json/subcircuit.json")
    pauli_z_error = tensor_from_pauli_index(Pauli.Z, index=2, n_qubits=8)
    slice_tableau = UnitaryTableau(circ)
    terminal_error = slice_tableau.get_row_product(pauli_z_error)
    print(terminal_error)


if __name__ == "__main__":
    main()
