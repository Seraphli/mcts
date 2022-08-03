import random
from math import log, sqrt
from mcts.node import Node
from mcts.value import AvgValueCls


class MCTSConfig(object):
    uct_c: float
    bar: bool
    child_verbose: float

    def __init__(self):
        self.uct_c = 2
        # Can use a fixed seed random choice
        self.random_choice = random.choice
        # Can be change to AvgValueCls or MaxValueCls
        self.value_cls = AvgValueCls
        self.node_cls = Node
        # Display progressbar
        self.bar = False
        # Display search result
        self.child_verbose = 0
        # Max rollout depth, 0 stands for unlimited
        self.max_depth = 0

    def uct_lambda(self, node: Node):
        return lambda c: c.value + sqrt(self.uct_c * log(node.visits) / c.visits)

    def sorted_children(self, node: Node):
        # Can be changed to sort by visits or wins or more complex method
        # Used for choose final action
        # The first one will be selected as the best action
        return sorted(node.children, key=lambda c: c.value, reverse=True)

    def sorted_children_for_print(self, node: Node):
        # Can be changed to sort by visits or wins or more complex method
        # Only used for print debug information
        return sorted(node.children, key=lambda c: c.value, reverse=True)

    def early_stop(self, root):
        children = root.sorted_children()
        if len(children) > 2 and children[0].visits > children[1].visits * 10:
            return True
        return False
