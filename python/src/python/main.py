import json
from pytket import Circuit
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


def generate_circuit_json(circ: Circuit, file_path: str) -> None:
    with open(file_path, "w") as fp:
        json.dump(circ.to_dict(), fp)


def load_circuit_input(file_path: str) -> None:
    with open(file_path, "r") as fp:
        circ_json = json.load(fp)
    circ = Tk2Circuit.from_package_json(circ_json)
    circ = lower_to_pytket(circ)
    print(circ.to_tket1().get_commands())


def main():
    load_circuit_input("../test_files/tket2_json/test.json")
    # draw(build_goto_circuit())


if __name__ == "__main__":
    main()
