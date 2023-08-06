from mario.registry import Registry
from typing import List, Union, Type
from uuid import uuid4
from mario.funcs import FnConfig, DoFn
from mario.util import Status
from collections import deque
from mario.sinks.base import Sink


class Pipeline:
    def __init__(self, registry: Registry, sink: Sink = None):
        self.id = str(uuid4())
        self._registry = registry
        self._configs = None
        self.time_started = None
        self.time_ended = None
        self.status = Status.NOT_STARTED
        self.steps = []
        self.result = None
        self.queue = deque()
        self.sink = sink

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.determine_status()
        self.result = self.collect_output()
        if self.sink:
            self.sink.write(self)

    def determine_status(self):
        statuses = [step["status"] for step in self.steps]
        if any(x == Status.FAIL for x in statuses):
            self.status = Status.FAIL
        elif all(x == Status.SUCCEESS for x in statuses):
            self.status = Status.SUCCEESS

    def collect_output(self):
        return {
            "id": self.id,
            "status": self.status,
            "steps": self.steps
        }

    def _resolve_fn_location(self, fn: Union[str, Type[DoFn]]):
        if isinstance(fn, str):
            return self._registry[fn]
        elif issubclass(fn, DoFn):
            return fn
        else:
            raise ValueError(
                f"Could not resolve fn {fn}. Make sure its been registered using registry.register([fn]) first."
            )

    def _prepare_config(self) -> deque:
        for conf in self._configs:
            fn = self._resolve_fn_location(conf.fn)
            func = fn(conf.name)
            self.queue.append((conf, func))
        return self.queue

    def run(self, configs: List[FnConfig]):
        self._configs = configs
        queue = self._prepare_config()
        self.status = Status.RUNNING

        while queue:
            conf, func = queue.popleft()
            if self.status != Status.FAIL:
                try:
                    func(**conf.args)
                except:
                    self.status = Status.FAIL
            self.steps.append(func.collect_output())



