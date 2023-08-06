from contextlib import contextmanager


class InvalidExpression(Exception):
    pass

class CircularReference(Exception):
    pass


@contextmanager
def detect_circular(refs, value):
    if value in refs:
        raise CircularReference('circular reference ({}) - reference stack: {}'.format(
            value, refs))
    refs.append(value)

    yield
    assert refs.pop() == value # NOTE: this should always be true ????
