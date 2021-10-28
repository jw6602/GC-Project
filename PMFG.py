import networkx
from typing import List
import planarity
import itertools
import threading

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
        i = 0
        while i < len(self.sort_edges):
            if pmfg_graph.number_of_edges() < 3 * (number_of_nodes - 2): # we will only use single thread for now
                edge = self.sort_edges[i]
                pmfg_graph.add_edge(edge.src, edge.dst, weight=edge.wt)
                if not self.is_planar(pmfg_graph, self.planarity_check_lib):
                    pmfg_graph.remove_edge(edge.src, edge.dst)
                i += 1
            else:
                # when the size of the graph is small, it is better to use single thread b/c planarity check is too fast
                # when the size of the graph is large enough, the multi-threading should have better performance
                step_length = 95
                edges = self.sort_edges[i:i+step_length]
                results = [False] * len(edges)
                threads = []
                def forward_one_step_is_planar(graph, index, edge):
                    graph.add_edge(edge.src, edge.dst, weight=edge.wt)
                    results[index] = planarity.is_planar(graph)
                for index, edge in enumerate(edges):
                    threads.append(threading.Thread(target=forward_one_step_is_planar, args=(pmfg_graph.copy(), index, edge)))
                for _t in threads:
                    _t.start()
                for _t in threads:
                    _t.join()
                available_edges = []
                for index, ok in enumerate(results):
                    if ok:
                        available_edges.append(edges[index])
                edges_combinations = self.combinations(available_edges)
                for edges_combination in edges_combinations:
                    for edge in edges_combination:
                        pmfg_graph.add_edge(edge.src, edge.dst, weight=edge.wt)
                    if self.is_planar(pmfg_graph, self.planarity_check_lib):
                        break
                    else:
                        for edge in edges_combination:
                            pmfg_graph.remove_edge(edge.src, edge.dst)
                i += step_length
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
    
    def combinations(iterable):
        r = []
        for i in reversed(range(1, len(iterable)+1)):
            for subset in itertools.combinations(iterable, i):
                r.append(subset)
        return r