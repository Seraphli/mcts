from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcts.game import Game
    from mcts.config import MCTSConfig
    from typing import Union, List, Dict

from copy import deepcopy


class Node(object):
    descendant: List[any]
    descendant_desc: Dict[any, str]
    untried_actions: List[any]
    player_just_moved: int
    children: List[Node]
    action_child_map: Dict[any, Node]

    def __init__(
        self,
        game: Game,
        config: MCTSConfig,
        action: any = "root",
        desc: str = "root",
        parent: Union[Node, None] = None,
        depth: int = 0,
    ):
        self.action = action
        self.desc = desc
        self.parent = parent
        self.config = config
        self.depth = depth

        actions = game.get_actions()
        actions_desc = game.get_actions_desc()
        self.descendant = deepcopy(actions)
        self.descendant_desc = deepcopy(actions_desc)
        self.untried_actions = deepcopy(actions)
        self.player_just_moved = game.player_just_moved

        self.children = []
        self.action_child_map = {}
        self._value = self.config.value_cls()
        self._depth_estimate = 0

    def is_leaf(self):
        return not self.children

    def add_child(self, child: Node):
        assert isinstance(child, Node)
        self.untried_actions.remove(child.action)
        self.children.append(child)
        self.action_child_map[child.action] = child
        return child

    def select_child_by_action(self, action):
        return self.action_child_map[action]

    def sorted_children(self):
        return self.config.sorted_children(self)

    def sorted_children_for_print(self):
        return self.config.sorted_children_for_print(self)

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
        # Update depth align with new root
        self._decrease_depth()
        return self

    def _decrease_depth(self):
        self.depth -= 1
        for c in self.children:
            c._decrease_depth()

    def update(self, result, virtual_loss=0):
        self._value.update(result, virtual_loss)

    def update_depth(self, depth):
        assert depth >= self.depth, "depth should be larger than current depth"
        self._depth_estimate += depth - self.depth

    @property
    def depth_future(self):
        return self._depth_estimate / self.visits

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
        return (
            f"[P:{self.player_just_moved} A:{self.action} "
            f"W/V:{int(self.wins)}/{self.visits} Q:{self.value:.2f}]"
        )

    def tree_to_string(self, indent=0, deep=0, limit=-1):
        s = self.indent_string(indent) + str(self)
        if limit != -1 and deep >= limit:
            return s
        for c in self.sorted_children_for_print():
            s += c.tree_to_string(indent + 1, deep + 1, limit)
        if deep == 0:
            s += "\n"
        return s

    @staticmethod
    def indent_string(indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def children_to_string(self):
        s = ""
        for idx, c in enumerate(self.sorted_children_for_print()):
            s += f"{idx}: {c}\n"
        return s
