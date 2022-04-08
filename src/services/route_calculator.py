import sys
import copy
from typing import List, Dict


class RouteCalculator:
    def __init__(self, distances: List[str], destinations: List[str], start_node: str):
        self.distances = distances
        self.destinations = destinations
        self.nodes = self._fill_nodes_list()
        self.graph = self._init_graph()
        self.graph = self._fill_graph(self.graph)
        self.graph = self._get_symmetrical_graph()
        self.path = []
        self.start_node = start_node

    def _fill_nodes_list(self) -> List[str]:
        """Fills nodes list from input distances.
        Returns:
             sorted list of nodes
        """
        nodes = []
        for item in self.distances:
            both_nodes, distance = item.strip().split(":")
            both_nodes = both_nodes.split("-")
            for node in both_nodes:
                nodes.append(node.strip())

        return sorted(list(set(nodes)))  # sorted is for test purposes

    def _init_graph(self) -> Dict[str, Dict]:
        """Initializes empty graph with all nodes from list.
        Returns:
            Empty graph as list with all nodes
        """
        init_graph = {}
        for node in self.nodes:
            init_graph[node] = {}
        return init_graph

    def _fill_graph(self, graph: Dict[str, Dict]) -> Dict[str, Dict[str, int]]:
        """
        Fills Initialized Graph with edges from distances input.
        Args:
            graph: Initialized Graph (Dict[str, Dict]
        Returns:
            Graph with all nodes and edges with weights
        """
        for item in self.distances:
            both_nodes, distance = item.strip().split(":")
            first_node, second_node = both_nodes.split("-")
            first_node = first_node.strip()
            second_node = second_node.strip()
            graph[first_node][second_node] = int(distance)
        return graph

    def _get_symmetrical_graph(self) -> Dict[str, Dict[str, int]]:
        """
        Ensures the symmetry of the graph. If there is a path from node A to B with value N,
        there must be a path from node B to node A with value N.
        Returns:
            Symmetrical Graph
        """
        for node, edges in self.graph.items():
            for adjacent_node, value in edges.items():
                if not self.graph[adjacent_node].get(node, False):
                    self.graph[adjacent_node][node] = value

        return self.graph

    def _get_nodes(self) -> List[str]:
        """Getter for all graph's nodes
        Returns:
            List of graphs nodes
        """
        return self.nodes

    def _get_outgoing_edges(self, node: str) -> List[str]:
        """Gets the node's neighbors
        Args:
            node: Node's name
        Returns:
            The list of node's neighbors
        """
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False):
                connections.append(out_node)
        return connections

    def _get_value(self, node1: str, node2: str) -> int:
        """Get the weigh of edge between two nodes
        Args:
            node1: First node
            node2: Second node
        Returns:
            The weight of edge beetween two nodes
        """
        return self.graph[node1][node2]

    def _calculate_with_dijkstra_algorithm(self, start_node: str):
        """Calculates the fastest route using Dijkstra algorythm
        Args:
            start_node: Stating point of route
        Returns:
            A dict of nodes on the shortest path
        """
        unvisited_nodes = copy.deepcopy(self._get_nodes())

        # This dictionary is used to save visits to each node and update it as we go
        # through graph
        shortest_path = {}

        # We use this dict to store the shortest known route to the found node
        previous_nodes = {}

        # We use sys.maxsize to initialize the infinite weight of unvisited nodes
        max_value = sys.maxsize
        for node in unvisited_nodes:
            shortest_path[node] = max_value

        # Initialize start node with zero weight
        shortest_path[start_node] = 0

        # We need to visit all nodes of graph
        while unvisited_nodes:
            # Founding node with the lowest cost
            current_min_node = None
            for node in unvisited_nodes:
                if current_min_node is None:
                    current_min_node = node
                elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node

            # we get the neighbours of the current node and renew their costs
            neighbors = self._get_outgoing_edges(current_min_node)
            for neighbor in neighbors:
                tentative_value = shortest_path[current_min_node] + self._get_value(
                    current_min_node, neighbor
                )
                if tentative_value < shortest_path[neighbor]:
                    shortest_path[neighbor] = tentative_value
                    # We also update the best route to the current node
                    previous_nodes[neighbor] = current_min_node

            # After visiting all nodes neighbours we mark node as visited
            unvisited_nodes.remove(current_min_node)

        return previous_nodes

    def _get_best_path(self, start_node: str, target_node: str) -> List[str]:
        """Based on calculated previous nodes, gets the fastest path from starting point to destination
        Args:
            start_node: Starting point
            target_node: Destination point
        Returns:
            A list of nodes of the fastest path to the destination point
        """

        previous_nodes = self._calculate_with_dijkstra_algorithm(start_node)
        path = []
        node = target_node

        while node != start_node:
            path.append(node)
            node = previous_nodes[node]

        # as we have several destionations we update final path with calculated for given
        # destinations. We also need to reverse it.
        self.path += list(reversed(path))

        return self.path

    def run(self):
        """The main runner of algorythm which iterates over destinations list calculates best path and
        updates final path

        Returns: Path from starting point to final destination

        """

        # first we need to get path from starting point to first destination
        self._get_best_path(self.start_node, self.destinations[0])
        i = 1
        start_node = self.destinations[0]
        while i < len(self.destinations):
            target_node = self.destinations[i]
            self._get_best_path(start_node=start_node, target_node=target_node)
            i += 1
            start_node = target_node
        self.path.insert(0, self.start_node)

        result = self.path

        return result
