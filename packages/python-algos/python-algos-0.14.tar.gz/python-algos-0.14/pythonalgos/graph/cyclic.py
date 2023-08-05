""" Module that contains a main function that checks whether a directed graph
is cyclic or not

Calls to advice insertions are included at join-points. These calls belong to a
abstract class Advisor, which must be implemented by interested parties """

from .. util.advisor import Advisor
from . directed_graph_core import DirectedGraphCore
from . vertex import Vertex
from typing import Set, MutableMapping


def is_cyclic(directed_graph: DirectedGraphCore, advisor: Advisor):
    """ Function that checks whether a directed graph contains a cycle or not

    Args:
        directed_graph (DirectedGraph): The directed graph
        advisor(Advisor): Object that contains advice which can be inserted at
        join points

    Returns:
        bool: True if the directed graph contains a cycle, otherwise False """

    def _is_cyclic_dfs(directed_graph: DirectedGraphCore, vertex: Vertex,
                       visited_already: MutableMapping[Vertex, bool],
                       in_cycle: MutableMapping[Vertex, bool]):
        """ Function that recursively searches the directed graph depth first
        and checks if a vertex was already in_cycle before.

        It checks all vertices that have not been traversed before. The heads
        of those
        vertices are followed. If in that traversal, a vertex is found that is
        present in the dict "in_cycle" with a value of true, then a cycle is
        present

        Args:
            directed_graph (DirectedGraphCore): The directed graph
            vertex(Vertex): The current vertex
            visited_already (dict): A dictionary that maintains whether
                vertices have been traversed already. It's a performance
                measure put in place in order to shortcut processing if a
                vertex was already processed by another subtree in_cycle
                (list): A list that, if a vertex has been found to part be
                part of cycle, for that vertex, has a value of true. If
                that vertex is not part of a cycle, it's value is false

        Returns:
            bool: True if the vertex was in_cycle before, False otherwise """

        visited_already[vertex] = True
        in_cycle[vertex] = True
        advisor.advise("visit_vertex", directed_graph, vertex)

        for edge in vertex.get_edges():
            if visited_already.get(edge.get_head()) is None:
                if _is_cyclic_dfs(directed_graph, edge.get_head(),
                                  visited_already, in_cycle):
                    advisor.advise("cycle_reported_recursive", directed_graph,
                                   edge.get_head())
                    return True
                else:
                    advisor.advise("no_cycle_reported_recursive",
                                   directed_graph, vertex)
            elif in_cycle[edge.get_head()]:
                advisor.advise("cycle_found", directed_graph, vertex,
                               edge.get_head())
                return True
            elif visited_already.get(edge.get_head().get_label()):
                advisor.advise("vertex_already_visited", directed_graph, edge)

        in_cycle[vertex] = False
        return False

    def _is_cyclic_inner(directed_graph: DirectedGraphCore):
        """ Main function that loops through the vertices and starts
        the traversal for each vertex.

        Args:
            directed_graph (DirectedGraphCore): The directed graph """

        visited_already: MutableMapping[Vertex, bool] = dict()
        in_cycle: MutableMapping[Vertex, bool] = {
            vertex: False for vertex in directed_graph.get_vertices()}
        for vertex in directed_graph.get_vertices():
            if vertex not in visited_already:
                if _is_cyclic_dfs(directed_graph, vertex, visited_already,
                                  in_cycle):
                    return True

        return False

    return _is_cyclic_inner(directed_graph)
