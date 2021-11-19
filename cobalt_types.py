# __init__ = ctor
# __del__ = dtor
# __repr__ = Python representation
# __str__ = string representation (Cobalt)
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

# self.__Cobalt_type__

from abc import abstractmethod, ABCMeta
from collections import defaultdict
import decimal

# TODO: Constants
decimal.getcontext().prec = 100

class CobaltType(metaclass=ABCMeta):
    @abstractmethod
    def Cobalt_type():
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

class CobaltNumeric(CobaltType, metaclass=ABCMeta):
    def Cobalt_type():
        return 'numeric'

    @abstractmethod
    def __index__(self):
        pass

    @abstractmethod
    def __neg__(self):
        pass

class CobaltNumber(CobaltNumeric, metaclass=ABCMeta):
    def Cobalt_type():
        return 'number'

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __radd__(self, other):
        pass

class CobaltReal(CobaltNumber):
    def Cobalt_type():
        return 'real'

class CobaltAction(CobaltType):
    def Cobalt_type():
        return 'action'

class CobaltIter(CobaltType):
    def Cobalt_type():
        return 'iter'

# ======

class CobaltInt(CobaltReal):
    def Cobalt_type():
        return 'int'

    def __init__(self, val):
        self.val = int(val)

    def __index__(self):
        return self.val

    def __neg__(self):
        return CobaltInt(-self.val)

    def __add__(self, other):
        if not isinstance(other, CobaltNumber):
            raise TypeError('addition is only supported between number types')
        if isinstance(other, CobaltFloat) or isinstance(other, CobaltComplex) or isinstance(other, CobaltQuaternion):
            return other.__radd__(self)
        return CobaltInt(self.val + other.val)

    def __radd__(self, other):
        if not isinstance(other, CobaltNumber):
            raise TypeError('addition is only supported between number types')
        if isinstance(other, CobaltFloat) or isinstance(other, CobaltComplex) or isinstance(other, CobaltQuaternion):
            return other.__add__(self)
        return CobaltInt(self.val + other.val)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.val})'

    def __str__(self):
        return str(self.val)

    def __eq__(self, o: object) -> bool:
        return self.val == o.val

    def __ne__(self, o: object) -> bool:
        return self.val != o.val

class CobaltFloat(CobaltReal):
    def Cobalt_type():
        return 'float'

    def __init__(self, val):
        self.val = decimal.Decimal(val)

    def __index__(self):
        return self.val

    def __neg__(self):
        return CobaltInt(-self.val)

    def __add__(self, other):
        if not isinstance(other, CobaltNumber):
            raise TypeError('addition is only supported between number types')
        if isinstance(other, CobaltComplex) or isinstance(other, CobaltQuaternion):
            return other.__radd__(self)
        return CobaltFloat(self.val + other.val)

    def __radd__(self, other):
        if not isinstance(other, CobaltNumber):
            raise TypeError('addition is only supported between number types')
        if isinstance(other, CobaltComplex) or isinstance(other, CobaltQuaternion):
            return other.__add__(self)
        return CobaltFloat(self.val + other.val)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.val})'

    def __str__(self):
        return str(self.val)

    def __eq__(self, o: object) -> bool:
        return self.val == o.val

    def __ne__(self, o: object) -> bool:
        return self.val != o.val

class CobaltComplex(CobaltNumber):
    def Cobalt_type():
        return 'complex'

    def __init__(self, val):
        self.val = complex(val)

class CobaltQuaternion(CobaltNumber, CobaltIter):
    def Cobalt_type():
        return 'quaternion'

class CobaltString(CobaltIter):
    def Cobalt_type():
        return 'str'

# ======

class CobaltChar(CobaltNumeric, CobaltIter):
    def Cobalt_type():
        return 'str'


class CobaltRegex(CobaltString):
    def Cobalt_type():
        return 'regex'


class CobaltList(CobaltIter):
    def Cobalt_type():
        return 'list'


class CobaltBlock(CobaltAction):
    def Cobalt_type():
        return 'block'


class CobaltOperation(CobaltAction):
    def __init__(self, opcode: str):
        self._opcode = opcode

    def Cobalt_type():
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


class CobaltVariable(CobaltAction):
    def Cobalt_type():
        return 'variable'

class CobaltLiteral(CobaltAction):
    def __init__(self, val: CobaltType):
        self._val = val

    def Cobalt_type():
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