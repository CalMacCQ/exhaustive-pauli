import json
import itertools


from tket2.circuit.build import H, from_coms, CX, PauliX, PauliY, PauliZ, id_circ
from tket2.pattern import Rule, RuleMatcher
from tket2.circuit import Tk2Circuit
from pytket.circuit.display import view_browser as draw


# hadamard_rules = [
#    Rule(from_coms(PauliX(0), H(0)), from_coms(H(0), PauliZ(0))),
#    Rule(from_coms(PauliZ(0), H(0)), from_coms(H(0), PauliX(0))),
# ]

cx_rules = [
    Rule(from_coms(PauliZ(0), CX(0, 1)), from_coms(CX(0, 1), PauliZ(0))),
    Rule(from_coms(PauliX(1), CX(0, 1)), from_coms(CX(0, 1), PauliX(1))),
    Rule(from_coms(PauliZ(1), CX(0, 1)), from_coms(CX(0, 1), PauliZ(0), PauliZ(1))),
    Rule(from_coms(PauliX(0), CX(0, 1)), from_coms(CX(0, 1), PauliX(0), PauliX(1))),
]


# def merge_rules() -> list[Rule]:
#    paulis = [PauliX(0), PauliY(0), PauliZ(0)]
#    identities = [Rule(from_coms(p, p), id_circ(1)) for p in paulis]
#
#    off_diag = [
#        Rule(from_coms(p0, p1), from_coms(p2))
#        for p0, p1, p2 in itertools.permutations(paulis)
#    ]
#    return [*identities, *off_diag]
#
#
# merge_rules = merge_rules()


matcher = RuleMatcher([*cx_rules])


def apply_exhaustive(circ: Tk2Circuit, matcher: RuleMatcher) -> int:
    """Apply the first matching rule until no more matches are found. Return the
    number of rewrites applied."""
    match_count = 0
    while match := matcher.find_match(circ):
        match_count += 1
        circ.apply_rewrite(match)

    return match_count


with open("../test_files/tket1_json/goto.json", "r") as fp:
    circ = Tk2Circuit.from_tket1_json(fp)


draw(circ.to_tket1())

matches = apply_exhaustive(circ, matcher)
print(f"Applied {matches} rewrites")

draw(circ.to_tket1())
