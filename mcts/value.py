class ValueCls(object):
    def __init__(self):
        self._visits = 0
        self._wins = 0
        self._virtual_visits = 0
        self._virtual_wins = 0

    def apply_virtual_loss(self, virtual_loss):
        self._virtual_visits += virtual_loss
        self._virtual_wins -= virtual_loss

    def update_rule(self, v, virtual_loss=0):
        raise NotImplementedError

    def update(self, v, virtual_loss=0):
        self.update_rule(v, virtual_loss)

    @property
    def visits(self):
        return self._visits + self._virtual_visits

    @property
    def t_visits(self):
        return self._visits

    @property
    def wins(self):
        return self._wins + self._virtual_wins

    @property
    def t_wins(self):
        return self._wins

    @property
    def value(self):
        if self._visits == 0:
            return 0
        return self.wins / self.visits

    def check_virtual_loss(self):
        assert self._virtual_visits == 0 and self._virtual_wins == 0


class AvgValueCls(ValueCls):
    def update_rule(self, v, virtual_loss=0):
        self._visits += 1
        self._wins += v
        self._virtual_visits -= virtual_loss
        self._virtual_wins += virtual_loss


class MaxValueCls(ValueCls):
    def __init__(self):
        super(MaxValueCls, self).__init__()
        self._max_value = 0

    def update_rule(self, v, virtual_loss=0):
        if self._visits == 0:
            self._visits = 1
            self._wins = v
            self._max_value = v
            return
        self._virtual_visits -= virtual_loss
        self._virtual_wins += virtual_loss
        if self._max_value < v:
            self._max_value = v
        self._visits += 1
        self._wins = self._max_value * self._visits
