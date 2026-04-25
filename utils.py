import time
import functools


def log_call(fn):
    @functools.wraps(fn)
    def wrap(*a, **kw):
        print(f"→ {fn.__qualname__} called with kwargs={kw}")
        return fn(*a, **kw)
    return wrap


def positive(param):
    def deco(fn):
        @functools.wraps(fn)
        def wrap(*a, **kw):
            if (v := kw.get(param)) is not None and v <= 0:
                raise ValueError(f"'{param}' must be > 0, got {v}")
            return fn(*a, **kw)
        return wrap
    return deco

def timer(fn):
    @functools.wraps(fn)
    def wrap(*a, **kw):
        t = time.perf_counter()
        r = fn(*a, **kw)
        print(f"{fn.__qualname__} → {(time.perf_counter() - t) * 1000:.1f}ms")
        return r
    return wrap
