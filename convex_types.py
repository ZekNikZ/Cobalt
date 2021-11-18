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

class ConvexNumeric(metaclass=ABCMeta):
    @abstractmethod
    def __index__(self):
        pass
    
    @abstractmethod
    def __neg__(self):
        pass

class ConvexNumber(ConvexNumeric):
    pass

class ConvexReal(ConvexNumber):
    pass

class ConvexAction:
    pass

class ConvexIter:
    pass

# ======

class ConvexInt(ConvexReal):
    def __init__(val):
        self.val = int(val)

class ConvexFloat(ConvexReal):
    def __init__(val):
        self.val = float(val)

class ConvexComplex(ConvexNumber):
    def __init__(val):
        self.val = complex(val)

class ConvexQuaternion(ConvexNumber, ConvexIter):
    pass

class ConvexString(ConvexIter):
    pass

# ======

class ConvexChar(ConvexNumeric, ConvexIter):
    pass

class ConvexRegex(ConvexString):
    pass

class ConvexList(ConvexIter):
    pass

class ConvexBlock(ConvexAction):
    pass

class ConvexOperation(ConvexAction):
    pass

class ConvexVariable(ConvexAction):
    pass
