class EulerScheme:
    """
    Compute the result of an SDE using euler scheme
    """
    def __init__(self, env, W):
        self._W = W
        self._env = env

    def result(self):
        ans = self._env.S0
        for i in range(len(self._env.x) - 1):
            temp = ans
            ans = temp + self._env.b * temp *\
                (self._env.x[i + 1] - self._env.x[i]) +\
                self._env.sig * temp * (self._W[i + 1] - self._W[i])
        return ans

    # GETTERS, SETTERS AND PROPERTIES #

    def _get_env(self):
        return self._env

    def _set_env(self, env):
        self._env = env

    def _get_W(self):
        return self._W

    def _set_W(self, W):
        self._W = W

    W = property(_get_W, _set_W)
    env = property(_get_env, _set_env)
