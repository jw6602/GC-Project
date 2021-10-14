import networkx
from typing import List
import planarity

class edge():
    """
    Create an edge from `src` to `dst` with weight `wt`

    @params
    src: source node
    dst: destination node
    wt: weight
    """
    def __init__(self, src, dst, wt):
        self.src = src
        self.dst = dst
        self.wt = wt

class PMFG():

    def __init__(self, graph: networkx.Graph):
        self.origin_graph = graph
        self.sort_edges = None
        self.pmfg_graph = None

    def sort_edge(self) -> List[edge]:
        sort_edges = []
        print("sort_edge starts")
        for src, dst, data in sorted(self.origin_graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True):
            print(f"Adding the edge from {edge.src} to {edge.dst} with weight {edge.wt}")
            sort_edges.append(edge(src, dst, data["weight"]))
        print("sort_edge ends")
        self.sort_edges = sort_edges
        return sort_edges
    
    def compute(self) -> networkx.Graph:
        if self.sort_edges == None:
            self.sort_edge()
        number_of_nodes = self.origin_graph.number_of_nodes()
        pmfg_graph = networkx.Graph()
        for edge in self.sort_edges:
            # Adding edge and check the planarity
            print(f"Adding the edge from {edge.src} to {edge.dst} with weight {edge.wt}")
            pmfg_graph.add_edge(edge.src, edge.dst, weight=edge.wt)
            # This planarity check algorithm is a little bit slow
            # is_planar, _ = networkx.algorithms.planarity.check_planarity(pmfg_graph)
            # We may switch to https://github.com/hagberg/planarity/
            is_planar = planarity.is_planar(pmfg_graph)
            # If the graph is not planar, then remove the edge
            if not is_planar:
                pmfg_graph.remove_edge(edge.src, edge.dst)
            if pmfg_graph.number_of_edges == 3 * number_of_nodes - 2:
                break
        self.pmfg_graph = pmfg_graph
        return pmfg_graph

if __name__ == "__main__":
    # An example
    G = networkx.random_geometric_graph(200,0.3)
    import random
    for (u,v,w) in G.edges(data=True):
        G.edges[u,v]['weight'] = random.randint(1,10)
    pos = networkx.get_node_attributes(G, "pos")
    networkx.draw_networkx_edges(PMFG(graph=G).compute(), pos=pos)