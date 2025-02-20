from tket2.circuit.build import H, from_coms, CX, PauliX, PauliZ
from tket2.pattern import Rule


hadamard_rules = [
    Rule(from_coms(PauliX(0), H(0)), from_coms(H(0), PauliZ(0))),
    Rule(from_coms(PauliZ(0), H(0)), from_coms(H(0), PauliX(0))),
]

cx_rules = [
    Rule(from_coms(PauliZ(0), CX(0, 1)), from_coms(CX(0, 1), PauliZ(0))),
    Rule(from_coms(PauliX(1), CX(0, 1)), from_coms(CX(0, 1), PauliX(1))),
    Rule(from_coms(PauliZ(1), CX(0, 1)), from_coms(CX(0, 1), PauliZ(0), PauliZ(1))),
    Rule(from_coms(PauliX(0), CX(0, 1)), from_coms(CX(0, 1), PauliX(0), PauliX(1))),
]
