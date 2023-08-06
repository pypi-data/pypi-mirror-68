from abc import ABCMeta, abstractmethod

from pypads import logger
from pypads.functions.loggers.base_logger import FunctionHolder
from pypads.functions.loggers.mixins import DependencyMixin, OrderMixin, IntermediateCallableMixin, TimedCallableMixin, \
    DefensiveCallableMixin


class PostRunFunction(DefensiveCallableMixin, IntermediateCallableMixin, FunctionHolder, TimedCallableMixin,
                      DependencyMixin, OrderMixin):
    """
    This class should be used to define new post run functions
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, *args, fn=None, **kwargs):
        super().__init__(*args, fn=fn, **kwargs)
        if self._fn is None:
            self._fn = self._call

    @abstractmethod
    def _call(self, pads, *args, **kwargs):
        """
        Function where to add you custom code to execute after ending the run.

        :param pads: the current instance of PyPads.
        """
        return NotImplementedError()

    def __real_call__(self, *args, **kwargs):
        from pypads.pypads import get_current_pads
        return super().__real_call__(get_current_pads(), *args, **kwargs)

    def _handle_error(self, *args, ctx, _pypads_env, error, **kwargs):
        logger.warning(str(error))
