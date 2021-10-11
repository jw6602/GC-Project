import networkx
from typing import List

class edge():
    
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
        for src, dst, data in sorted(self.origin_graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True):
            sort_edges.append(edge(src, dst, data["weight"]))
        self.sort_edges = sort_edges
        return sort_edges
    
    def compute(self) -> networkx.Graph:
        if self.sort_edges == None:
            self.sort_edge()
        number_of_nodes = self.origin_graph.number_of_nodes()
        pmfg_graph = networkx.Graph()
        for edge in self.sort_edges:
            # Adding edge and check the planarity
            pmfg_graph.add_edge(edge.src, edge.dst, weight=edge.wt)
            is_planar, _ = networkx.algorithms.planarity.check_planarity(pmfg_graph)
            # If the graph is not planar, then remove the edge
            if not is_planar:
                pmfg_graph.remove_edge(edge.src, edge.dst)
            if pmfg_graph.number_of_nodes == 3 * number_of_nodes - 2:
                break
        self.pmfg_graph = pmfg_graph
        return pmfg_graph

if __name__ == "__main__":
    G = networkx.random_geometric_graph(200,0.3)
    import random
    for (u,v,w) in G.edges(data=True):
        G.edges[u,v]['weight'] = random.randint(1,10)
    pos = networkx.get_node_attributes(G, "pos")
    networkx.draw_networkx_edges(PMFG(graph=G).compute(), pos=pos)