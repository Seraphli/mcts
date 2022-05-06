from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcts.node import Node
    from mcts.game import Game
    from mcts.config import MCTSConfig


class MCTS(object):
    _root: Node
    _game: Game

    def __init__(self, config: MCTSConfig):
        self.config = config

    @property
    def root(self):
        return self._root

    def set_root(self, game: Game):
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
            a = self.config.random_choice(self._node.untried_actions)
            desc = self._node.descendant_desc[a]
            self._actions.append(a)
            self._game.take_action(a)
            # add child and descend tree
            child_node = self.config.node_cls(
                self._game,
                self.config,
                action=a,
                desc=desc,
                parent=self._node,
                depth=self._node.depth + 1,
            )
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
        depth = len(self._actions)
        while self._node is not None:
            # state is terminal. Update node with result
            # from POV of node.playerJustMoved
            self._node.update(self._game.get_result(self._node.player_just_moved))
            self._node.update_depth(depth)
            self._node = self._node.parent

    def uct(self, game: Game, iters: int):
        if self.config.bar:
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

        if self.config.child_verbose >= 1:
            print(self._root.children_to_string())
        if self.config.child_verbose >= 2:
            print(
                self._root.tree_to_string(
                    limit=int((self.config.child_verbose - 2) * 100)
                )
            )

        self._node = None
        self._game = None
        self._actions = None

        s = self._root.sorted_children()
        return s[0].action
