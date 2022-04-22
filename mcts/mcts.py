from mcts.config import MCTSConfig


class MCTS(object):
    def __init__(self, config: MCTSConfig, verbose=0):
        self.config = config
        self.verbose = verbose

    def set_root(self, game):
        self._root = self.config.node_cls(game, self.config)
        return self

    def update_root(self, action):
        new_root = self._root.select_child_by_action(action)
        self._root = new_root.detach()

    def _select(self):
        # Select
        # node is fully expanded and non-terminal
        while not self._node.untried_actions and self._node.children:
            self._node = self._node.uct_select_child()
            a = self._node.action
            self._actions.append(a)
            self._game.take_action(a)

    def _expand(self):
        # Expand
        # if we can expand (i.e. state/node is non-terminal)
        if self._node.untried_actions:
            a = self._node.untried_actions[0]
            self._actions.append(a)
            self._game.take_action(a)
            # add child and descend tree
            child_node = self.config.node_cls(
                self._game, self.config, action=a, parent=self._node)
            self._node = self._node.add_child(child_node)

    def _rollout(self):
        # Rollout - this can often be made orders of magnitude quicker
        # while state is non-terminal
        while self._game.get_actions():
            a = self.config.random_choice(self._game.get_actions())
            self._actions.append(a)
            self._game.take_action(a)

    def _backup(self):
        # Backpropagate
        # backpropagate from the expanded node and work back to the root node
        while self._node is not None:
            # state is terminal. Update node with result
            # from POV of node.playerJustMoved
            self._node.update(
                self._game.get_result(self._node.player_just_moved))
            self._node = self._node.parent

    def uct(self, game, iters):
        if self.verbose >= 1:
            from tqdm import trange
            import sys
            iterator = trange(iters, file=sys.stdout)
        else:
            iterator = range(iters)

        for _ in iterator:
            self._node = self._root
            self._game = game.clone()
            self._actions = []

            self._select()
            self._expand()
            self._rollout()
            self._backup()

        if self.verbose >= 2:
            print(self._root.children_to_string())
        if self.verbose >= 3:
            print(self._root.tree_to_string(
                limit=int((self.verbose - 3) * 100)))

        s = self._root.sorted_children()[::-1]
        return s[0].action
