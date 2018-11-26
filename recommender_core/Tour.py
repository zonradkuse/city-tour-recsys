# use z3 in order to find good tours
from z3 import *
import networkx as nx

_DEBUG = False

class Tour(nx.Graph):

    @staticmethod
    def from_pois(pois):
        t = Tour()
        for p in pois:
            t.add_node(p)

        return t

class TourSolver():

    def __init__(self):
        self.pois = {}
        self._solver = Optimize()
        self._poi_variables = {}
        self._order_variables = {}

    def add_poi(self, poi):
        self.pois[poi["NODE_ID"]] = poi
        var = Int(f'x_{poi["NODE_ID"]}')
        self._poi_variables[poi["NODE_ID"]] = var
        self._solver.add(var >= 0)
        self._solver.add(var <= 1)

    # Input: length in km
    def restrict_tour_length(self, length):
        # the sum of all parts of the tour must be less than length
        assert(false) # not implemented

    def make_poi_mandatory(self, poi_id):
        assert(false)

    def make_poi_start(self, poi_id):
        assert(false)

    def solve(self):
        self._build_ip()
        # important! first check, otherwise we segfault
        sat_result = self._solver.check()

        if _DEBUG:
            print(self._solver)
            print('-------- results in -----')
            print(sat_result)

        if sat_result == unsat:
            return Tour.from_pois(self.pois.values())

        # extract the model
        model = self._solver.model()

        if _DEBUG:
            print(model)

        # iterate through model and create the Tour
        tour = Tour.from_pois(self.pois.values())
        for pid, var in self._poi_variables.items():
            for other_pid, other_var in self._poi_variables.items():
                if pid == other_pid:
                    continue

                if model.evaluate(self._order_variables[pid, other_pid]).as_long() > 0:
                    # we choose to go from pid to other_pid
                    tour.add_edge(self.pois[pid], self.pois[other_pid])

        return tour

    def clear(self):
        # just replace the solver by a new instance
        self._solver = Optimize()

    def _build_ip(self):
        # add variables
        for pid, var in self._poi_variables.items():
            for other_pid, other_var in self._poi_variables.items():
                if pid != other_pid:
                    var = Int(f'y_{pid}_{other_pid}')
                    self._order_variables[pid, other_pid] = var
                    self._solver.add(var >= 0)
                    self._solver.add(var <= 1)

        # sum of all outgoing edges to i must be equal to x_i
        for pid, var in self._poi_variables.items():
            constr = 0
            for other_pid, other_var in self._poi_variables.items():
                if pid != other_pid:
                    constr = constr + self._order_variables[pid, other_pid]

            self._solver.add(constr == var)

        # sum of all incoming edges to i must be equal to x_i
        for pid, var in self._poi_variables.items():
            constr = 0
            for other_pid, other_var in self._poi_variables.items():
                if pid != other_pid:
                    constr = constr + self._order_variables[other_pid, pid]

            self._solver.add(constr == var)

        obj = 0
        for pid, var in self._poi_variables.items():
            obj = obj + var

        self._solver.add(obj >= 1) # we visit at least one

        # probably we will never need this - it just holds the objective value
        self._objective = self._solver.maximize(obj)

