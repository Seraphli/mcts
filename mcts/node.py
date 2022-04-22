class Node(object):
    def __init__(self, game, config, action='root', parent=None):
        self.action = action
        self.parent = parent
        self.config = config

        self.descendant = game.get_actions()
        self.untried_actions = game.get_actions()
        self.player_just_moved = game.player_just_moved

        self.children = []
        self.action_child_map = {}
        self._value = self.config.value_cls()

    def add_child(self, child):
        assert isinstance(child, Node)
        self.untried_actions.remove(child.action)
        self.children.append(child)
        self.action_child_map[child.action] = child
        return child

    def select_child_by_action(self, action):
        return self.action_child_map[action]

    def sorted_children(self):
        return sorted(self.children, key=self.config.sort_lambda)

    def uct_select_child(self):
        """
        Use the UCB1 formula to select a child node.
        Often a constant UCTK is applied so we have
        lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits
        to vary the amount of exploration versus exploitation.
        """
        return sorted(self.children, key=self.config.uct_lambda(self))[-1]

    def detach(self):
        self.parent = None
        return self

    def update(self, result, virtual_loss=0):
        self._value.update(result, virtual_loss)

    @property
    def wins(self):
        return self._value.t_wins

    @property
    def visits(self):
        return self._value.t_visits

    @property
    def value(self):
        return self._value.value

    def __repr__(self):
        return f'[P:{self.player_just_moved} A:{self.action} ' \
               f'W/V:{int(self.wins)}/{self.visits} Q:{self.value:.2f}'

    def tree_to_string(self, indent=0, deep=0, limit=-1):
        s = self.indent_string(indent) + str(self)
        if limit != -1 and deep >= limit:
            return s
        for c in self.sorted_children():
            s += c.tree_to_string(indent + 1, deep + 1, limit)
        if deep == 0:
            s += '\n'
        return s

    @staticmethod
    def indent_string(indent):
        s = '\n'
        for i in range(1, indent + 1):
            s += '| '
        return s

    def children_to_string(self):
        s = ''
        for idx, c in enumerate(self.sorted_children()):
            s += f'{idx}: {c}\n'
        return s
