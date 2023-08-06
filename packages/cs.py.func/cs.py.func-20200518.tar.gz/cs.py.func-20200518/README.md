Convenience facilities related to Python functions.
* funccite: cite a function (name and code location)
* @prop: replacement for @property which turns internal AttributeErrors into RuntimeErrors
* some decorators to verify the return types of functions

*Latest release 20200518*:
funcname: prefer `func.__qualname__` over `func.__name__`

## Function `callmethod_if(o, method, default=None, a=None, kw=None)`

Call the named `method` on the object `o` if it exists.

If it does not exist, return `default` (which defaults to None).
Otherwise call getattr(o, method)(*a, **kw).
`a` defaults to ().
`kw` defaults to {}.

## Function `derived_from(property_name)`

A property which must be recomputed
if the revision of another property exceeds the snapshot revision.

## Function `derived_property(func, original_revision_name='_revision', lock_name='_lock', property_name=None, unset_object=None)`

A property which must be recomputed
if the reference revision (attached to self)
exceeds the snapshot revision.

## Function `funccite(func)`

Return a citation for a function (name and code location).

## Function `funcname(func)`

Return a name for the supplied function `func`.
Several objects do not have a __name__ attribute, such as partials.

## Function `prop(func)`

A substitute for the builtin @property.

The builtin @property decorator lets internal AttributeErrors escape.
While that can support properties that appear to exist conditionally,
in practice this is almost never what I want, and it masks deeper errors.
Hence this wrapper for @property that transmutes internal AttributeErrors
into RuntimeErrors.

## Function `returns_bool(func)`

Decorator for functions which should return Booleans.

## Function `returns_str(func)`

Decorator for functions which should return strings.

## Function `returns_type(func, basetype)`

Decrator which checks that a function returns values of type `basetype`.

## Function `yields_str(func)`

Decorator for generators which should yield strings.

## Function `yields_type(func, basetype)`

Decorator which checks that a generator yields values of type `basetype`.

# Release Log



*Release 20200518*:
funcname: prefer `func.__qualname__` over `func.__name__`

*Release 20190729*:
funccite: handle callables with no __code__ attribute.

*Release 20190108*:
Break import loop. Use cs.py3.raise_from for portability.

*Release 20181231*:
* Some type specific convenience wrappers for yields_type and returns_type.
* Bugfix for @prop.

*Release 20170906.1*:
Minor tweaks.

*Release 20170906*:
Bugfix for @prop.

*Release 20170608*:
New decorator @prop which works just like the builtin @property, but transmutes internal AttributeError into RuntimeError, unmasking many bugs.

*Release 20160828*:
Use "install_requires" instead of "requires" in DISTINFO.

*Release 20150115*:
First PyPI release.
