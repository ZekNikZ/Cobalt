"""
{
  opcode: '+',
  arity: 2,
  strict_param_order: False,
  param_types: [ NUMERIC, NUMERIC ],
  postfix_param_type: None,
  name: 'addition',
  description: 'boopity boop',
#   group: 'addition',
  action: lambda x, y: x + y,
  redefinable: False
}
"""

from convex_types import *

OPERATIONS = {
    '+': {
        'opcode': '+',
        'arity': 2,
        'name': 'Addition',
        'description': 'Pop two numbers and push their sum.',
        'actions': [
            {
                'param_types': (ConvexNumber, ConvexNumber),
                'action': lambda x, y: x + y
            }
        ],
    }
}