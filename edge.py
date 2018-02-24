"""Graph Edge for ACO"""
class Edge:
    def __init__(self, dist = 0.0, tao = 0.0):
        self._dist = dist
        self._tao = tao

    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, value):
        self._dist = value

    @property
    def tao(self):
        return self._tao

    @tao.setter
    def tao(self, value):
        self._tao = value