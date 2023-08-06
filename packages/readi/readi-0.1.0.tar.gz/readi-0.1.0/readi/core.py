import functools
import pkg_resources


class Collection(dict):
    def __init__(self, entrypoints=None):
        self._presets = {}
        self._sublcs_parents = {}
        self.entrypoints = entrypoints
        self.register_entrypoints()
        super().__init__()

    def get_name(self, child):
        '''Retrieve the name of the processor.'''
        return getattr(child, 'name', None) or child.__name__.lower()

    def is_enabled(self, child):
        '''Determine if a processor should be considered enabled or not.'''
        return child is not None and getattr(child, 'enabled', True)

    def _init_with_kw(self, name, prockw=None, **kw):
        '''Instantiate processor unless disabled by keyword arg (`{name}=False`).'''
        return (
            self[name](**mergedicts(self._presets.get(name), kw, prockw))
            if prockw is not False else None)

    def register(self, child, name=None):
        '''Register a processor.'''
        def inner(child):
            self[name or self.get_name(child)] = child
        if isinstance(child, str):
            name, child = child, None
            return inner
        return inner(child)

    def register_subclasses(self, cls, include=False):
        '''Register all subclass instances of a class.'''
        self._sublcs_parents[self.get_name(cls)] = cls
        if include:
            self.register(cls)
        for cls_i in all_subclasses(cls):
            self.register(cls_i)

    def refresh_subclasses(self):
        '''For all parent classes registered using `register_subclasses`,
        iterate over their subclasses again and register any new subclasses.
        '''
        for cls in self._sublcs_parents.values():
            self.register_subclasses(cls)

    def register_entrypoints(self, name=None):
        '''Register any processors specified using setup.py entrypoints.'''
        name = name or self.entrypoints
        if name:
            for entry_point in pkg_resources.iter_entry_points(name):
                self[entry_point.name] = entry_point.load()

    def register_variant(self, source, name=None, **kw):
        '''Register a source alias with an alternate name and additional kw params.'''
        if name:
            # NOTE: lambda so that name will use the latest version of self[source]
            self[name] = lambda *a, **kw: self[source](*a, **kw)

        name = name or source
        if name not in self._presets:
            self._presets[name] = {}
        self._presets[name].update(kw)

    def gather(self, *keys, **kw):
        '''Gather processors dependent on keyword args.'''
        keys = keys or self.keys()
        # filter out args with the names of processors - those are specific args.
        childkw = {k: kw.pop(k, None) for k in keys}
        # filter out disabled processors - maay need to be instantiated first.
        children = (self._init_with_kw(k, childkw[k], **kw) for k in keys)
        return {
            k: p for k, p in zip(keys, children)
            if p is not None and self.is_enabled(p)
        }

    def gatheritems(self, *keys, **kw):
        return list(self.gather(*keys, **kw).values())

    def getone(self, key, **kw):
        return self._init_with_kw(key, **kw)


def mergedicts(*ds):
    '''Merge multiple dictionaries. Skips over non-dict values.'''
    out = {}
    for d in ds:
        if d and isinstance(d, dict):
            out.update(d)
    return out

def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        s for c in cls.__subclasses__() for s in all_subclasses(c))

def wrap(func):
    '''Wraps functions that don't use their own closure if you want to
    return a function with bound keyword args. If you want the result
    of the function call, don't use this.

    Example:
        # needs wrap()
        @collection.register
        @readi.wrap
        def asdf(a=5, b=6):
            return a + b

        # doesn't need wrap - it returns a callable.
        @collection.register
        def asdf(a=5, b=6, c='zxcvzxvc'):
            init(c)
            def inner(a=a, b=b):
                return a + 2 * b
            return inner
    '''
    @functools.wraps(func)
    def outer(**outkw):
        @functools.wraps(func)
        def inner(*a, **kw):
            return func(*a, **dict(outkw, **kw))
        return inner
    return outer
