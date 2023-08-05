tagged_dataclasses
==================

Support for tagged unions based on dataclasses via a lightweight mixin that is supported
by mypy

```python
from typing import Optional

from dataclasses import dataclass

from tagged_dataclasses import TaggedUnion

class A:
    pass

@dataclass
class AB(A):
    pass

@dataclass
class AC(A):
    pass

@dataclass
class MyUnion(TaggedUnion[A]):
    # Optional is not optional here (this is for better support in PyCharm)
    first: Optional[AB] = None
    second: Optional[AC] = None

x = MyUnion.from_value(AB())

# support for many variations

if x.first is not None:
    pass
elif x.second is not None:
    pass

# other

if x.kind == AB:
    x.value()
elif x.kind == AC:
    x.value()



```
