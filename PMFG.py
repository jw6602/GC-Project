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

    def __init__(self, graph: networkx.Graph, planarity_check_lib: str="default", verbose: bool=False):
        self.origin_graph = graph
        self.sort_edges = None
        self.pmfg_graph = None
        self.planarity_check_lib = planarity_check_lib
        self.verbose = verbose

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
            # If the graph is not planar, then remove the edge
            if not self.is_planar(pmfg_graph, self.planarity_check_lib):
                pmfg_graph.remove_edge(edge.src, edge.dst)
            if self.verbose:
                    print(f"Number of edges added = {pmfg_graph.number_of_edges()}, Number of edges to be added = {3 * (number_of_nodes - 2) - pmfg_graph.number_of_edges()}")
            if pmfg_graph.number_of_edges() == 3 * (number_of_nodes - 2):
                break
        self.pmfg_graph = pmfg_graph
        return pmfg_graph

    @staticmethod
    def is_planar(graph: networkx.Graph, planarity_check_lib: str="default") -> bool:
        if planarity_check_lib == "networkx":
            return networkx.algorithms.planarity.check_planarity(graph)[0]
        return planarity.is_planar(graph)
