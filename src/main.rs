use tket2::{
    self,
    hugr::{hugr::views::SiblingSubgraph, HugrView, Node},
};

fn subgraph_from_source_node(circuit: tket2::Circuit, source_node: Node) -> SiblingSubgraph {
    let mut visited_nodes: Vec<Node> = Vec::new();
    let mut nodes_to_visit = vec![source_node];

    visited_nodes.push(source_node);

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
        tket2::serialize::load_tk1_json_file("./test_files/goto.json").unwrap();
    //let extarcted =  subgraph_from_source_node(circ, start_node);
    //let subcircuit = Circuit::try_new(extracted, extracted.root())
}
