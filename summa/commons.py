from summa.graph import Graph

def build_graph(sequence):
    graph = Graph()
    document = []
    for item in sequence:
        item = item.strip()
        if item is None or len(item) == 0:
            continue
        if not graph.has_node(item):
            graph.add_node(item)
            document.append(item)
    return graph, document


def remove_unreachable_nodes(graph):
    for node in graph.nodes():
        if sum(graph.edge_weight((node, other)) for other in graph.neighbors(node)) == 0:
            graph.del_node(node)