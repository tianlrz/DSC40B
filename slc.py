from dsc40graph import UndirectedGraph

class _DisjointSetForestCore:
    def __init__(self):
        self._parent = []
        self._rank = []
        self._size_of_set = []
    
    def make_set(self):
        x = len(self._parent)
        self._parent.append(None)
        self._rank.append(0)
        self._size_of_set.append(1)
        return x
    
    def find_set(self, x):
        try:
            parent = self._parent[x]
        except IndexError:
            raise ValueError(f'{x} is not in the collection.')
        
        if self._parent[x] is None:
            return x
        else:
            root = self.find_set(self._parent[x])
            self._parent[x] = root  # Path compression
            return root
    
    def union(self, x, y):
        x_rep = self.find_set(x)
        y_rep = self.find_set(y)
        
        if x_rep == y_rep:
            return
            
        if self._rank[x_rep] > self._rank[y_rep]:
            self._parent[y_rep] = x_rep
            self._size_of_set[x_rep] += self._size_of_set[y_rep]
        else:
            self._parent[x_rep] = y_rep
            self._size_of_set[y_rep] += self._size_of_set[x_rep]
            if self._rank[x_rep] == self._rank[y_rep]:
                self._rank[y_rep] += 1

class DisjointSetForest:
    def __init__(self, elements):
        self._core = _DisjointSetForestCore()
        self.element_to_id = {}
        self.id_to_element = {}
        
        for element in elements:
            eid = self._core.make_set()
            self.element_to_id[element] = eid
            self.id_to_element[eid] = element
    
    def find_set(self, element):
        return self.id_to_element[
            self._core.find_set(
                self.element_to_id[element]
            )
        ]
    
    def union(self, x, y):
        x_id = self.element_to_id[x]
        y_id = self.element_to_id[y]
        self._core.union(x_id, y_id)
    
    def in_same_set(self, x, y):
        return self.find_set(x) == self.find_set(y)

def slc(graph, d, k):
    """
    Perform single linkage clustering using Kruskal's algorithm.
    
    Args:
        graph: An instance of dsc40graph.UndirectedGraph
        d: A function that takes an edge (tuple of two nodes) and returns the distance
        k: Number of desired clusters
        
    Returns:
        frozenset of k frozensets, each representing a cluster
    """
    edges = []
    for edge in graph.edges:
        if edge[0] < edge[1]:  # Only add each edge once
            edges.append(edge)
    
    # Sort edges by distance
    edges.sort(key=d)
    
    # Initialize disjoint set forest with all nodes
    dsf = DisjointSetForest(graph.nodes)
    
    # Number of components (starts with |V| components)
    num_components = len(graph.nodes)
    
    # Run modified Kruskal's until we have k components
    for u, v in edges:
        if num_components <= k:
            break
            
        if not dsf.in_same_set(u, v):
            dsf.union(u, v)
            num_components -= 1
    
    # Collect the clusters
    clusters = {}
    for node in graph.nodes:
        rep = dsf.find_set(node)
        if rep not in clusters:
            clusters[rep] = set()
        clusters[rep].add(node)
    
    # Convert to frozenset of frozensets
    return frozenset(frozenset(cluster) for cluster in clusters.values())
