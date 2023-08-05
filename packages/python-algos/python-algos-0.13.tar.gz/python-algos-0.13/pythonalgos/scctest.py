# Kosaraju's algorithm to find strongly connected components in Python


from collections import defaultdict


class Graph:

    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)

    # Add edge into the graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # DFS
    def DFS(self, v, visited):
        visited[v] = True
        # print(v, end='')
        for i in self.graph[v]:
            # print(str(i))
            if not visited[i]:
                self.DFS(i, visited)

    def fillOrder(self, v, visited, stack):
        visited[v] = True
        for i in self.graph[v]:
            if not visited[i]:
                self.fillOrder(i, visited, stack)
        stack = stack.append(v)

    # Transpose the matrix
    def Transpose(self):
        g = Graph(self.V)

        for i in self.graph:
            for j in self.graph[i]:
                g.addEdge(j, i)
        return g

    # Print stongly connected components
    def printSCC(self):
        stack = []
        visited = [False] * (self.V)

        for i in range(self.V):
            if not visited[i]:
                self.fillOrder(i, visited, stack)

        gr = self.Transpose()

        visited = [False] * (self.V)

        while stack:
            i = stack.pop()
            if not visited[i]:
                print(str(i))
                gr.DFS(i, visited)


# g = Graph(8)
# g.addEdge(0, 1)
# g.addEdge(1, 2)
# g.addEdge(2, 3)
# g.addEdge(2, 5)
# g.addEdge(3, 4)
# g.addEdge(4, 5)
# g.addEdge(4, 2)
# g.addEdge(5, 6)
# g.addEdge(6, 7)
# g.addEdge(7, 5)
# g.addEdge(8, 8)

g = Graph(11)
g.addEdge(0, 1)
g.addEdge(1, 2)
g.addEdge(1, 3)
g.addEdge(2, 0)
g.addEdge(3, 4)
g.addEdge(4, 5)
g.addEdge(5, 3)
g.addEdge(6, 5)
g.addEdge(6, 7)
g.addEdge(7, 8)
g.addEdge(8, 9)
g.addEdge(9, 6)
g.addEdge(9, 10)


print("Strongly Connected Components:")
g.printSCC()

"""
"

   self.vertices = {"A": ["B"], "B": ["C", "D"], "C": ["A"], "D": ["E"],
                         "E": ["F"], "F": ["D"], "G": ["F", "H"], "H": ["I"],
                         "I": ["J"], "J": ["G", "K"], "K": []}*/
                         """