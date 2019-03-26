from mcts.game import Game
from mcts.mcts import MCTS
from mcts.search_mgr import SearchMgr


class NimGame(Game):
    """
    A state of the game Nim. In Nim, players alternately take 1,2 or 3 chips
    with the winner being the player to take the last chip.
    In Nim any initial state of the form 4n+k for k = 1,2,3 is a win
    for player 1 (by choosing k) chips.
    Any initial state of the form 4n is a win for player 2.
    """

    def __init__(self, ch):
        super(NimGame, self).__init__()
        self.chips = ch

    def clone(self):
        st = NimGame(self.chips)
        st.player_just_moved = self.player_just_moved
        return st

    def take_action(self, action):
        assert 1 <= action <= 3 and action == int(action)
        self.chips -= action
        self.player_just_moved = 3 - self.player_just_moved

    def get_actions(self):
        return list(range(1, min([4, self.chips + 1])))

    def get_result(self, playerjm):
        assert self.chips == 0
        if self.player_just_moved == playerjm:
            # playerjm took the last chip and has won
            return 1.0
        else:
            # playerjm's opponent took the last chip and has won
            return 0.0

    def __repr__(self):
        s = 'Chips:' + str(self.chips) + \
            ' JustPlayed:' + str(self.player_just_moved)
        return s


def uct_play_game():
    game = NimGame(15)
    search_mgr = SearchMgr()
    p1, p2 = MCTS(search_mgr).set_root(game), MCTS(search_mgr).set_root(game)
    while game.get_actions():
        print(str(game))
        a1 = p1.uct(game, iters=100)
        a2 = p2.uct(game, iters=1000)
        if game.player_just_moved == 1:
            # play with values for iter_max and verbose = True
            # Player 2
            a = a2
        else:
            # Player 1
            a = a1
        print('Best Action: ' + str(a) + '\n')
        game.take_action(a)
        p1.update_root(a)
        p2.update_root(a)
    if game.get_result(game.player_just_moved) == 1.0:
        print('Player ' + str(game.player_just_moved) + ' wins!')
    elif game.get_result(game.player_just_moved) == 0.0:
        print('Player ' + str(3 - game.player_just_moved) + ' wins!')
    else:
        print('Nobody wins!')


if __name__ == '__main__':
    uct_play_game()
