import pickle


class Game(object):
    """Game template class."""

    def __init__(self):
        """player_just_moved is required."""
        self.player_just_moved = 2

    def clone(self):
        """Clone the game state for searching.

        Returns:
            the cloned game state.

        """
        return pickle.loads(pickle.dumps(self))

    def take_action(self, action):
        """Update the game state by carrying out the given action.

        Args:
            action: the given action.

        """
        raise NotImplementedError()

    def get_actions(self):
        """Get all possible actions from this state.

        Returns:
            all possible actions.

        """
        raise NotImplementedError()

    def get_result(self, playerjm):
        """Get the game result from the viewpoint of playerjm.

        Args:
            playerjm: the player that take the action

        """
        raise NotImplementedError()

    def __repr__(self):
        pass
