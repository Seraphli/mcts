import random
from math import log, sqrt
from mcts.node import Node
from mcts.value import AvgValueCls


class MCTSConfig(object):
    def __init__(self):
        self.uct_c = 2
        self.random_choice = random.choice
        self.value_cls = AvgValueCls
        self.node_cls = Node
        self.sort_lambda = lambda c: c.value
        # Display progressbar
        self.bar = False
        # Display search result
        self.child_verbose = 0

    def uct_lambda(self, node):
        return lambda c: c.value + sqrt(
            self.uct_c * log(node.visits) / c.visits)
