import pprint
from z3 import *

class Graph:
    # pin_pairs list of pairs(pair is a list of size 2 of tuples);
    def __init__(self, m : int, pin_pairs : list):
        self.m = m
        self.pin_pairs = pin_pairs

        self.graph = Graph.input_to_graph(m, pin_pairs)


    # returns a list "edges" of lists of size 2;
    # where edges[x][0] is the start vertex of the edge x and
    # where edges[x][1] is the terminal vertex of the edge x;
    def get_all_edges(self) -> list:
        edges = []
        for curr_vertex, outgoing_vertices in self.graph.items():
            for out_vertex in outgoing_vertices:
                edges.append([curr_vertex, out_vertex])

        return edges

    def get_incoming_edges(self, vertex) -> list:
        
        in_vertices = self.get_incoming_vertices(vertex)
        in_edges = [ [in_vertices[i], vertex] for i in range(len(in_vertices)) ]

        return in_edges

    def get_outgoing_edges(self, vertex) -> list:

        out_vertices = self.get_outgoing_vertices(vertex)
        out_edges = [ [vertex, out_vertices[i]] for i in range(len(out_vertices)) ]

        return out_edges

    def get_incoming_vertices(self, vertex) -> list:
        in_vertices = []
        for curr_vertex, outgoing_vertices in self.graph.items():
            for out_vertex in outgoing_vertices:
                if out_vertex == vertex:
                    in_vertices.append(curr_vertex)
            
        return in_vertices


    def get_outgoing_vertices(self, vertex) -> list:

        return self.graph[vertex]


    def print_as_grid(self):
        arr = [['.' for i in range(self.m)] for j in range(self.m)]

        # pin_pairs = [ 
        #   [(1, 0), (3, 4), 'a'],
        #   [(2, 0), (4, 5), 'b'],
        #   [(1, 4), (4, 2), 'c']
        # ]
        for pin_pair in self.pin_pairs:
            arr[pin_pair[0][0]][pin_pair[0][1]] = arr[pin_pair[1][0]][pin_pair[1][1]] = pin_pair[2]

        for i in range(len(arr)):
            for j in range(len(arr[0])):
                print(arr[i][j], " ", end='')
            print()
        print()


    def print_as_graph(self):
        pprint.pprint(self.graph)


    @staticmethod
    def input_to_graph(m : int, pin_pairs : list):

        graph = {}

        for x in range(m):
            for y in range(m):
                tempSet = []
                if x > 0: tempSet.append((x - 1, y))
                if y > 0: tempSet.append((x, y - 1))
                if x < m - 1: tempSet.append((x + 1, y))
                if y < m - 1: tempSet.append((x, y + 1))
                graph[(x, y)] = tempSet

        return graph



class FreeFlow2Sat:
    def __init__(self, graph : Graph):
        self.graph = graph

        self.__construct_variables()
        self.__construct_formula()


    def __construct_formula(self):
        self.formula = Solver()

        self.path2sat(self.graph.pin_pairs[0])

        answer = self.formula.check()
        model = self.formula.model()

        print(answer)
        print(model)
        # self.graph.print_as_grid_and_path(model)

    
    # pin pair - list of size 2 of tuples
    def path2sat(self, pin_pair : list):
#########################################
        s = pin_pair[0] # start vertex
        t = pin_pair[1] # terminal vertex
        label = pin_pair[2]

        # Adding clauses: (ru -> (rx1 or rx2 or ... or rxk)),
        # where ru is varible for graph vertex,
        # where rx1 ... rxk are predecessors of ru on the path;
        for vertex, _ in self.graph.graph.items():
            # Ignore start vertex since it does not have any predecessors on the path;
            if vertex == s:
                continue

            in_vertices = self.graph.get_incoming_vertices(vertex)

            # Implication clause: vertex -> in_vertex[0] or in_vertex[1] or ... or in_vertex[k];
            clause = []
            for in_vertex in in_vertices:
                clause.append(self.vvars[in_vertex][label])

            # self.__enforce_exactly_one(clause)
            clause.append(Not(self.vvars[vertex][label]))

            # Adding the implication clause to the formula;
            self.formula.add(Or(clause))

        # Adding start and terminal vertices as single clausses;
        self.formula.add([self.vvars[s][label]])
        self.formula.add([self.vvars[t][label]])
#########################################

        for vertex, _ in self.graph.graph.items():
            in_edges = self.graph.get_incoming_edges(vertex)
            out_edges = self.graph.get_outgoing_edges(vertex)

            if vertex != s:
                in_edges_clause = []
                for in_edge in in_edges:
                    in_edges_clause.append( self.evars[in_edge[0]][in_edge[1]][label] )
                
                self.__enforce_exactly_one(in_edges_clause)
                in_edges_clause.append(Not(self.vvars[vertex][label]))
                self.formula.add(Or(in_edges_clause))
            else:
                for in_edge in in_edges:
                    self.formula.add( Not(self.evars[in_edge[0]][in_edge[1]][label]) )


            if vertex != t:
                out_edges_clause = []
                for out_edge in out_edges:
                    out_edges_clause.append( self.evars[out_edge[0]][out_edge[1]][label] )

                self.__enforce_exactly_one(out_edges_clause)
                out_edges_clause.append(Not(self.vvars[vertex][label]))
                self.formula.add(Or(out_edges_clause))
            else:
                for out_edge in out_edges:
                    self.formula.add( Not(self.evars[out_edge[0]][out_edge[1]][label]) )  

            # vertex -> in_edge[0] or in_edge[1] or ... or in_edge[k]; already added
            # exactly_one(in_vertex[0], in_vertex[1], ..., in_vertex[k]);
            # vertex -> out_vertex[0] or out_vertex[1] or ... or out_vertex[k]; // todo
            # exactly_one(out_vertex[0], out_vertex[1], ..., out_vertex[k]);

            # if s => deal only with out vertices AND make sure all vars for in edges = 0;
            # if t => deal only with in vertices AND make sure all vars for out edges = 0;



    
    # Creates 2 dictionaries - vvars and evars;
    # vvars stores variables that encode vertices -> vvars[vertex][pinPairID];
    # For example, vertex is a tuple (0, 1) and pinPairID is 'a';
    # evars stores variables that encode edges -> evers[vertex_from][vertex_to][pinPairID];
    def __construct_variables(self):
        self.vvars = {}

        for vertex, _ in self.graph.graph.items():
            if not vertex in self.vvars:
                self.vvars[vertex] = {}

            for pin_pair in self.graph.pin_pairs:
                pin_pair_label = pin_pair[2]
                self.vvars[vertex][pin_pair_label] = Bool(str(vertex[0]) + "," + str(vertex[1]) + ";" + pin_pair_label)

        self.evars = {}

        all_edges = self.graph.get_all_edges()

        for edge in all_edges:
            s = edge[0] # start vertex of an edge;
            t = edge[1] # terminal vertex of an edge;

            if not s in self.evars:
                self.evars[s] = {}

            self.evars[s][t] = {}

            for pin_pair in self.graph.pin_pairs:
                pin_pair_label = pin_pair[2]
                self.evars[s][t][pin_pair_label] = Bool(str(s[0]) + "," + str(s[1]) + "; " + str(t[0]) + "," + str(t[1]) + "; " + pin_pair_label)


    def __enforce_exactly_one(self, variables: list):
        clauses = []

        for i in range(len(variables)):
            for j in range(i + 1, len(variables)):
                # variables[i] -> !variables[j]
                clauses += [[ Not(variables[i]), Not(variables[j]) ]]

        for clause in clauses:
            self.formula.add(Or(clause))



if __name__ == "__main__":
    m = 3
    
    pin_pairs = [ 
        [(0, 0), (1, 2), 'a'],
        [(2, 0), (2, 2), 'b']
    ]

    graph = Graph(m, pin_pairs)
    graph.print_as_grid()

    graph.print_as_graph()

    sol = FreeFlow2Sat(graph)
