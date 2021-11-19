from convex_types import *
from convex_operations import OPERATIONS
from convex_utils import print_stack

def apply_operation(stack:list, op_info, action):
    args = [stack.pop() for _ in range(op_info['arity'])]
    res = action['action'](*args[::-1])
    if res is None:
        pass
    elif type(res) is tuple:
        stack.extend(res)
    else:
        stack.append(res)

def evaluate(stack: list[ConvexType], operation_list: list[ConvexAction], variables: dict[str, ConvexType]={}):
    for i in range(len(operation_list)):
        operation = operation_list[i]

        if isinstance(operation, ConvexLiteral):
            stack.append(operation.val)
        elif isinstance(operation, ConvexOperation):
            op_info = OPERATIONS[operation.opcode]

            # TODO: pull from STDIN if not enough on stack
            stack_types = []
            for i in range(-op_info['arity'], 0):
                stack_types.append(type(stack[i]))

            for action in op_info['actions']:
                if op_info.get('postfix_param_type'):
                    # TODO
                    pass

                if isinstance(action['param_types'], (list, tuple)):
                    # strict order
                    for i in range(len(action['param_types'])):
                        if not isinstance(stack_types[i], action['param_types'][i]):
                            continue
                else:
                    # TODO: any order
                    continue

                apply_operation(stack, op_info, action)
                break
            else:
                # TODO: better error
                raise RuntimeError("invalid operation for operands on stack")

def parse(input_string: str) -> list[ConvexAction]:
    input_string += ' '

    res = []

    numeric_sign = ''
    numeric_literal = ''
    in_numeric_literal = False

    i = 0
    while i < len(input_string):
        c = input_string[i]

        if c == '-' and input_string[i + 1] in '0123456789':
            in_numeric_literal = True
            numeric_sign = '-'
            i += 1
            continue
        elif c in '01234567890' or (c == '.' and (in_numeric_literal or input_string[i + 1] in '0123456789')):
            in_numeric_literal = True
            numeric_literal += c
            i += 1
            continue

        if in_numeric_literal:
            if '.' in numeric_literal:
                res.append(ConvexLiteral(ConvexFloat(numeric_sign + numeric_literal)))
            else:
                res.append(ConvexLiteral(ConvexInt(numeric_sign + numeric_literal)))
            numeric_sign = numeric_literal = ''
            in_numeric_literal = False

        if c == ' ':
            i += 1
            continue
        elif c == "'":
            res.append(ConvexLiteral(ConvexChar(input_string[i + 1])))
            i += 1
            continue
        elif c in OPERATIONS.keys():
            res.append(ConvexOperation(c))
            i += 1
            continue

        raise RuntimeError(f"""unexpected character in input string '{input_string}' at position {i}
    {input_string}
    {' '*i}^""")

    return res

if __name__ == '__main__':
    stack = []
    evaluate(stack, [ConvexLiteral(ConvexInt(2)), ConvexLiteral(ConvexInt(3)), ConvexOperation('+')])
    print_stack(stack)