Convenience facilities for objects.

*Latest release 20200517*:
Documentation improvements.

Presents:
* flavour, for deciding whether an object resembles a mapping or sequence.
* Some O_* functions for working with objects
* Proxy, a very simple minded object proxy intended to aid debugging.

## Function `copy(obj, *a, **kw)`

Convenient function to shallow copy an object with simple modifications.

Performs a shallow copy of `self` using copy.copy.

Treat all positional parameters as attribute names, and
replace those attributes with shallow copies of the original
attribute.

Treat all keyword arguments as (attribute,value) tuples and
replace those attributes with the supplied values.

## Function `flavour(obj)`

Return constants indicating the ``flavour'' of an object:
* `T_MAP`: DictType, DictionaryType, objects with an __keys__ or keys attribute.
* `T_SEQ`: TupleType, ListType, objects with an __iter__ attribute.
* `T_SCALAR`: Anything else.

## Class `O(types.SimpleNamespace)`

The `O` class is now obsolete, please subclass `types.SimpleNamespace`.

## Function `O_attritems(o)`

Generator yielding `(attr,value)` for relevant attributes of `o`.

## Function `O_attrs(o)`

Yield attribute names from `o` which are pertinent to `O_str`.

Note: this calls `getattr(o,attr)` to inspect it in order to
prune callables.

## Function `O_merge(o, _conflict=None, _overwrite=False, **kw)`

Merge key:value pairs from a mapping into an object.

Ignore keys that do not start with a letter.
New attributes or attributes whose values compare equal are
merged in. Unequal values are passed to:

    _conflict(o, attr, old_value, new_value)

to resolve the conflict. If _conflict is omitted or None
then the new value overwrites the old if _overwrite is true.

## Function `O_str(o, no_recurse=False, seen=None)`

Return a `str` representation of the object `o`.

Parameters:
* `o`: the object to describe.
* `no_recurse`: if true, do not recurse into the object's structure.
  Default: `False`.
* `seen`: a set of previously sighted objects
  to prevent recursion loops.

## Function `obj_as_dict(o, attr_prefix=None, attr_match=None)`

Return a dictionary with keys mapping to `o` attributes.

## Class `Proxy`

An extremely simple proxy object
that passes all unmatched attribute accesses to the proxied object.

Note that setattr and delattr work directly on the proxy, not the proxied object.

## Function `singleton(registry, key, factory, fargs, fkwargs)`

Obtain an object for `key` via `registry` (a mapping of `key`=>`object`.
Return `(is_new,instance)`.

If the `key` exists in the registry, return the associated object.
Otherwise create a new object by calling `factory(*fargs,**fkwargs)`
and store it as `key` in the `registry`.

The `registry` may be any mapping of `key`s to objects
but might usually be a `weakref.WeakValueMapping`
to that object references expire as normal.

*Note*: this function *is not* thread safe.
Multithreaded users should hold a mutex.

See the `SingletonMixin` class for a simple mixin to create
singleton classes,
which does provide thread safe operations.

## Class `SingletonMixin`

A mixin turning a subclass into a singleton factory.

*Note*: this should be the *first* superclass of the subclass
in order to intercept `__new__` and `__init__`.

A subclass should:
* *not* provide an `__init__` method.
* provide a `_singleton_init` method in place of the normal `__init__`
  with the usual signature `(self,*args,**kwargs)`.
* provide a `_singleton_key(cls,*args,**kwargs)` class method
  returning a key for the single registry
  computed from the positional and keyword arguments
  supplied on instance creation
  i.e. those which `__init__` would normally receive.
  This should have the same signature as `_singleton_init`
  (but using `cls` instead of `self`).

This class is thread safe for the registry operations.

Example:

    class Pool(SingletonMixin):

        @classmethod
        def _singleton_key(cls, foo, bah=3):
            return foo, bah

        def _singleton_init(self, foo, bah=3):
           ... normal __init__ stuff here ...

## Class `TrackedClassMixin`

A mixin to track all instances of a particular class.

This is aimed at checking the global state of objects of a
particular type, particularly states like counters. The
tracking is attached to the class itself.

The class to be tracked includes this mixin as a superclass and calls:

    TrackedClassMixin.__init__(class_to_track)

from its __init__ method. Note that `class_to_track` is
typically the class name itself, not `type(self)` which would
track the specific subclass. At some relevant point one can call:

    self.tcm_dump(class_to_track[, file])

`class_to_track` needs a `tcm_get_state` method to return the
salient information, such as this from cs.resources.MultiOpenMixin:

    def tcm_get_state(self):
        return {'opened': self.opened, 'opens': self._opens}

See cs.resources.MultiOpenMixin for example use.

# Release Log



*Release 20200517*:
Documentation improvements.

*Release 20200318*:
* Replace obsolete O class with a new subclass of SimpleNamespace which issues a warning.
* New singleton() generic factory function and SingletonMixin mixin class for making singleton classes.

*Release 20190103*:
* New mixin class TrackedClassMixin to track all instances of a particular class.
* Documentation updates.

*Release 20170904*:
Minor cleanups.

*Release 20160828*:
* Use "install_requires" instead of "requires" in DISTINFO.
* Minor tweaks.

*Release 20150118*:
move long_description into cs/README-obj.rst

*Release 20150110*:
cleaned out some old junk, readied metadata for PyPI
