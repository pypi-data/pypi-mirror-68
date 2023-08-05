import typing as tp

from .metric_types import Metric, MetricLevel
from .metric_types.measurable_mixin import MeasurableMixin


class AggregateMetric(Metric, MeasurableMixin):
    """
    A virtual metric grabbing a few other metrics and having a single .handle() call represent a bunch of
    calls to other metrics. Ie, the following:

    >>> m1 = getMetric('summary', 'summary')
    >>> m2 = getMetric('histogram', 'histogram')
    >>> m1.runtime()
    >>> m2.runtime()

    Is the same as:

    >>> am = AggregateMetric(getMetric('summary', 'summary'), getMetric('histogram', 'histogram'))
    >>> am.runtime()

    Note that this class supports only reporting. It doesn't read data, or read/write metric levels.
    """
    __slots__ = ('metrics', )

    def __init__(self, *metrics):
        self.metrics = metrics

    def handle(self, level: tp.Union[int, MetricLevel], *args, **kwargs) -> None:
        for metric in self.metrics:
            metric.handle(level, *args, **kwargs)

    def debug(self, *args, **kwargs) -> None:
        self.handle(MetricLevel.DEBUG, *args, **kwargs)

    def runtime(self, *args, **kwargs) -> None:
        self.handle(MetricLevel.RUNTIME, *args, **kwargs)
