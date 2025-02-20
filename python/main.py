import json
from pytket import Circuit

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


with open("./test_files/goto.json", "w") as fp:
    json.dump(goto.to_dict(), fp)
