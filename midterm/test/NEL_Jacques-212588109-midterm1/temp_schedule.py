from abc import ABC, abstractmethod
import numpy as np


class TempSchedule(ABC):

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def k(self):
        pass

    @abstractmethod
    def final_temp(self):
        pass

    def requires_obj(self):
        return False


class QASchedule(TempSchedule):

    def __init__(self,
                 initial_temp: float,
                 final_temp: float,
                 num_cycles: int):

        assert(num_cycles > 0)
        assert(final_temp <= initial_temp)

        self._initial_temp = initial_temp
        self._final_temp = final_temp
        self._num_cycles = num_cycles
        self._k = 0

    def step(self):
        t0 = self._initial_temp
        tf = self._final_temp
        k = self._k
        n = self._num_cycles

        t = tf + (t0 - tf) * ((n - k) / n)**2

        self._k += 1

        return t

    def reset(self):
        self._k = 0

    def k(self):
        return self._k

    def final_temp(self):
        return self._final_temp


class LSchedule(TempSchedule):
    def __init__(self,
                 initial_temp: float,
                 final_temp: float,
                 num_cycles: int):

        assert(num_cycles > 0)
        assert(final_temp <= initial_temp)

        self._initial_temp = initial_temp
        self._final_temp = final_temp
        self._num_cycles = num_cycles
        self._k = 0
        self._alpha = (final_temp - initial_temp) / num_cycles

    def step(self):
        t0 = self._initial_temp
        tf = self._final_temp
        k = self._k
        m = self._alpha

        t = max(t0 + m * k, tf)

        self._k += 1

        return t

    def reset(self):
        self._k = 0

    def k(self):
        return self._k

    def final_temp(self):
        return self._final_temp


class EASchedule(TempSchedule):
    def __init__(self,
                 initial_temp: float,
                 final_temp: float,
                 num_cycles: int):

        assert(final_temp <= initial_temp)
        assert(num_cycles > 0)

        self._initial_temp = initial_temp
        self._final_temp = final_temp
        self._num_cycles = num_cycles
        self._k = 0

    def step(self):
        t0 = self._initial_temp
        tf = self._final_temp
        k = self._k
        n = self._num_cycles

        exp_term = (2.0 * np.log(t0 - tf) / n) * (k - 0.5 * n)
        t = tf + (t0 - tf) * (1 / (1 + np.exp(exp_term)))

        self._k += 1

        return t

    def reset(self):
        self._k = 0

    def k(self):
        return self._k

    def final_temp(self):
        return self._final_temp + 1e-12


class MLSchedule(TempSchedule):
    def __init__(self,
                 initial_temp: float,
                 final_temp: float,
                 alpha: float):

        assert(alpha > 0.0)
        assert(final_temp <= initial_temp)

        self._initial_temp = initial_temp
        self._final_temp = final_temp
        self._alpha = alpha
        self._k = 0

    def step(self):
        t0 = self._initial_temp
        tf = self._final_temp
        k = self._k
        alpha = self._alpha

        t = t0 / (1.0 + alpha * k)

        self._k += 1

        return t

    def reset(self):
        self._k = 0

    def k(self):
        return self._k

    def final_temp(self):
        return self._final_temp
