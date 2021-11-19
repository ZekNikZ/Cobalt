# __init__ = ctor
# __del__ = dtor
# __repr__ = Python representation
# __str__ = string representation (Convex)
# __format__ = if custom formatting options are required beyond str()
# __lt__, __le__, __eq__, __ne__, __gt__, __ge__ = comparison
# __hash__ = hash((self.val, self.name, ...))
# __bool__ = cast to bool
# __len__ = length of object
# __getitem__ = only if `self[key]` should be supported; should throw indexerror
# __setitem__ = only if `self[key] = val` should be supported
# __iter__ = iterator for container (for list, obvious. For ints, over digits, etc.)
# __reversed__ = reverse iterator 
# __add__, __sub__, __mul__, __matmul__, __trudiv__, __floordiv__, __mod__, __divmod__, __pow__, __lshift__, __rshift__, __and__, __xor__, __or__ = normal operations (self <op> other)
# __radd__ ... = reverse operations (other <op> self)
# __iadd__ ... = (+=, -=, etc. support)
# __neg__, __pos__, __abs__, __invert__ (-, +, abs(), ~) unary operators
# __complex__, __int__, __float__ = casting
# __index__ = (operator.index()) = <int value>
# __round__, __trunc__, __floor__, __ceil__ 

# self.__convex_type__

from abc import abstractmethod, ABCMeta
from collections import defaultdict
import decimal

# TODO: Constants
decimal.getcontext().prec = 100

class ConvexType(metaclass=ABCMeta):
    @abstractmethod
    def convex_type():
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __eq__(self, o: object) -> bool:
        pass

    @abstractmethod
    def __ne__(self, o: object) -> bool:
        pass

class ConvexNumeric(ConvexType, metaclass=ABCMeta):
    def convex_type():
        return 'numeric'

    @abstractmethod
    def __index__(self):
        pass

    @abstractmethod
    def __neg__(self):
        pass

class ConvexNumber(ConvexNumeric, metaclass=ABCMeta):
    def convex_type():
        return 'number'

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __radd__(self, other):
        pass

class ConvexReal(ConvexNumber):
    def convex_type():
        return 'real'

class ConvexAction(ConvexType):
    def convex_type():
        return 'action'

class ConvexIter(ConvexType):
    def convex_type():
        return 'iter'

# ======

class ConvexInt(ConvexReal):
    def convex_type():
        return 'int'

    def __init__(self, val):
        self.val = int(val)

    def __index__(self):
        return self.val

    def __neg__(self):
        return ConvexInt(-self.val)

    def __add__(self, other):
        if not isinstance(other, ConvexNumber):
            raise TypeError('addition is only supported between number types')
        if isinstance(other, ConvexFloat) or isinstance(other, ConvexComplex) or isinstance(other, ConvexQuaternion):
            return other.__radd__(self)
        return ConvexInt(self.val + other.val)

    def __radd__(self, other):
        if not isinstance(other, ConvexNumber):
            raise TypeError('addition is only supported between number types')
        if isinstance(other, ConvexFloat) or isinstance(other, ConvexComplex) or isinstance(other, ConvexQuaternion):
            return other.__add__(self)
        return ConvexInt(self.val + other.val)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.val})'

    def __str__(self):
        return str(self.val)

    def __eq__(self, o: object) -> bool:
        return self.val == o.val

    def __ne__(self, o: object) -> bool:
        return self.val != o.val

class ConvexFloat(ConvexReal):
    def convex_type():
        return 'float'

    def __init__(self, val):
        self.val = decimal.Decimal(val)

    def __index__(self):
        return self.val

    def __neg__(self):
        return ConvexInt(-self.val)

    def __add__(self, other):
        if not isinstance(other, ConvexNumber):
            raise TypeError('addition is only supported between number types')
        if isinstance(other, ConvexComplex) or isinstance(other, ConvexQuaternion):
            return other.__radd__(self)
        return ConvexFloat(self.val + other.val)

    def __radd__(self, other):
        if not isinstance(other, ConvexNumber):
            raise TypeError('addition is only supported between number types')
        if isinstance(other, ConvexComplex) or isinstance(other, ConvexQuaternion):
            return other.__add__(self)
        return ConvexFloat(self.val + other.val)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.val})'

    def __str__(self):
        return str(self.val)

    def __eq__(self, o: object) -> bool:
        return self.val == o.val

    def __ne__(self, o: object) -> bool:
        return self.val != o.val

class ConvexComplex(ConvexNumber):
    def convex_type():
        return 'complex'

    def __init__(self, val):
        self.val = complex(val)

class ConvexQuaternion(ConvexNumber, ConvexIter):
    def convex_type():
        return 'quaternion'

class ConvexString(ConvexIter):
    def convex_type():
        return 'str'

# ======

class ConvexChar(ConvexNumeric, ConvexIter):
    def convex_type():
        return 'str'


class ConvexRegex(ConvexString):
    def convex_type():
        return 'regex'


class ConvexList(ConvexIter):
    def convex_type():
        return 'list'


class ConvexBlock(ConvexAction):
    def convex_type():
        return 'block'


class ConvexOperation(ConvexAction):
    def __init__(self, opcode: str):
        self._opcode = opcode

    def convex_type():
        return 'operation'

    @property
    def opcode(self):
        return self._opcode

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self._opcode)})"

    def __str__(self):
        return self._opcode

    def __eq__(self, o: object) -> bool:
        return self._val == o._val

    def __ne__(self, o: object) -> bool:
        return self._val != o._val


class ConvexVariable(ConvexAction):
    def convex_type():
        return 'variable'

class ConvexLiteral(ConvexAction):
    def __init__(self, val: ConvexType):
        self._val = val

    def convex_type():
        return 'literal'

    @property
    def val(self):
        return self._val

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self._val)})"

    def __str__(self):
        return str(self._val)

    def __eq__(self, o: object) -> bool:
        return self._val == o._val

    def __ne__(self, o: object) -> bool:
        return self._val != o._val

# ========

# TODO: finish this
class multiset:
    def __init__(self, *args):
        self.map = defaultdict(int)

        for key in args:
            self.map[key] += 1

    def __eq__(self, o: object) -> bool:
        if type(o) is multiset:
            return self.map == o.map
        else:
            return self == multiset(*o)

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __repr__(self) -> str:
        res = []
        for key in self:
            res.append(str(key))
        return f'{self.__class__.__name__}(' + ', '.join(res) + ')'

    def __contains__(self, key):
        return key in self.map and self.map[key] > 0

    def remove(self, key):
        if key not in self.map or self.map[key] == 0:
            raise ValueError('key not in set')
        self.map[key] -= 1

    def __iter__(self):
        for key, rep in self.map.items():
            for _ in range(rep):
                yield key