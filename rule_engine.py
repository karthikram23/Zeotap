<<<<<<< SEARCH
=======
import ast
import operator

class Node:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

def create_rule(rule_string):
    def parse_expression(node):
        if isinstance(node, ast.BoolOp):
            return Node(
                "operator",
                "AND" if isinstance(node.op, ast.And) else "OR",
                parse_expression(node.values[0]),
                parse_expression(node.values[1])
            )
        elif isinstance(node, ast.Compare):
            left = node.left.id
            op = type(node.ops[0]).__name__
            right = node.comparators[0].value
            return Node("operand", f"{left} {op} {right}")
        else:
            raise ValueError(f"Unsupported node type: {type(node)}")

    tree = ast.parse(rule_string, mode='eval')
    return parse_expression(tree.body)

def combine_rules(rules):
    if not rules:
        return None
    if len(rules) == 1:
        return create_rule(rules[0])

    combined = Node("operator", "AND")
    combined.left = create_rule(rules[0])
    combined.right = combine_rules(rules[1:])
    return combined

def evaluate_rule(node, data):
    if node.type == "operator":
        if node.value == "AND":
            return evaluate_rule(node.left, data) and evaluate_rule(node.right, data)
        elif node.value == "OR":
            return evaluate_rule(node.left, data) or evaluate_rule(node.right, data)
    elif node.type == "operand":
        left, op, right = node.value.split()
        left_value = data.get(left)
        right_value = ast.literal_eval(right)

        ops = {
            '>': operator.gt,
            '<': operator.lt,
            '>=': operator.ge,
            '<=': operator.le,
            '==': operator.eq,
            '!=': operator.ne
        }

        return ops[op](left_value, right_value)

    raise ValueError(f"Invalid node type: {node.type}")
>>>>>>> REPLACE
