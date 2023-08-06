# from . import *
import jinja2
import confuse
from .util import *
from .safe_eval import safe_eval


def finalize_config(thing):
    return thing.get() if isinstance(thing, confuse.ConfigView) else thing

env = jinja2.Environment(finalize=finalize_config)


class Subview(confuse.Subview):
    _references = []
    def resolve(self):
        return ((self._templated_value(value), s) for value, s in super().resolve())

    def _templated_value(self, value):
        with detect_circular(self._references, value):
            # convert value
            if isinstance(value, list):
                value = [self._templated_value(v) for v in value]
            elif isinstance(value, dict):
                value = {k: self._templated_value(v) for k, v in value.items()}
            elif isinstance(value, str):
                value = safe_eval(env.from_string(value).render(C=self.root()))
            return value



SubviewBackup = confuse.Subview
def enable():
    confuse.Subview = Subview

def disable():
    confuse.Subview = SubviewBackup
