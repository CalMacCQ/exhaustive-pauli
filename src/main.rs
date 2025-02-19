use tket2;

fn main() {
    // Load a tket1 circuit.
    let mut circ: tket2::Circuit =
        tket2::serialize::load_tk1_json_file("./test_files/barenco_tof_5.json").unwrap();

    assert_eq!(circ.qubit_count(), 9);
    assert_eq!(circ.num_operations(), 170);

    // Traverse the circuit and print the gates.
    //for command in circ.commands() {
    //    println!("{:?}", command.optype());
    //}

    // Render the circuit as a mermaid diagram.
    println!("{}", circ.mermaid_string());
    println!(
        "{}",
        "======================================================================="
    );
    // Optimise the circuit.
    tket2::passes::apply_greedy_commutation(&mut circ).unwrap();

    // Render optimised circuit.
    println!("{}", circ.mermaid_string());
}
