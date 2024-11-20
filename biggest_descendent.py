import dsc40graph

def biggest_descendent(graph, root, value):
    result = {}
    
    def dfs(node):
        # If already processed this node, return its result
        if node in result:
            return result[node]
            
        # Start with the node's own value
        max_value = value[node]
        
        # Use the successors() method as documented in dsc40graph
        for child in graph.successors(node):
            child_max = dfs(child)
            max_value = max(max_value, child_max)
        
        result[node] = max_value
        return max_value
    
    # Process all nodes starting from the root
    # We'll use nodes attribute from the documentation
    for node in graph.nodes:
        if node not in result:
            dfs(node)
    
    return result
