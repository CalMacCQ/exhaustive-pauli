use tket2::{
    self,
    hugr::{hugr::views::SiblingSubgraph, ops::NamedOp, HugrView, Node},
    serialize::save_tk1_json_writer,
};

use std::fs::File;

fn subgraph_from_source_node(circuit: &tket2::Circuit, source_node: Node) -> SiblingSubgraph {
    // Traverse the Circuit with BFS to find the subcircuit
    // in the causal cone of the source node

    let mut visited_nodes: Vec<Node> = Vec::new();
    let mut nodes_to_visit = vec![source_node];

    // Normally in BFS we would add the source node to visited_nodes
    // However we only want the gates that come after the Pauli gate

    while nodes_to_visit.len() > 0 {
        let current_node = nodes_to_visit.pop().unwrap();
        for neighbour in circuit.hugr().output_neighbours(current_node) {
            if !visited_nodes.contains(&neighbour) {
                visited_nodes.push(neighbour);
                nodes_to_visit.push(neighbour);
            }
        }
    }
    SiblingSubgraph::try_from_nodes(visited_nodes, circuit.hugr()).unwrap()
}

fn main() {
    let circ: tket2::Circuit =
        tket2::serialize::load_tk1_json_file("./test_files/input_circuits/t_doped_goto.json")
            .unwrap();

    println!("{}", circ.mermaid_string());

    let pauli_z_cmds: Vec<_> = circ
        .commands()
        .filter(|cmd| cmd.optype().name() == "tket2.quantum.Z")
        .collect();

    let first_pauli = &pauli_z_cmds[0];

    let sibgraph = subgraph_from_source_node(&circ, first_pauli.node());

    let extracted = sibgraph.extract_subgraph(circ.hugr(), "");

    let subcircuit = tket2::Circuit::try_new(extracted.clone(), extracted.root()).unwrap();
    println!("{}", subcircuit.mermaid_string());

    let file = File::create("test_files/output_circuits/t_doped_subcircuit.json").unwrap();

    let _ = save_tk1_json_writer(&subcircuit, file);
}
