##############
# ERRORS
############## 
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'\nFile: {self.pos_start.fn}, line {self.pos_start.ln + 1}\n'
        result += string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end) + '\n'
        return result
    
class SemanticError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Semantic Error', details)

class DomainError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Semantic Error', details)

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'\nFile: {self.pos_start.fn}, line {self.pos_start.ln + 1}\n\n'
        return result

class ParseError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Parse Failure', details)

def string_with_arrows(text, pos_start, pos_end):
    result = ''

    # Calculate indices
    idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0: idx_end = len(text)

    # Generate each line
    line_count = pos_end.ln - pos_start.ln + 1
    for i in range(line_count):
        # Calculate line columns
        line = text[idx_start:idx_end]
        col_start = pos_start.col if i == 0 else 0
        col_end = pos_end.col if i == line_count - 1 else len(line) - 1

        # Append to result
        result += line + '\n'
        if pos_start.idx == pos_end.idx and pos_start.ln == pos_end.ln and pos_start.col == pos_end.col:
            result += ' ' * col_start + '^'
        else:
            result += ' ' * col_start + '^' * (col_end - col_start)

        # Re-calculate indices
        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(text)

    return result.replace('\t', ' ')

###################
# AST Nodes
###################

class ASTNode:
    def __init__(self, data, pos_start=None, pos_end=None):
        self.data = data
        self.children = []
        self.parent = None
        self.pos_start = pos_start
        self.pos_end = pos_end

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def print_tree(self):
        spaces = ' ' * self.get_level() * 3 
        prefix = spaces + "ᴸ--" if self.parent else spaces
        print(prefix + str(self.data))
        if self.children:
            for child in self.children:
                child.print_tree()

    def get_parent(self):
        return self.parent
    
    def get_leftmost_sibling(self):
        if self.parent:
            return self.parent.children[0]
        return None
    
    def get_right_sibling(self):
        if self.parent:
            idx = self.parent.children.index(self)
            if idx < len(self.parent.children) - 1:
                return self.parent.children[idx + 1]
        return None
    
class NumNode(ASTNode): # for numbers
    def __init__(self, value, pos_start=None, pos_end=None):
        super().__init__(f"Number: {value}", pos_start, pos_end)
        self.value = value

    def __repr__(self):
        return f"{self.value}"

class BinOpNode(ASTNode): # binary operation
    def __init__(self, left, op, right, pos_start=None, pos_end=None):
        super().__init__(f"Binary Operation: {op.type}", pos_start, pos_end)
        self.left = left
        self.op = op.type
        self.right = right
        self.add_child(left)
        self.add_child(right)

    def __repr__(self):
        return f'BinOpNode_Object: {self.op}'

class RelOpNode(ASTNode): # relational operation
    def __init__(self, left, op, right, pos_start=None, pos_end=None):
        super().__init__(f"Relational Operation: {op.type}", pos_start, pos_end)
        self.left = left
        self.op = op.type
        self.right = right
        self.add_child(left)
        self.add_child(right)

class LogOpNode(ASTNode): # logical operation
    def __init__(self, left, op, right, pos_start=None, pos_end=None):
        super().__init__(f"Logical Operation: {op.type}", pos_start, pos_end)
        self.left = left
        self.op = op.type
        self.right = right
        self.add_child(left)
        self.add_child(right)

class UnaryOpNode(ASTNode): # unary operation
    def __init__(self, op, expr, pre=False, post=False, pos_start=None, pos_end=None):
        super().__init__("Unary Operation", pos_start, pos_end)
        self.op = UnaryOperator(op, pos_start, pos_end)
        self.expr = expr
        self.pre = pre
        self.post = post
        if pre: self.add_child(self.op)
        self.add_child(expr)
        if post: self.add_child(self.op)

    def __repr__(self):
        if self.pre:
            return f"{self.op}{self.expr}"
        elif self.post:
            return f"{self.expr}{self.op}"
        else:
            return f"{self.op} {self.expr}"
    
class UnaryOperator(ASTNode): # unary operator
    def __init__(self, op, pos_start=None, pos_end=None):
        super().__init__(f"Unary Operator: {op.type}", pos_start, pos_end)
        self.op = op.type

class ExponentNode(ASTNode): # exponentiation
    def __init__(self, left, right, pos_start=None, pos_end=None):
        super().__init__("Exponentiation", pos_start, pos_end)
        self.left = left
        self.right = right
        self.add_child(left)
        self.add_child(right)

class BoolNode(ASTNode):
    def __init__(self, value, pos_start=None, pos_end=None):
        super().__init__(f"Bool: {value}", pos_start, pos_end)
        self.value = value

    def __repr__(self):
        return f"BoolNode_Object: {self.value}"

class NullNode(ASTNode):
    def __init__(self, value, pos_start=None, pos_end=None):
        super().__init__(f"Null", pos_start, pos_end)
        self.value = value
    
    def __repr__(self):
        return f"NullNode_Object"
        
class RestrictNode(ASTNode): # for restrict keyword
    def __init__(self, pos_start=None, pos_end=None):
        super().__init__("Restrict", pos_start, pos_end)
    
    def __repr__(self):
        return f"RestrictNode_Object"

class DatatypeNode(ASTNode): # for datatype keywords
    def __init__(self, datatype, pos_start=None, pos_end=None):
        super().__init__(f"Datatype: {datatype}", pos_start, pos_end)
        self.datatype = datatype
    
    def __repr__(self):
        return f"DatatypeNode_Object: {self.datatype}"

class IdNode(ASTNode): # for identifier names
    def __init__(self, name, pos_start=None, pos_end=None):
        super().__init__(f"Identifier: {name}", pos_start, pos_end)
        self.name = name

    def __repr__(self):
        return f"IdNode_Object: {self.name}"

class VarDecNode(ASTNode): # for variable assignments
    def __init__(self, restrict, datatype, name, value, pos_start=None, pos_end=None):
        super().__init__("Variable Declaration", pos_start, pos_end)
        self.restrict = restrict
        self.datatype = datatype
        self.name = name
        self.value = value
        if restrict:
            self.add_child(RestrictNode(pos_start, pos_end))
        self.add_child(DatatypeNode(datatype, pos_start, pos_end))
        self.add_child(IdNode(name, pos_start, pos_end))
        if value:
            self.add_child(value)

    def __repr__(self):
        restrict_str = " restrict" if self.restrict else ""
        return f"VarDecNode_Object: {self.datatype} {self.name} = {self.value}{restrict_str}"

class VarAssignNode(ASTNode): # for variable assignments
    def __init__(self, name, value, pos_start=None, pos_end=None):
        super().__init__("Variable Assignment", pos_start, pos_end)
        self.name = name
        self.value = value
        self.add_child(IdNode(name, pos_start, pos_end))
        self.add_child(value)

    def __repr__(self):
        return f"VarAssignNode_Object: {self.name}"

class ClanDecNode(ASTNode): # for arrays
    def __init__(self, restrict, datatype, name, size1=None, size2=None, initial_values1=None, initial_values2=None, pos_start=None, pos_end=None):
        super().__init__("Clan Declaration", pos_start, pos_end)
        self.restrict = restrict
        self.datatype = datatype
        self.name = name
        self.size1 = size1
        self.size2 = size2
        self.initial_values1 = initial_values1 or []
        self.initial_values2 = initial_values2 or []
        self.add_child(DatatypeNode(datatype, pos_start, pos_end))
        self.add_child(IdNode(name, pos_start, pos_end))
        if size1:
            self.add_child(size1)
        if size2:
            self.add_child(size2)
        if initial_values1:
            self.add_child(ClanLiteralNode(initial_values1, pos_start, pos_end))
        if initial_values2:
            self.add_child(ClanLiteralNode(initial_values2, pos_start, pos_end))

    def __repr__(self):
        if self.initial_values1:
            return f"{self.datatype} {self.name}[{self.size}] = {self.initial_values}"
        else:
            return f"{self.datatype} {self.name}[{self.size}]"

class ClanLiteralNode(ASTNode): # for clan literals
    def __init__(self, values, pos_start=None, pos_end=None):
        super().__init__(f"Clan Literal: {{{', '.join(str(value) for value in values)}}}", pos_start, pos_end)
        self.values = values
        for value in values:
            self.add_child(value)

    def __repr__(self):
        return f"ClanLiteralNode({', '.join(repr(value) for value in self.values)})"
    
class ClanIndexNode(ASTNode): # for array indexing
    def __init__(self, index, pos_start=None, pos_end=None):
        super().__init__("Clan Index", pos_start, pos_end)
        self.index = index
        self.add_child(index)

    def __repr__(self):
        return f"{self.index}"

class ClanSizeNode(ASTNode): # for array size
    def __init__(self, size, pos_start=None, pos_end=None):
        super().__init__("Clan Size", pos_start, pos_end)
        self.size = size
        self.add_child(size)

    def __repr__(self):
        return f"ClanSizeNode({repr(self.size)})"
    
class ClanAccessNode(ASTNode): # for array access
    def __init__(self, name, index, pos_start=None, pos_end=None):
        super().__init__("Clan Access", pos_start, pos_end)
        self.name = name
        self.index = index
        self.add_child(IdNode(name, pos_start, pos_end))
        self.add_child(index)

class ClanIndexAssignNode(ASTNode): # for array index assignments
    def __init__(self, name, index, values, pos_start=None, pos_end=None):
        super().__init__("Clan Index Assign", pos_start, pos_end)
        self.name = name
        self.index = index
        self.values = values
        self.add_child(IdNode(name, pos_start, pos_end))
        self.add_child(index)
        for value in values:
            self.add_child(value)

    def __repr__(self):
        return f"{self.name}[{self.index}] = {self.values}"
    
class ClanAssignNode(ASTNode): # for assigning the whole array
    def __init__(self, name, values, pos_start=None, pos_end=None):
        super().__init__("Clan Assign", pos_start, pos_end)
        self.name = name
        self.values = values
        self.add_child(IdNode(name, pos_start, pos_end))
        self.add_child(ClanLiteralNode(values, pos_start, pos_end))

    def __repr__(self):
        return f"{self.name} = {self.values}"

class CurseDecNode(ASTNode): # for functions
    def __init__(self, datatype, name, parameters, body, pos_start=None, pos_end=None):
        super().__init__("Curse Declaration", pos_start, pos_end)
        self.datatype = datatype
        self.name = name
        self.parameters = parameters
        self.body = body
        self.add_child(DatatypeNode(datatype, pos_start, pos_end))
        self.add_child(IdNode(name, pos_start, pos_end))
        for param in parameters:
            self.add_child(param)
        self.add_child(body)

class CurseDomainNode(ASTNode): # for function domain
    def __init__(self, body, pos_start=None, pos_end=None):
        super().__init__("Main Curse", pos_start, pos_end)
        self.body = body
        self.add_child(body)

    def __repr__(self):
        return f"{self.body}"

class ParamNode(ASTNode): # for function parameters
    def __init__(self, datatype, name, pos_start=None, pos_end=None):
        super().__init__("Parameter", pos_start, pos_end)
        self.datatype = datatype
        self.name = name
        self.add_child(DatatypeNode(datatype, pos_start, pos_end))
        self.add_child(IdNode(name, pos_start, pos_end))

class BodyNode(ASTNode): # for body of functions and vows and boogies and cycles and sustains and perform-sustains
    def __init__(self, pos_start=None, pos_end=None):
        super().__init__("Body", pos_start, pos_end)

class CurseCallNode(ASTNode): # for curse calls
    def __init__(self, name, arguments, pos_start=None, pos_end=None):
        super().__init__("Curse Call", pos_start, pos_end)
        self.name = name
        self.arguments = arguments
        self.add_child(IdNode(name, pos_start, pos_end))
        if arguments:
            args_node = ASTNode("Arguments", pos_start, pos_end)
            for arg in arguments:
                args_node.add_child(arg)
            self.add_child(args_node)

    def __repr__(self):
        return f'CurseCallNode_Object: {self.name}'

class StringNode(ASTNode): # for strings
    def __init__(self, value, pos_start=None, pos_end=None):
        super().__init__(f"String: {value}", pos_start, pos_end)
        self.value = value

    def __repr__(self):
        return f'StringNode_Object'

class StringConcatNode(ASTNode): # for string concatenations
    def __init__(self, left, op, right, pos_start=None, pos_end=None):
        super().__init__("String Concatenation", pos_start, pos_end)
        self.left = left
        self.op = op.type
        self.right = right
        self.add_child(left)
        self.add_child(right)

    def __repr__(self):
        return f"StringConcatNode_Object: {self.left} {self.op} {self.right}"

class InvokeNode(ASTNode): # for printing invoke("Hello, World!")
    def __init__(self, value, pos_start=None, pos_end=None):
        super().__init__("Invoke Statement", pos_start, pos_end)
        self.value = value
        self.add_child(value)

class CaptureNode(ASTNode): # for user input, capture(id)
    def __init__(self, name, pos_start=None, pos_end=None):
        super().__init__("Capture Statement", pos_start, pos_end)
        self.name = name
        self.add_child(name)

class CleaveNode(ASTNode): # for cleave statements, cleave(id, index1Start, index2End)
    def __init__(self, name, index1, index2, pos_start=None, pos_end=None):
        super().__init__("Cleave Statement", pos_start, pos_end)
        self.name = name
        self.index1 = index1
        self.index2 = index2
        self.add_child(name)
        self.add_child(index1)
        self.add_child(index2)

class DismantleNode(ASTNode): # for dismantle statements, dismantle(id, delimiter)
    def __init__(self, name, delimiter, pos_start=None, pos_end=None):
        super().__init__("Dismantle Statement", pos_start, pos_end)
        self.name = name
        self.delimiter = delimiter
        self.add_child(name)
        self.add_child(delimiter)

class LenNode(ASTNode): # for len statements, len(id)
    def __init__(self, name, pos_start=None, pos_end=None):
        super().__init__("Len Statement", pos_start, pos_end)
        self.name = name
        self.add_child(name)

class RecallNode(ASTNode): # for return statements
    def __init__(self, value, pos_start=None, pos_end=None):
        super().__init__("Recall Statement", pos_start, pos_end)
        self.value = value
        if value:
            self.add_child(value)
    def __repr__(self):
        return f'RecallNode_Object: {self.value}'

class DismissNode(ASTNode): # for break statements
    def __init__(self, pos_start=None, pos_end=None):
        super().__init__("Dismiss", pos_start, pos_end)

class HopNode(ASTNode): # for continue statements
    def __init__(self, pos_start=None, pos_end=None):
        super().__init__("Hop", pos_start, pos_end)

class VowNode(ASTNode): # if-else (vow-else)
    def __init__(self, condition, body, else_vows=None, else_body=None, pos_start=None, pos_end=None):
        super().__init__("Vow Statement", pos_start, pos_end)
        self.condition = condition
        self.body = body
        self.else_vows = else_vows or []
        self.else_body = else_body
        self.add_child(condition)
        self.add_child(body)
        for else_vow in self.else_vows:
            self.add_child(else_vow)
        if else_body:
            self.add_child(else_body)

    def __repr__(self):
        return f"VowNode({self.condition}, {self.body}, {self.else_body})"

class ElseVow(ASTNode):
    def __init__(self, condition, body, pos_start=None, pos_end=None):
        super().__init__("Else Vow", pos_start, pos_end)
        self.condition = condition
        self.body = body
        self.add_child(condition)
        self.add_child(body)

class ElseNode(ASTNode):
    def __init__(self, body, pos_start=None, pos_end=None):
        super().__init__("Else", pos_start, pos_end)
        self.body = body
        self.add_child(body)

class BoogieNode(ASTNode): # switch-case (boogie)
    def __init__(self, expression, cases, pos_start=None, pos_end=None):
        super().__init__("Boogie Statement", pos_start, pos_end)
        self.expression = expression
        self.cases = cases
        if expression:
            self.add_child(expression)
        for case in cases:
            self.add_child(case)

    def __repr__(self):
        return f"BoogieNode({self.expression}, {self.cases})"

class WoogieTrueNode(ASTNode): # for cases/woogie of boogie true statements (switch true)
    def __init__(self, condition, body, pos_start=None, pos_end=None):
        super().__init__("Woogie True Statement", pos_start, pos_end)
        self.condition = condition
        self.body = body
        self.add_child(condition)
        self.add_child(body)

class WoogieNode(ASTNode): # for cases/woogie of standard boogie statements (switch)
    def __init__(self, condition, body, pos_start=None, pos_end=None):
        super().__init__("Woogie Statement", pos_start, pos_end)
        self.condition = condition
        self.body = body
        self.add_child(condition)
        self.add_child(body)

class DefaultCaseNode(ASTNode): # for default cases
    def __init__(self, body, pos_start=None, pos_end=None):
        super().__init__("Default Case", pos_start, pos_end)
        self.body = body
        self.add_child(body)

class SustainNode(ASTNode): # while loop (sustain)
    def __init__(self, condition, body, pos_start=None, pos_end=None):
        super().__init__("Sustain Statement", pos_start, pos_end)
        self.condition = condition
        self.body = body
        self.add_child(condition)
        self.add_child(body)

    def __repr__(self):
        return f"SustainNode({self.condition}, {self.body})"

class PerformSustainNode(ASTNode): # do-while loop (perform-sustain)
    def __init__(self, body, condition, pos_start=None, pos_end=None):
        super().__init__("PerformSustain Statement", pos_start, pos_end)
        self.body = body
        self.condition = condition
        self.add_child(body)
        self.add_child(condition)

    def __repr__(self):
        return f"PerformSustainNode({self.body}, {self.condition})"

class CycleNode(ASTNode): # for-loop (cycle)
    def __init__(self, cycle_condition, body, pos_start=None, pos_end=None):
        super().__init__("Cycle Statement", pos_start, pos_end)
        self.cycle_condition = cycle_condition
        self.body = body
        self.add_child(cycle_condition)
        self.add_child(body)

    def __repr__(self):
        return f"CycleNode({self.cycle_condition}, {self.body})"

class CycleConditionNode(ASTNode): # for-loop initialization, condition, and iteration
    def __init__(self, init, condition, iteration, pos_start=None, pos_end=None):
        super().__init__("Cycle Condition", pos_start, pos_end)
        self.init = init
        self.condition = condition
        self.iteration = iteration
        self.add_child(init)
        self.add_child(condition)
        self.add_child(iteration)

    def __repr__(self):
        return f"{self.init}; {self.condition}; {self.iteration}"

    
##################
## AST Traverser
##################

class ASTVisitor:
    def visit(self, node, parent=None):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, parent)

    def generic_visit(self, node, parent):
        if parent is None:
            print(f"Visiting root node: {type(node).__name__}")
        self.visit_node(node, parent)
        self.visit_children(node)

    def visit_node(self, node, parent):
        pass

    def visit_children(self, node):
        for child in node.children:
            print(f"Child node: {type(child).__name__}, Parent node: {type(node).__name__}")
            self.visit(child, node)

class MyASTVisitor(ASTVisitor):
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.errors = []
        self.unresolved_cases = []  # List to keep track of unresolved cases

    def visit_NumNode(self, node, parent):
        print(f"Visiting NumNode with value: {node.value}")
        self.visit_children(node)
        print(f"Exiting NumNode")

    def visit_DatatypeNode(self, node, parent):
        print(f"Visiting DatatypeNode with type: {node.datatype}")
        self.visit_children(node)
        print(f"Exiting DatatypeNode")

    def visit_StringNode(self, node, parent):
        print(f"Visiting StringNode with value: {node.value}")
        self.visit_children(node)
        print(f"Exiting StringNode")

    def visit_BoolNode(self, node, parent):
        print(f"Visiting BoolNode with value: {node.value}")
        self.visit_children(node)
        print(f"Exiting BoolNode")

    def visit_NullNode(self, node, parent):
        print(f"Visiting NullNode")
        self.visit_children(node)
        print(f"Exiting NullNode")

    def visit_ExponentNode(self, node, parent):
        print(f"Visiting ExponentNode")
        self.visit_children(node)
        print(f"Exiting ExponentNode")

    def visit_BinOpNode(self, node, parent):
        print(f"Visiting BinOpNode with operator: {node.op}")
        left_type = self.infer_type(node.left)
        right_type = self.infer_type(node.right)

        if left_type == 'null' or right_type == 'null':
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot perform binary operation on Null value"))

        if node.op == '/':
            if isinstance(node.right, NumNode) and node.right.value == 0:
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero"))

        if left_type != right_type:
            if (left_type == 'string' and right_type in ['int', 'float']) or (right_type == 'string' and left_type in ['int', 'float']):
                if not isinstance(parent, StringConcatNode):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch: Cannot concatenate '{left_type}' and '{right_type}'"))
            elif left_type == 'bool' and right_type == 'int':
                if isinstance(parent, BinOpNode):
                    evaluation = eval(f"{node.left.value} {node.op} {node.right.value}")
                    if evaluation == 0:
                        if isinstance(parent, BinOpNode) and parent.op == '/' and parent.right == node:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero"))
                pass
            elif left_type == 'int' and right_type == 'bool':
                if isinstance(parent, BinOpNode):
                    evaluation = eval(f"{node.left.value} {node.op} {node.right.value}")
                    if evaluation == 0:
                        if isinstance(parent, BinOpNode) and parent.op == '/' and parent.right == node:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero"))
                pass
            elif left_type == 'bool' and right_type == 'float':
                if isinstance(parent, BinOpNode):
                    evaluation = eval(f"{node.left.value} {node.op} {node.right.value}")
                    if evaluation == 0:
                        if isinstance(parent, BinOpNode) and parent.op == '/' and parent.right == node:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero"))
                pass
            elif left_type == 'float' and right_type == 'bool':
                if isinstance(parent, BinOpNode):
                    evaluation = eval(f"{node.left.value} {node.op} {node.right.value}")
                    if evaluation == 0:
                        if isinstance(parent, BinOpNode) and parent.op == '/' and parent.right == node:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero"))
                pass
            elif left_type == 'int' and right_type == 'float':
                if isinstance(parent, BinOpNode):
                    evaluation = eval(f"{node.left.value} {node.op} {node.right.value}")
                    if evaluation == 0:
                        if isinstance(parent, BinOpNode) and parent.op == '/' and parent.right == node:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero"))
                pass
            elif left_type == 'float' and right_type == 'int':
                if isinstance(parent, BinOpNode):
                    evaluation = eval(f"{node.left.value} {node.op} {node.right.value}")
                    if evaluation == 0:
                        if isinstance(parent, BinOpNode) and parent.op == '/' and parent.right == node:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero"))
                pass
            else:
                if isinstance(node.left, IdNode):
                    self.unresolved_cases.append((node.left, node))
                    return
                if isinstance(node.right, IdNode):
                    self.unresolved_cases.append((node.right, node))
                    return
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch: '{left_type}' and '{right_type}'"))
        else:
            if isinstance(parent, BinOpNode):
                if left_type == 'int' and right_type == 'int':
                    print("686")
                    evaluation = eval(f"{node.left.value} {node.op} {node.right.value}")
                    if evaluation == 0:
                        if isinstance(parent, BinOpNode) and parent.op == '/' and parent.right == node:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero"))
                elif left_type == 'float' and right_type == 'float':
                    evaluation = eval(f"{node.left.value} {node.op} {node.right.value}")
                    if evaluation == 0:
                        if isinstance(parent, BinOpNode) and parent.op == '/' and parent.right == node:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero"))
                elif left_type == 'bool' and right_type == 'bool':
                    evaluation = eval(f"{node.left.value} {node.op} {node.right.value}")
                    if evaluation == 0:
                        if isinstance(parent, BinOpNode) and parent.op == '/' and parent.right == node:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero"))
        self.visit_children(node)
        print(f"Exiting BinOpNode")

    def visit_RelOpNode(self, node, parent):
        print(f"Visiting RelOpNode with operator: {node.op}")
        self.visit_children(node)
        print(f"Exiting RelOpNode")

    def visit_LogOpNode(self, node, parent):
        print(f"Visiting LogOpNode with operator: {node.op}")
        self.visit_children(node)
        print(f"Exiting LogOpNode")

    def visit_UnaryOpNode(self, node, parent):
        print(f"Visiting UnaryOpNode with operator: {node.op.op}")
        self.visit_children(node)
        print(f"Exiting UnaryOpNode")

    def visit_IdNode(self, node, parent):
        print(f"Visiting IdNode with name: {node.name}")
        if isinstance(parent, (CurseDecNode, CurseDomainNode)):
            print(f"IdNode '{node.name}' is a parameter of a curse declaration")
        if not self.symbol_table.get(node.name):
            self.unresolved_cases.append((node, parent))
        print(f"Exiting IdNode")

    def visit_VarDecNode(self, node, parent):
        print(f"Visiting VarDecNode with type: {node.datatype}")
        if not isinstance(parent, (CycleConditionNode)) and self.symbol_table.get_local(node.name):
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Variable '{node.name}' already declared"))
        else:
            self.symbol_table.set(node.name, node)  # Store the VarDecNode object itself
        self.visit_children(node)
        print(f"Exiting VarDecNode")

    def visit_VarAssignNode(self, node, parent):
        print(f"Visiting VarAssignNode with name: {node.name}")
        if not self.symbol_table.get(node.name):
            self.unresolved_cases.append((node, parent))
        elif isinstance(node.value, BinOpNode):
            self.unresolved_cases.append((node, parent))
        else:
            value_type = self.infer_type(node.value)
            var_type = self.symbol_table.get_type(node.name)
            if var_type != value_type:
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch: Expected '{var_type}', got '{value_type}'"))
        self.visit_children(node)
        print(f"Exiting VarAssignNode")

    def visit_ClanDecNode(self, node, parent):
        print(f"Visiting ClanDecNode with name: {node.name}")
        if self.symbol_table.get(node.name):
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Clan '{node.name}' already declared"))
        else:
            self.symbol_table.set(node.name, node.datatype)
        if node.initial_values1:
            for value in node.initial_values1:
                value_type = self.infer_type(value)
                if node.datatype != value_type:
                    self.errors.append(SemanticError(value.pos_start, value.pos_end, f"Type mismatch in initial values: Expected '{node.datatype}', got '{value_type}'"))
        if node.initial_values2:
            for value in node.initial_values2:
                value_type = self.infer_type(value)
                if node.datatype != value_type:
                    self.errors.append(SemanticError(value.pos_start, value.pos_end, f"Type mismatch in initial values: Expected '{node.datatype}', got '{value_type}'"))
        self.visit_children(node)
        print(f"Exiting ClanDecNode")

    def visit_ClanLiteralNode(self, node, parent):
        print(f"Visiting ClanLiteralNode with values: {node.values}")
        self.visit_children(node)
        print(f"Exiting ClanLiteralNode")

    def visit_ClanIndexNode(self, node, parent):
        print(f"Visiting ClanIndexNode with index: {node.index}")
        self.visit_children(node)
        print(f"Exiting ClanIndexNode")

    def visit_ClanSizeNode(self, node, parent):
        print(f"Visiting ClanSizeNode with size: {node.size}")
        self.visit_children(node)
        print(f"Exiting ClanSizeNode")

    def visit_ClanAccessNode(self, node, parent):
        print(f"Visiting ClanAccessNode with name: {node.name}")
        symbol = self.symbol_table.get(node.name)
        if symbol is None:
            self.unresolved_cases.append((node, parent))
        self.visit_children(node)
        print(f"Exiting ClanAccessNode")

    def visit_ClanIndexAssignNode(self, node, parent):
        print(f"Visiting ClanIndexAssignNode with name: {node.name}")
        symbol_type = self.symbol_table.get_type(node.name)
        if symbol_type is None:
            self.unresolved_cases.append((node, parent))
        else:
            for value in node.values:
                value_type = self.infer_type(value)
                if symbol_type != value_type:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch: Expected '{symbol_type}', got '{value_type}'"))
        self.visit_children(node)
        print(f"Exiting ClanIndexAssignNode")

    def visit_ClanAssignNode(self, node, parent):
        print(f"Visiting ClanAssignNode with name: {node.name}")
        symbol = self.symbol_table.get(node.name)
        if symbol is None:
            self.unresolved_cases.append((node, parent))
        self.visit_children(node)
        print(f"Exiting ClanAssignNode")

    def visit_CurseDecNode(self, node, parent):
        print(f"Visiting CurseDecNode with name: {node.name}")
        if self.symbol_table.get(node.name):
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Curse '{node.name}' already declared"))
        else:
            self.symbol_table.set(node.name, node)  # Store the CurseDecNode object itself
        self.symbol_table.push()  # Enter new scope for function body
        for param in node.parameters:
            self.symbol_table.set(param.name, param)  # Store the ParamNode object itself
        self.visit_children(node)
        self.symbol_table.pop()  # Exit function scope
        print(f"Exiting CurseDecNode")

    def visit_CurseDomainNode(self, node, parent):
        print(f"Visiting CurseDomainNode")
        if self.symbol_table.get("domain"):
            self.errors.append(SemanticError(node.pos_start, node.pos_end, "Multiple 'domain' declarations are not allowed"))
        else:
            self.symbol_table.set("domain", "CurseDomain")
        self.symbol_table.push()  # Enter new scope for domain body
        self.visit_children(node)
        self.symbol_table.pop()  # Exit domain scope
        print(f"Exiting CurseDomainNode")

    def visit_ParamNode(self, node, parent):
        print(f"Visiting ParamNode with name: {node.name}")
        if parent is None and self.symbol_table.get(node.name):
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Parameter '{node.name}' already declared"))
        else:
            self.symbol_table.set(node.name, node.datatype)
        self.visit_children(node)
        print(f"Exiting ParamNode")

    def visit_BodyNode(self, node, parent):
        print(f"Visiting BodyNode")
        self.symbol_table.push()  # Enter new scope for body
        self.visit_children(node)
        self.symbol_table.pop()  # Exit body scope
        print(f"Exiting BodyNode")

    def visit_CurseCallNode(self, node, parent):
        print(f"Visiting CurseCallNode with name: {node.name}")
        curse_node = self.symbol_table.get(node.name)
        if curse_node is None:
            self.unresolved_cases.append((node, parent))
        else:
            if isinstance(curse_node, CurseDecNode):
                if len(curse_node.parameters) != len(node.arguments):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected {len(curse_node.parameters)} arguments, got {len(node.arguments)}"))
                else:
                    for param, arg in zip(curse_node.parameters, node.arguments):
                        param_type = param.datatype  # Use param.datatype directly
                        arg_type = self.infer_type(arg)
                        if param_type != arg_type:
                            self.errors.append(SemanticError(arg.pos_start, arg.pos_end, f"Type mismatch: Expected '{param_type}', got '{arg_type}'"))
            else:
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"'{node.name}' is not a curse"))
        self.visit_children(node)
        print(f"Exiting CurseCallNode")

    def visit_StringConcatNode(self, node, parent):
        print(f"Visiting StringConcatNode")
        self.visit_children(node)
        print(f"Exiting StringConcatNode")

    def visit_InvokeNode(self, node, parent):
        print(f"Visiting InvokeNode")
        self.visit_children(node)
        print(f"Exiting InvokeNode")

    def visit_CaptureNode(self, node, parent):
        print(f"Visiting CaptureNode with name: {node.name}")
        self.visit_children(node)
        print(f"Exiting CaptureNode")

    def visit_CleaveNode(self, node, parent):
        print(f"Visiting CleaveNode with name: {node.name}")
        self.visit_children(node)
        print(f"Exiting CleaveNode")

    def visit_DismantleNode(self, node, parent):
        print(f"Visiting DismantleNode with name: {node.name}")
        self.visit_children(node)
        print(f"Exiting DismantleNode")

    def visit_LenNode(self, node, parent):
        print(f"Visiting LenNode with name: {node.name}")
        self.visit_children(node)
        print(f"Exiting LenNode")

    def visit_RecallNode(self, node, parent):
        print(f"Visiting RecallNode")
        grandparent = parent.parent if parent else None
        print(f"Grandparent node: {type(grandparent).__name__}")
        if isinstance(grandparent, CurseDecNode) and grandparent.datatype != None:
            if not node.value:
                self.errors.append(SemanticError(node.pos_start, node.pos_end, "Recall statement must return a value in a non-void curse"))
            else:
                if isinstance(node.value, CurseCallNode):
                    curse_node = self.symbol_table.get(node.value.name)
                    if curse_node is None:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undefined curse '{node.value.name}'"))
                    else:
                        curse_return_type = curse_node.datatype
                        if curse_return_type is None:
                            curse_return_type = 'void'
                        if grandparent.datatype != curse_return_type:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch: Expected '{grandparent.datatype}', got '{curse_return_type}'"))
                elif isinstance(node.value, ClanAccessNode):
                    symbol_type = self.symbol_table.get_type(node.value.name)
                    if symbol_type is None:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undefined clan '{node.value.name}'"))
                    else:
                        if grandparent.datatype != symbol_type:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch: Expected '{grandparent.datatype}', got '{symbol_type}'"))
                elif isinstance(node.value, IdNode):   
                    symbol_type = self.symbol_table.get_type(node.value.name)
                    if symbol_type is None:
                        self.unresolved_cases.append((node, parent))
                    else:
                        if grandparent.datatype != symbol_type:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch: Expected '{grandparent.datatype}', got '{symbol_type}'"))
                elif isinstance(node.value, BinOpNode):
                    self.unresolved_cases.append((node.value, node))
                else:
                    return_type = self.infer_type(node.value)
                    if return_type != grandparent.datatype:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch: Expected '{grandparent.datatype}', got '{return_type}'"))
        elif isinstance(grandparent, CurseDecNode) and grandparent.datatype == None:
            if node.value:
                self.errors.append(SemanticError(node.pos_start, node.pos_end, "Recall statement cannot return a value in a void curse"))
        elif isinstance(grandparent, CurseDomainNode):
            if node.value:
                self.errors.append(SemanticError(node.pos_start, node.pos_end, "Recall statement cannot return a value in the curse domain"))
        self.visit_children(node)
        print(f"Exiting RecallNode")

    def visit_DismissNode(self, node, parent):
        print(f"Visiting DismissNode")
        if not isinstance(parent, (SustainNode, PerformSustainNode, CycleNode)):
            self.errors.append(SemanticError(node.pos_start, node.pos_end, "Dismiss statement not within a loop"))
        self.visit_children(node)
        print(f"Exiting DismissNode")

    def visit_HopNode(self, node, parent):
        print(f"Visiting HopNode")
        if not isinstance(parent, (SustainNode, PerformSustainNode, CycleNode)):
            self.errors.append(SemanticError(node.pos_start, node.pos_end, "Dismiss statement not within a loop"))
        self.visit_children(node)
        print(f"Exiting HopNode")

    def visit_VowNode(self, node, parent):
        print(f"Visiting VowNode")
        condition_type = self.infer_type(node.condition)
        if condition_type != 'bool':
            self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, f"Condition must be a boolean expression, got '{condition_type}'"))
        self.visit_children(node)
        print(f"Exiting VowNode")

    def visit_ElseVow(self, node, parent):
        print(f"Visiting ElseVow")
        condition_type = self.infer_type(node.condition)
        if condition_type != 'bool':
            self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, f"Condition must be a boolean expression, got '{condition_type}'"))
        self.visit_children(node)
        print(f"Exiting ElseVow")

    def visit_ElseNode(self, node, parent):
        print(f"Visiting ElseNode")
        self.visit_children(node)
        print(f"Exiting ElseNode")

    def visit_BoogieNode(self, node, parent):
        print(f"Visiting BoogieNode")
        self.visit_children(node)
        print(f"Exiting BoogieNode")

    def visit_WoogieTrueNode(self, node, parent):
        print(f"Visiting WoogieTrueNode")
        self.visit_children(node)
        print(f"Exiting WoogieTrueNode")

    def visit_WoogieNode(self, node, parent):
        print(f"Visiting WoogieNode")
        self.visit_children(node)
        print(f"Exiting WoogieNode")

    def visit_DefaultCaseNode(self, node, parent):
        print(f"Visiting DefaultCaseNode")
        self.visit_children(node)
        print(f"Exiting DefaultCaseNode")

    def visit_SustainNode(self, node, parent):
        print(f"Visiting SustainNode")
        self.visit_children(node)
        print(f"Exiting SustainNode")

    def visit_PerformSustainNode(self, node, parent):
        print(f"Visiting PerformSustainNode")
        self.visit_children(node)
        print(f"Exiting PerformSustainNode")

    def visit_CycleNode(self, node, parent):
        print(f"Visiting CycleNode")
        self.visit_children(node)
        print(f"Exiting CycleNode")

    def visit_CycleConditionNode(self, node, parent):
        print(f"Visiting CycleConditionNode")
        self.visit_children(node)
        print(f"Exiting CycleConditionNode")

    def resolve_unresolved(self):
        print("Resolving unresolved references...")
        print(f"Unresolved cases: {self.unresolved_cases}")

        for node, parent in self.unresolved_cases:
            if isinstance(node, VarAssignNode):
                symbol_type = self.symbol_table.get_type(node.name)
                if symbol_type is None:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared variable '{node.name}'"))
                else:
                    if isinstance(node.value, CurseCallNode):
                        curse_node = self.symbol_table.get(node.value.name)
                        if curse_node is None:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undefined curse '{node.value.name}'"))
                            break
                        else:
                            curse_return_type = curse_node.datatype
                            if curse_return_type is None:
                                curse_return_type = 'void'
                            if symbol_type != curse_return_type:
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch: Expected '{symbol_type}' curse, got '{curse_return_type}' curse"))
                    else:
                        value_type = self.infer_type(node.value)
                        if symbol_type != value_type:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch: Expected '{symbol_type}', got '{value_type}'"))

            elif isinstance(node, CurseCallNode):
                curse_node = self.symbol_table.get(node.name)

                if isinstance(curse_node, VarDecNode):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"'{node.name}' is not a curse"))
                elif isinstance(parent, VarAssignNode):
                    if isinstance(curse_node, CurseDecNode):
                        if parent.datatype != curse_node.datatype:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch: Expected '{parent.datatype}' curse, got '{curse_node.datatype}' curse"))  

                if curse_node is None:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undefined curse '{node.name}'"))
                    break
                else:
                    if isinstance(curse_node, CurseDecNode):
                        if len(curse_node.parameters) != len(node.arguments):
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected {len(curse_node.parameters)} arguments, got {len(node.arguments)}"))
                        else:
                            for param, arg in zip(curse_node.parameters, node.arguments):
                                param_type = param.datatype
                                arg_type = self.infer_type(arg)
                                if param_type != arg_type:
                                    self.errors.append(SemanticError(arg.pos_start, arg.pos_end, f"Type mismatch: Expected '{param_type}' type argument, got '{arg_type}'"))
                            if isinstance(parent, VarAssignNode):
                                parent_datatype = self.symbol_table.get_type(parent.name)
                                if parent_datatype != curse_node.datatype:
                                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch: Expected '{parent_datatype}' curse, got '{curse_node.datatype}' curse"))
            elif isinstance(node, InvokeNode):
                if isinstance(node.value, IdNode):
                    symbol = self.symbol_table.get(node.value.name)
                    if symbol is None:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared variable '{node.value.name}'"))
            
            elif isinstance(node, IdNode) and isinstance(parent, RecallNode):
                if isinstance(node, IdNode):
                    symbol = self.symbol_table.get(node.name)
                    if symbol is None:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared variable '{node.value.name}'"))
                    else:
                        parent_function = parent
                        while parent_function and not isinstance(parent_function, CurseDecNode):
                            parent_function = parent_function.parent
                        if parent_function and parent_function.datatype != symbol.datatype:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch: Expected '{parent_function.datatype}', got '{symbol.datatype}'"))

            elif isinstance(node, IdNode):
                symbol = self.symbol_table.get(node.name)
                symbol_type = self.symbol_table.get_type(node.name)
                if symbol is None:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared variable '{node.name}'"))
                if isinstance(parent, StringConcatNode):
                    if symbol_type == 'bool':
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot concatenate string with boolean"))
                    elif symbol_type == 'null':
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot concatenate string with null"))
            elif isinstance(node, BinOpNode):
                binop_type = self.infer_type(node)
                binop_parent = node.parent
                if isinstance(binop_parent, (VarDecNode)):
                    if binop_type != binop_parent.datatype:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch: Expected '{binop_parent.datatype}', got '{binop_type}'"))
                elif isinstance(binop_parent, (RecallNode)):
                    parent_function = binop_parent.parent
                    while parent_function and not isinstance(parent_function, CurseDecNode):
                        parent_function = parent_function.parent
                    if parent_function and parent_function.datatype != binop_type:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch: Expected '{parent_function.datatype}', got '{binop_type}'"))
                    else: print(f"Unhandled Error: {parent.function.datatype} and {binop_type}")
                elif isinstance(binop_parent, (CycleConditionNode)):
                    if binop_type != 'bool':
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Condition must be a boolean expression, got '{binop_type}'"))
                elif isinstance(binop_parent, (VowNode, ElseVow)):
                    if binop_type != 'bool':
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Condition must be a boolean expression, got '{binop_type}'"))
                elif isinstance(binop_parent, (WoogieTrueNode)):
                    if binop_type != 'bool':
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Condition must be a boolean expression, got '{binop_type}'"))
        print(f"Unresolved cases after resolution: {self.unresolved_cases}\n")

    def infer_type(self, node):
        if isinstance(node, NumNode):
            return 'int' if isinstance(node.value, int) else 'float'
        elif isinstance(node, StringNode):
            return 'string'
        elif isinstance(node, BoolNode):
            return 'bool'
        elif isinstance(node, NullNode):
            return 'null'
        elif isinstance(node, IdNode):
            return self.symbol_table.get_type(node.name)
        elif isinstance(node, BinOpNode):
            left = node.left
            right = node.right
            left_type = self.infer_type(left)
            right_type = self.infer_type(right)
            if left_type == right_type:
                return left_type
            else:
                if left_type == 'bool' and right_type == 'bool':
                    return 'bool'
                elif left_type == 'int' and right_type == 'bool':
                    return 'int'
                elif left_type == 'bool' and right_type == 'int':
                    return 'int'
                elif left_type == 'float' and right_type == 'bool':
                    return 'float'
                elif left_type == 'bool' and right_type == 'float':
                    return 'float'
                elif left_type == 'float' or right_type == 'float':
                    return 'float'
                elif left_type == 'int' or right_type == 'int':
                    return 'int'
                elif left_type == 'string' or right_type == 'string':
                    return 'string'
                else:
                    return 'unknown'
        elif isinstance(node, UnaryOpNode):
            return self.infer_type(node.expr)
        elif isinstance(node, ClanAccessNode):
            return self.symbol_table.get_type(node.name)
        elif isinstance(node, CurseCallNode):
            curse_node = self.symbol_table.get(node.name)
            if isinstance(curse_node, CurseDecNode):
                return curse_node.datatype
            return 'unknown'
        else:
            return 'unknown'

###################
# Symbol Table Class
###################

class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # Start with a global scope

    def push(self):
        print(f"Push Success... New Symbol Stack: {self.scopes}")
        self.scopes.append({})  # Enter a new scope

    def pop(self):
        print(f"Pop Success... New Symbol Stack: {self.scopes}")
        self.scopes.pop()  # Exit the current scope

    def get(self, name):
        # Search from innermost to outermost scope
        for scope in reversed(self.scopes):
            if name in scope:
                print(f"Found name '{name}' in scope {scope}!")
                return scope[name]  # Return the actual object stored
        return None
    
    def get_local(self, name):
        # Search only in the innermost scope
        if name in self.scopes[-1]:
            return self.scopes[-1][name]
        else: 
            print(f"Id '{name}' not found in the local scope")
            return None
    
    def get_type(self, name):
        # Search from innermost to outermost scope
        for scope in reversed(self.scopes):
            if name in scope:
                print(f"Found name type '{name}' in scope {scope}!")
                return scope[name].datatype if hasattr(scope[name], 'datatype') else scope[name]
        print(f"'{name}' not found in any scope, get_type returns None")
        return None

    def set(self, name, value):
        # Set in the current (innermost) scope
        self.scopes[-1][name] = value
        print(f"Id '{name}' not found in global scope, \nAdding {name} to local scope {self.scopes[-1]}...\nAppend Success... New Symbol Stack: {self.scopes}")

###################
# Parser Class
###################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.advance()
        self.semantic_errors = []
        self.symbol_table = SymbolTable()

    def advance(self):
        while True:
            self.token_idx += 1
            if self.token_idx < len(self.tokens):
                self.current_token = self.tokens[self.token_idx]
                if self.current_token.type not in ['\n', '\t', ' ', '\\n', '\\t', 'space']:
                    break
            else:
                self.current_token = None
                break
        return self.current_token
    
    def reset(self):
        self.token_idx = -1
        self.advance()

    def peek(self):
        current_idx = self.token_idx
        while True:
            current_idx += 1
            if current_idx < len(self.tokens):
                next_token = self.tokens[current_idx]
                if next_token.type not in ['\n', '\t', ' ', '\\n', '\\t', 'space']:
                    return next_token
            else:
                return None

###################
# AST Builder
###################

    def build_ast(self):
        errors = []
        self.reset()
        root = ASTNode("Program")
        while self.current_token is not None and self.current_token.type != 'EOF':
            if self.current_token is not None and self.current_token.type in ['int', 'float', 'string', 'bool', 'curse', 'restrict']:
                declaration, error = self.parseDeclaration()
                if declaration:
                    if isinstance(declaration, list):
                        for decl in declaration:
                            root.add_child(decl)
                    else:
                        root.add_child(declaration)
                if error:
                    errors.append(error)
            elif self.current_token is not None and self.current_token.type == 'id':
                assignment, error = self.parseIdCall()
                if assignment:
                    root.add_child(assignment)
                if error:
                    errors.append(error)
            else: 
                self.advance()
        return root, errors

    def parseFactor(self):
        tok = self.current_token

        if tok.type in ('int_literal', 'float_literal'):
            self.advance()
            return NumNode(tok.value, tok.pos_start, tok.pos_end), None
        elif tok.type == 'string_literal':
            self.advance()
            return StringNode(tok.value, tok.pos_start, tok.pos_end), None
        elif tok.type == 'bool_literal':
            self.advance()
            return BoolNode(tok.value, tok.pos_start, tok.pos_end), None
        elif tok.type == 'null_literal':
            self.advance()
            return NullNode(tok.value, tok.pos_start, tok.pos_end), None
        elif tok.type == 'id' and self.peek().type == '[':
            name = tok.value
            pos_start = tok.pos_start
            self.advance()
            self.advance()
            index, error = self.parseExpr()
            if error: return None, error
            if self.current_token.type == ']':
                self.advance()
                return ClanAccessNode(name, index, pos_start, self.current_token.pos_end), None
            else:
                return None, SemanticError(tok.pos_start, tok.pos_end, "Expected: ']'")
        elif tok.type == 'id':
            pos_start = tok.pos_start
            pos_end = tok.pos_end
            self.advance()
            if self.current_token.type in ('++', '--'):
                op = self.current_token
                self.advance()
                return UnaryOpNode(op, IdNode(tok.value, tok.pos_start, tok.pos_end), post=True, pos_start=pos_start, pos_end=self.current_token.pos_end), None
            return IdNode(tok.value, pos_start, pos_end), None
        elif tok.type == '(':
            pos_start = tok.pos_start
            self.advance()
            expr, error = self.parseExpr()
            if error: return None, error
            if self.current_token.type == ')':
                self.advance()
                return expr, None
            else:
                return None, SemanticError(tok.pos_start, tok.pos_end, "Expected: ')'")
        elif tok.type in ('++', '--'):
            op = tok
            self.advance()
            factor, error = self.parseFactor()
            if error: return None, error
            return UnaryOpNode(op, factor, pre=True, pos_start=op.pos_start, pos_end=factor.pos_end), None
        elif tok.type == '!':
            op = tok
            self.advance()
            factor, error = self.parseFactor()
            return UnaryOpNode(op, factor, pre=True, pos_start=op.pos_start, pos_end=factor.pos_end), None
        else:
            return None, SemanticError(tok.pos_start, tok.pos_end, "Expected: int, float, bool, null, identifier, or '('")

    def parseExpr(self):
        return self.parseLogExpr()

    def parseLogExpr(self):
        return self.parseBinOp(self.parseRelExpr, ['&&', '||'], LogOpNode)

    def parseRelExpr(self):
        return self.parseBinOp(self.parseArithExpr, ['<', '>', '<=', '>=', '==', '!='], RelOpNode)

    def parseArithExpr(self):
        return self.parseBinOp(self.parseTerm, ['+', '-'], BinOpNode)

    def parseTerm(self):
        return self.parseBinOp(self.parseExponent, ['*', '/', '%'], BinOpNode)

    def parseExponent(self):
        pos_start = self.current_token.pos_start
        left, error = self.parseFactor()
        if error: return None, error
        while self.current_token.type == '**':
            op = self.current_token
            self.advance()
            right, error = self.parseFactor()
            if error: return None, error
            left = ExponentNode(left, right, pos_start, self.current_token.pos_end)
        return left, None

    def parseBinOp(self, func, ops, node_class):
        pos_start = self.current_token.pos_start
        left, error = func()
        if error: return None, error
        while self.current_token.type in ops:
            op = self.current_token
            self.advance()
            right, error = func()
            if error: return None, error
            left = node_class(left, op, right, pos_start, self.current_token.pos_end)
        return left, None
    
    def parseIdCall(self):
        if self.current_token.type != 'id':
            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: identifier")
        name = self.current_token.value
        pos_start = self.current_token.pos_start
        self.advance()
        
        if self.current_token.type not in ['=', '+=', '-=', '*=', '/=', '%=', '++', '--', '(', '[', ',', ';']:
            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '=', '+=', '-=', '*=', '/=', '%=', '++', '--', '(', '[', ';'")
        
        if self.current_token.type in ['=', '+=', '-=', '*=', '/=', '%=']:
            op = self.current_token.type
            self.advance()
            if self.current_token.type not in ['{', '(', '++', '--', '!', 'id', 'cleave', 'len', 'dismantle', 'string_literal', 'int_literal', 'float_literal', 'bool_literal', 'null_literal']:
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '{{', '(', '++', '--', '!', 'id', 'cleave', 'len', 'dismantle', 'string_literal', 'int_literal', 'float_literal', 'bool_literal', 'null_literal'")

            if self.current_token.type == '{': # check later for previous node type
                self.advance()
                values = []
                values_pos_start = self.current_token.pos_start
                
                if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(', '{']:
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: int, float, string, identifier, or '('")
                
                if self.current_token.type == '{': # found two '{', parse two dimensional clan literal
                    self.advance()

                    while self.current_token.type != '}':
                        if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: int, float, string, identifier, or '('")
                        new_val, error = self.parseExpr()
                        if error: return None, error
                        values.append(new_val)
                        if self.current_token.type not in [',', '}']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ',' or closing brace")
                        if self.current_token.type == ',':
                            self.advance() 
                    self.advance() # move past the closing brace '}'
                    if self.current_token.type != ',':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ','")
                    self.advance()
                    if self.current_token.type != '{':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: opening brace")
                    self.advance()
                    while self.current_token.type != '}':
                        if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: int, float, string, identifier, or '('")
                        new_val, error = self.parseExpr()
                        if error: return None, error
                        values.append(new_val)
                        if self.current_token.type not in [',', '}']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ',' or closing brace")
                        if self.current_token.type == ',':
                            self.advance()
                    self.advance() # move past the closing brace '}'
                else:           
                    while self.current_token.type != '}':
                        if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: int, float, string, identifier, or '('")
                        new_val, error = self.parseExpr()
                        values.append(new_val)
                        if self.current_token.type not in ['}', ',']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '}}' or ','")
                        if self.current_token.type == ',':
                            self.advance()
                self.advance()
                pos_end = self.current_token.pos_end
                return ClanAssignNode(name, values, pos_start, pos_end), None
            
            elif self.current_token.type == 'id' and self.peek().type == '(':
                value, error = self.parseIdCall()
                if error: return None, error
                pos_end = self.current_token.pos_end
                return VarAssignNode(name, value, pos_start, pos_end), None
            elif self.current_token.type == 'id' and self.peek().type == '[':
                clan_id = self.current_token.value
                self.advance()
                self.advance() # self advanced two times to reach the actual index value
                index, error = self.parseExpr()
                index_pos_start = self.current_token.pos_start
                if error: return None, error
                index_node = ClanIndexNode(index, index_pos_start, self.current_token.pos_end)
                value = ClanAccessNode(clan_id, index_node, pos_start, self.current_token.pos_end)
                pos_end = self.current_token.pos_end
                return VarAssignNode(name, value, pos_start, pos_end), None
            elif self.current_token.type == 'cleave':
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    cleave_id = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end) # check node types after advancing
                    self.advance() 
                    if self.current_token.type == ',':
                        self.advance()
                        index1, error = self.parseExpr()
                        if error: return None, error
                        if self.current_token.type == ',':
                            self.advance()
                            index2, error = self.parseExpr()
                            if error: return None, error
                            if self.current_token.type == ')':
                                self.advance()
                                pos_end = self.current_token.pos_end
                                return VarAssignNode(name, CleaveNode(cleave_id, index1, index2, pos_start, pos_end), pos_start, pos_end), None
            elif self.current_token.type == 'dismantle':
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    dismantle_id = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end) # check node types after advancing
                    self.advance()
                    if self.current_token.type == ',':
                        self.advance()
                        delimiter = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        self.advance()
                        if self.current_token.type == ')':
                            self.advance()
                            pos_end = self.current_token.pos_end
                            return VarAssignNode(name, DismantleNode(dismantle_id, delimiter, pos_start, pos_end), pos_start, pos_end), None
            elif self.current_token.type == 'len':
                len_pos_start = self.current_token.pos_start
                self.advance()
                if self.current_token.type != '(':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                self.advance()  
                if self.current_token.type != 'id':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: identifier")
                len_id = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                self.advance()
                if self.current_token.type != ')': 
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                self.advance()
                pos_end = self.current_token.pos_end
                return VarAssignNode(name, LenNode(len_id, pos_start, pos_end), pos_start, pos_end), None
            else:
                value, error = self.parseExpr()
                if error: return None, error
                pos_end = self.current_token.pos_end
                if op == '=':
                    return VarAssignNode(name, value, pos_start, pos_end), None
                else:
                    # Transform shorthand assignment into equivalent expression
                    bin_op = op[0]  # Get the operator part of the shorthand assignment
                    left = IdNode(name, pos_start, pos_end)
                    right = value
                    bin_op_node = BinOpNode(left, type('Token', (object,), {'type': bin_op})(), right)
                    return VarAssignNode(name, bin_op_node, pos_start, pos_end), None
        elif self.current_token.type == '[':
            self.advance()
            index_pos_start = self.current_token.pos_start
            index, error = self.parseExpr()
            if error: return None, error
            index_node = ClanIndexNode(index, index_pos_start, self.current_token.pos_end)
            if self.current_token.type == ']':
                self.advance()
                if self.current_token.type == '=':
                    self.advance()
                    if self.current_token.type == '{':
                        self.advance()
                        values = []
                        while self.current_token.type != '}':
                            new_val, error = self.parseExpr()
                            if error: return None, error
                            values.append(new_val)
                            if self.current_token.type == ',':
                                self.advance()
                        pos_end = self.current_token.pos_end
                        return ClanIndexAssignNode(name, index_node, values, pos_start, pos_end), None
        elif self.current_token.type == '(':
            self.advance()
            args = []
            while self.current_token.type != ')':
                if self.current_token.type == 'string_literal':
                    args.append(StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end))
                    self.advance()
                elif self.current_token.type == 'id':
                    value, error = self.parseIdCall()
                    args.append(value)
                else:
                    new_arg, error = self.parseExpr()
                    if error: return None, error
                    args.append(new_arg)
                if self.current_token.type == ',':
                    self.advance()
            self.advance()
            pos_end = self.current_token.pos_end
            return CurseCallNode(name, args, pos_start, pos_end), None
        elif self.current_token.type == ',': # parse for multi declaration, this one's value is 0
            self.advance()
            pos_end = self.current_token.pos_end
            return VarAssignNode(name, NumNode(0, pos_start, pos_end), pos_start, pos_end), None
        elif self.current_token.type == '++' or self.current_token.type == '--':
            op = self.current_token
            self.advance()
            pos_end = self.current_token.pos_end
            return UnaryOpNode(op, IdNode(name, pos_start, pos_end), post=True, pos_start=pos_start, pos_end=pos_end), None
        elif self.current_token.type == ';':
            self.advance()
            return IdNode(name, pos_start, self.current_token.pos_end), None
        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: 'id'")

    def parseDeclaration(self):
        if self.current_token.type in ['int', 'float', 'string', 'bool']:
            datatype = self.current_token.type
            pos_start = self.current_token.pos_start
            self.advance()

            if self.current_token.type not in ['id', 'curse']:
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: identifier or curse")
                
            if self.current_token.type == 'id':
                name = self.current_token.value
                self.advance()

                if self.current_token.type not in ['=', '[', '[...]', ';', ',']:
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '=', '[', '[...]', ';', ',', ';'")

                if self.current_token.type == '=':
                    self.advance()
                    if self.current_token.type == 'id' and self.peek().type in ['++', '--', '(']:
                        value, error = self.parseIdCall()
                        if error: return None, error
                        if self.peek() == ',':
                            declarations = [VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end)]
                            while self.current_token.type == ',':
                                self.advance()
                                if self.current_token.type != 'id':
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: identifier")
                                name = self.current_token.value
                                self.advance()
                                if self.current_token.type == '=':
                                    self.advance()
                                    value, error = self.parseExpr()
                                    if error: return None, error
                                    declarations.append(VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end))
                                else:
                                    declarations.append(VarDecNode(None, datatype, name, 0, pos_start, self.current_token.pos_end))
                            return declarations, None
                        return VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end), None
                    elif self.current_token.type == 'id' and self.peek().type in ['+', '-', '/', '%', '*', '**']:
                        value, error = self.parseExpr()
                        if error: return None, error
                        if self.peek() == ',':
                            declarations = [VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end)]
                            while self.current_token.type == ',':
                                self.advance()
                                if self.current_token.type != 'id':
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: identifier")
                                name = self.current_token.value
                                self.advance()
                                if self.current_token.type == '=':
                                    self.advance()
                                    value, error = self.parseExpr()
                                    if error: return None, error
                                    declarations.append(VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end))
                                else:
                                    declarations.append(VarDecNode(None, datatype, name, 0, pos_start, self.current_token.pos_end))
                            return declarations, None
                        return VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end), None
                    elif self.current_token.type == 'id' and self.peek().type == '[':
                        clan_id = self.current_token.value
                        pos_start = self.current_token.pos_start
                        self.advance()
                        self.advance()
                        if self.current_token.type not in ['int_literal', 'float_literal', 'id']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: int, float, or identifier")
                        index, error = self.parseExpr()
                        if error: return None, error
                        index_node = ClanIndexNode(index, self.current_token.pos_start, self.current_token.pos_end)
                        value = ClanAccessNode(clan_id, index_node, pos_start, self.current_token.pos_end)
                        if self.peek() == ',':
                            declarations = [VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end)]
                            while self.current_token.type == ',':
                                self.advance()
                                if self.current_token.type != 'id':
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: identifier")
                                name = self.current_token.value
                                self.advance()
                                if self.current_token.type == '=':
                                    self.advance()
                                    value, error = self.parseExpr()
                                    if error: return None, error
                                    declarations.append(VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end))
                                else:
                                    declarations.append(VarDecNode(None, datatype, name, 0, pos_start, self.current_token.pos_end))
                        return VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end), None
                    elif self.current_token.type == 'id':
                        value = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        self.advance()
                        if self.current_token.type == ',':
                            declarations = [VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end)]
                            while self.current_token.type == ',':
                                self.advance()
                                if self.current_token.type != 'id':
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: identifier")
                                name = self.current_token.value
                                self.advance()
                                if self.current_token.type == '=':
                                    self.advance()
                                    value, error = self.parseExpr()
                                    if error: return None, error
                                    declarations.append(VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end))
                                else:
                                    declarations.append(VarDecNode(None, datatype, name, 0, pos_start, self.current_token.pos_end))
                            return declarations, None
                        return VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end), None
                    elif self.current_token.type == 'cleave':
                        self.advance()
                        if self.current_token.type != '(':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                        else:
                            self.advance()
                            if self.current_token.type not in ['string_literal', 'id']:
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: string or identifier")

                            if self.current_token.type == 'string_literal':
                                cleave_id = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            
                            if self.current_token.type == 'id': 
                                cleave_id = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end) 
                            
                            self.advance()
                            if self.current_token.type != ',':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Missing Parameter")
                            
                            self.advance()
                            if self.current_token.type not in ['int_literal', 'float_literal', 'id']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: int, float, or identifier")
                            index1, error = self.parseExpr()
                            if error: return None, error

                            if self.current_token.type != ',':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Missing Parameter")
            
                            self.advance()
                            if self.current_token.type not in ['int_literal', 'float_literal', 'id']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: int, float, or identifier")
                            index2, error = self.parseExpr()
                            if error: return None, error

                            if self.current_token.type != ')':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                            
                            self.advance()
                            return VarDecNode(None, datatype, name, CleaveNode(cleave_id, index1, index2, pos_start, self.current_token.pos_end), pos_start, self.current_token.pos_end), None
                    elif self.current_token.type == 'dismantle':
                        self.advance()
                        if self.current_token.type != '(':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                        else:
                            self.advance()
                            if self.current_token.type not in ['string_literal', 'id']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: string or identifier")
                            if self.current_token.type == 'string_literal':
                                dismantle_id = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            if self.current_token.type == 'id':
                                dismantle_id = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            self.advance()
                            if self.current_token.type != ',':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Missing Parameter")
                            self.advance()
                            if self.current_token.type != 'string_literal':
                                return None, SemanticError(self.current_token.pos_start, self.current_token.pos_end, f"Expected: string type parameter")
                            delimiter = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            self.advance()
                            if self.current_token.type != ')':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                            self.advance()
                            return VarDecNode(None, datatype, name, DismantleNode(dismantle_id, delimiter, pos_start, self.current_token.pos_end), pos_start, self.current_token.pos_end), None
                    elif self.current_token.type == 'len':
                        self.advance()
                        if self.current_token.type != '(':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                        self.advance()
                        if self.current_token.type != 'id':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: identifier")
                        len_id = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        self.advance()
                        if self.current_token.type != ')':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                        self.advance()
                        return VarDecNode(None, datatype, name, LenNode(len_id, pos_start, self.current_token.pos_end), pos_start, self.current_token.pos_end), None
                    else:
                        if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'bool_literal', 'null_literal', 'id', '(', '[']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: int, float, string, boolean, identifier, or '('")
                        value, error = self.parseExpr()
                        if error: return None, error
                        if self.current_token.type == ',': # for parsing multi variable declaration
                            declarations = [VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end)]
                            while self.current_token.type == ',':
                                self.advance()
                                if self.current_token.type != 'id':
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: identifier")
                                name = self.current_token.value
                                self.advance()
                                if self.current_token.type == '=':
                                    self.advance()
                                    value, error = self.parseExpr()
                                    if error: return None, error
                                    declarations.append(VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end))
                                elif self.current_token.type == ';':
                                    declarations.append(VarDecNode(None, datatype, name, 0, pos_start, self.current_token.pos_end))
                                else:
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '=' or ';'")
                            return declarations, None
                        return VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end), None
                elif self.current_token.type == '[':
                    self.advance()
                    if self.current_token.type not in ['int_literal', 'float_literal', 'id', '(']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: int, float, identifier, or '('")
                    size_pos_start = self.current_token.pos_start
                    size, error = self.parseExpr()
                    if error: return None, error
                    clan_size_node1 = ClanSizeNode(size, size_pos_start, self.current_token.pos_end)
                    clan_size_node2 = None
                    if self.current_token.type != ']':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ']'")
                    self.advance()

                    if self.current_token.type not in ['=', '[']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '=', '['")

                    if self.current_token.type == '=': # Parse one dimensional clan declaration
                        initial_values = [] 
                        self.advance()
                        if self.current_token.type != '{':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: opening brace")
                        self.advance()
                        while self.current_token.type != '}':
                            if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: int, float, string, identifier, or '('")
                            new_val, error = self.parseExpr()
                            if error: return None, error
                            initial_values.append(new_val)
                            if self.current_token.type not in [',', '}']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ',' or closing brace")
                            if self.current_token.type == ',': 
                                self.advance() 
                        self.advance() # move past the closing brace '}'
                        return ClanDecNode(None, datatype, name, clan_size_node1, clan_size_node2, initial_values, None, pos_start, self.current_token.pos_end), None
                    elif self.current_token.type == '[':
                        self.advance()
                        if self.current_token.type not in ['int_literal', 'float_literal', 'id', '(']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: int, float, identifier, or '('")
                        size_pos_start = self.current_token.pos_start
                        size, error = self.parseExpr()
                        if error: return None, error
                        clan_size_node2 = ClanSizeNode(size, size_pos_start, self.current_token.pos_end)
                        if self.current_token.type != ']':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ']'")
                        self.advance()
                        initial_values1 = []
                        initial_values2 = []
                        if self.current_token.type != '=':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '='")
                        self.advance()
                        if self.current_token.type != '{':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: opening brace")
                        self.advance()
                        if self.current_token.type != '{':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: opening brace")
                        self.advance()
                        while self.current_token.type != '}':
                            if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: int, float, string, identifier, or '('")
                            new_val, error = self.parseExpr()
                            if error: return None, error
                            initial_values1.append(new_val)
                            if self.current_token.type not in [',', '}']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ',' or closing brace")
                            if self.current_token.type == ',':
                                self.advance() 
                        self.advance() # move past the closing brace '}'
                        if self.current_token.type != ',':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ','")
                        self.advance()
                        if self.current_token.type != '{':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: opening brace")
                        self.advance()
                        while self.current_token.type != '}':
                            if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: int, float, string, identifier, or '('")
                            new_val, error = self.parseExpr()
                            if error: return None, error
                            initial_values2.append(new_val)
                            if self.current_token.type not in [',', '}']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ',' or closing brace")
                            if self.current_token.type == ',':
                                self.advance()
                        self.advance() # move past the closing brace '}'
                        return ClanDecNode(None, datatype, name, clan_size_node1, clan_size_node2, initial_values1, initial_values2, pos_start, self.current_token.pos_end), None
                elif self.current_token.type == '[...]':
                    self.advance()
                    initial_values = []
                    if self.current_token.type != '=':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '='")
                    self.advance()
                    if self.current_token.type != '{':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: opening brace")
                    self.advance()
                    while self.current_token.type != '}':
                        if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: int, float, string, identifier, or '('")
                        new_val, error = self.parseExpr()
                        if error: return None, error
                        initial_values.append(new_val)
                        if self.current_token.type not in [',', '}']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ',' or closing brace")
                        if self.current_token.type == ',':
                            self.advance()
                    self.advance() # move past the closing brace
                    return ClanDecNode(None, datatype, name, None, None, initial_values, None, pos_start, self.current_token.pos_end), None
                elif self.current_token.type == ',':
                    declarations = [VarDecNode(None, datatype, name, 0, pos_start, self.current_token.pos_end)]

                    while self.current_token.type == ',':
                        pos_start = self.current_token.pos_start
                        self.advance()
                        if self.current_token.type != 'id':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: identifier")
                        name = self.current_token.value
                        self.advance()

                        if self.current_token.type not in ['=', '[', ',', ';']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '=', '[', ',', ';'")
                        

                        if self.current_token.type == '=':
                            self.advance()
                            value, error = self.parseExpr()
                            if error: return None, error
                            declarations.append(VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end))
                        elif self.current_token.type == '[':
                            self.advance()
                            index, error = self.parseExpr()
                            if error: return None, error
                            if self.current_token.type != ']':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ']'")
                            self.advance()
                            value = ClanAccessNode(name, index, pos_start, self.current_token.pos_end)
                            declarations.append(VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end))
                            self.advance()
                        elif self.current_token.type == ',':
                            declarations.append(VarDecNode(None, datatype, name, 0, pos_start, self.current_token.pos_end))
                        elif self.current_token.type == ';':
                            declarations.append(VarDecNode(None, datatype, name, 0, pos_start, self.current_token.pos_end))
                    return declarations, None
                
                elif self.current_token.type == ';':
                    return VarDecNode(None, datatype, name, 0, pos_start, self.current_token.pos_end), None
            elif self.current_token.type == 'curse':
                self.advance()
                if self.current_token.type != 'id':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: identifier")
                name = self.current_token.value
                self.advance()
                if self.current_token.type != '(':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                self.advance()
                parameters = []
                while self.current_token.type != ')':
                    pos_start = self.current_token.pos_start
                    if self.current_token.type not in ['int', 'float', 'string', 'bool']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: int, float, string, bool")
                    param_type = self.current_token.type
                    self.advance()
                    if self.current_token.type != 'id':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: identifier")
                    param_name = self.current_token.value
                    self.advance()
                    param_node = ParamNode(param_type, param_name, pos_start, self.current_token.pos_end)
                    parameters.append(param_node)
                    if self.current_token.type not in [',', ')']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ',' or ')'")
                    if self.current_token.type == ',':
                        self.advance()
                self.advance()
                if self.current_token.type != '{':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: left brace for body")
                self.advance()
                body, error = self.parseBody()
                if error: return None, error
                self.advance() # move past the closing '}'
                return CurseDecNode(datatype, name, parameters, body, pos_start, self.current_token.pos_end), None
                
        elif self.current_token.type == 'curse':
            self.advance()
            if self.current_token.type not in ['id', 'domain']:
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: identifier or domain")

            if self.current_token.type == 'id':
                pos_start = self.current_token.pos_start
                name = self.current_token.value
                self.advance()
                if self.current_token.type != '(':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: '('")
                self.advance()
                parameters = []
                while self.current_token.type != ')':
                    pos_start = self.current_token.pos_start
                    if self.current_token.type not in ['int', 'float', 'string', 'bool']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: int, float, string, bool")
                    param_type = self.current_token.type
                    self.advance()

                    if self.current_token.type != 'id':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: identifier")
                    param_name = self.current_token.value
                    self.advance()

                    param_node = ParamNode(param_type, param_name, pos_start, self.current_token.pos_end)
                    parameters.append(param_node)
                
                    if self.current_token.type not in [',', ')']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: ',' or ')'")
                    if self.current_token.type == ',':
                        self.advance()
                pos_end = self.current_token.pos_end
                self.advance() # move past the closing ')'

                if self.current_token.type != '{':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: left brace for body")
                else:
                    self.advance()
                    body, error = self.parseBody()
                    if error: return None, error
                    self.advance() # move past the closing '}'
                    return CurseDecNode(None, name, parameters, body, pos_start, pos_end), None
            elif self.current_token.type == 'domain':
                pos_start = self.current_token.pos_start
                self.advance()
                if self.current_token.type != '(':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: '('")
                self.advance()
                if self.current_token.type != ')':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: ')'")
                pos_end = self.current_token.pos_end
                self.advance()
                if self.current_token.type != '{':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: '{{'")
                self.advance()
                body, error = self.parseBody()
                if error: return None, error
                return CurseDomainNode(body, pos_start, pos_end), None
        elif self.current_token.type == 'restrict':
            pos_start = self.current_token.pos_start
            self.advance()
            if self.current_token.type not in ['int', 'float', 'string', 'bool']: 
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: int, float, string, bool")
            datatype = self.current_token.type
            self.advance()
            if self.current_token.type != 'id':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: identifier")
            name = self.current_token.value
            self.advance()
            if self.current_token.type not in ['=', ',', ';']:
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: '=', ',' or ';'")
            if self.current_token.type == '=':
                self.advance()
                value, error = self.parseExpr()
                if error: return None, error
                if self.current_token.type == ',':
                    declarations = [VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end)]
                    while self.current_token.type == ',':
                        self.advance()
                        if self.current_token.type != 'id':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: identifier")
                        name = self.current_token.value
                        self.advance()
                        if self.current_token.type == '=':
                            self.advance()
                            value, error = self.parseExpr()
                            if error: return None, error
                            declarations.append(VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end))
                        else:
                            declarations.append(VarDecNode(True, datatype, name, 0, pos_start, self.current_token.pos_end))
                    return declarations, None
                return VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end), 0
            elif self.current_token.type == ',':
                pos_start = self.current_token.pos_start
                declarations = [VarDecNode('restrict', datatype, name, 0, pos_start, self.current_token.pos_end)]
                while self.current_token.type == ',':
                    self.advance()
                    if self.current_token.type != 'id':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: identifier")
                    name = self.current_token.value
                    self.advance()
                    if self.current_token.type == '=':
                        self.advance()
                        value, error = self.parseExpr()
                        if error: return None, error
                        declarations.append(VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end))
                    else:
                        declarations.append(VarDecNode(True, datatype, name, 0, pos_start, self.current_token.pos_end))
                return declarations, None
            elif self.current_token.type == ';':
                return VarDecNode(True, datatype, name, 0, pos_start, self.current_token.pos_end), None
        else:
            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: int, float, string, bool, curse, or restrict")
    
    def parseBody(self):
        body = BodyNode()
    
        while self.current_token.type != '}':
                if self.current_token.type in ['int', 'float', 'string', 'bool', 'curse', 'restrict']:
                    declarations, error = self.parseDeclaration()
                    if error: return None, error
                    if declarations:
                        if isinstance(declarations, list):
                            for declaration in declarations:
                                body.add_child(declaration)
                        else:
                            body.add_child(declarations)
                elif self.current_token.type == 'id':
                    assignment, error = self.parseIdCall()
                    if error: return None, error
                    if assignment:
                        body.add_child(assignment)
                elif self.current_token.type == 'invoke':
                    invoke_pos_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type != '(':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                    self.advance()
                    if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(', '[']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: int, float, string, identifier, or '('")
                    value, error = self.parseInvokeArgument()
                    if error: return None, error
                    if self.current_token.type != ')':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                    self.advance() # move past the parenthesis
                    if self.current_token.type != ';':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ';'")
                    invoke_pos_end = self.current_token.pos_end
                    self.advance() # advance past the semicolon
                    body.add_child(InvokeNode(value, invoke_pos_start, invoke_pos_end))
                elif self.current_token.type == 'capture':
                    capture_pos_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type != '(':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                    self.advance()
                    if self.current_token.type != 'id':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: identifier")
                    name = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                    self.advance()
                    if self.current_token.type != ')':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                    capture_pos_end = self.current_token.pos_end
                    self.advance()
                    body.add_child(CaptureNode(name, capture_pos_start, capture_pos_end))
                elif self.current_token.type == 'dismiss':
                    pos_start, pos_end = self.current_token.pos_start, self.current_token.pos_end
                    self.advance()
                    body.add_child(DismissNode(pos_start, pos_end))
                elif self.current_token.type == 'hop':
                    pos_start, pos_end = self.current_token.pos_start, self.current_token.pos_end
                    self.advance()
                    body.add_child(HopNode(pos_start, pos_end))
                elif self.current_token.type == 'recall': # check later for all possibilities
                    self.advance()
                    pos_start = self.current_token.pos_start
                    if self.current_token.type == ';':
                        self.advance()
                        body.add_child(RecallNode(None, pos_start, self.current_token.pos_end))
                    else:
                        value, error = self.parseExpr()
                        if error: return None, error
                        body.add_child(RecallNode(value, pos_start, value.pos_end))
                elif self.current_token.type == 'vow':
                    pos_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type != '(':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                    self.advance()
                    condition, error = self.parseExpr()
                    if error: return None, error
                    if self.current_token.type != ')':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                    self.advance()
                    if self.current_token.type != '{':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '{{'")
                    self.advance()
                    body_node, error = self.parseBody()
                    if error: return None, error
                    if self.current_token.type == '}':
                        self.advance()  # advance past the closing brace '}'
                    else_vows = []
                    while self.current_token.type == 'else' and self.peek().type == 'vow':
                        self.advance()
                        self.advance()
                        if self.current_token.type != '(':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                        self.advance()
                        else_condition, error = self.parseExpr()
                        if error: return None, error
                        if self.current_token.type != ')':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                        self.advance()
                        if self.current_token.type != '{':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '{{'")
                        self.advance()
                        else_body_node, error = self.parseBody()
                        if error: return None, error
                        if self.current_token.type == '}':
                            self.advance()  # advance past the closing '}'
                        else_vows.append(ElseVow(else_condition, else_body_node))
                    if self.current_token.type == 'else':
                        self.advance()
                        if self.current_token.type == '{':
                            self.advance()
                            else_pos_start = self.current_token.pos_start
                            else_body_node, error = self.parseBody()
                            else_pos_end = self.current_token.pos_end
                            self.advance()  # Advance past the closing '}'
                            body.add_child(VowNode(condition, body_node, else_vows, ElseNode(else_body_node, else_pos_start, else_pos_end), pos_start, self.current_token.pos_end))
                    else:
                        body.add_child(VowNode(condition, body_node, else_vows, None, pos_start, self.current_token.pos_end))
                elif self.current_token.type == 'boogie':
                    boogie_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type == '(':
                        self.advance()
                        expression = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        self.advance()
                        if self.current_token.type != ')':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                        self.advance()
                        if self.current_token.type != '{':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '{{'")
                        self.advance()
                        cases = []
                        while self.current_token.type != '}':
                            if self.current_token.type == 'woogie':
                                woogie_start = self.current_token.pos_start
                                self.advance()
                                if self.current_token.type in ['int_literal', 'float_literal', 'id']:
                                    case_expr, error = self.parseExpr()
                                    if error: return None, error
                                elif self.current_token.type == 'string_literal':
                                    case_expr = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                                    self.advance()
                                elif self.current_token.type == '(':
                                    self.advance()
                                    if self.current_token.type == 'id':
                                        case_expr, error = self.parseIdCall()
                                else:
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, "Expected: int_literal, float_literal, or string_literal")
                                if self.current_token.type != ':':
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ':'")
                                self.advance()
                                case_body, errors = self.parseWoogieBody()
                                if errors: return None, errors
                                cases.append(WoogieNode(case_expr, case_body, woogie_start, self.current_token.pos_end))
                            elif self.current_token.type == 'default':
                                default_start = self.current_token.pos_start
                                self.advance()
                                if self.current_token.type != ':':
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ':'")
                                self.advance()
                                default_body, errors = self.parseWoogieBody()
                                if errors: return None, errors
                                cases.append(DefaultCaseNode(default_body, default_start, self.current_token.pos_end))
                            else: return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: 'woogie' or 'default'")
                        self.advance()
                        body.add_child(BoogieNode(expression, cases, boogie_start, self.current_token.pos_end))
                    elif self.current_token.type == '{':
                        self.advance()
                        cases = []
                        while self.current_token.type != '}':
                            if self.current_token.type == 'woogie':
                                woogie_start = self.current_token.pos_start
                                self.advance()
                                case_expr, error = self.parseExpr()
                                if error: return None, error
                                if self.current_token.type == ':':
                                    self.advance()
                                    case_body, errors = self.parseWoogieBody()
                                    if errors: return None, errors
                                    cases.append(WoogieTrueNode(case_expr, case_body, woogie_start, self.current_token.pos_end))
                            elif self.current_token.type == 'default':
                                default_start = self.current_token.pos_start
                                self.advance()
                                if self.current_token.type == ':':
                                    self.advance()
                                    default_body, errors = self.parseWoogieBody()
                                    if errors: return None, errors
                                    cases.append(DefaultCaseNode(default_body, default_start, self.current_token.pos_end))
                        self.advance()
                        body.add_child(BoogieNode(None, cases, boogie_start, self.current_token.pos_end))
                    else: return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '(' or '{{'")

                elif self.current_token.type == 'cycle':
                    cycle_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type != '(':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                    self.advance()
                    cycle_condition, error = self.parseCycleCondition()
                    if error: return None, error
                    if self.current_token.type != ')':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                    self.advance()
                    if self.current_token.type != '{':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '{{'")
                    self.advance()
                    cycle_body, error = self.parseBody()
                    self.advance() # advance past the closing brace
                    body.add_child(CycleNode(cycle_condition, cycle_body, cycle_start, self.current_token.pos_end)) 
                elif self.current_token.type == 'sustain':
                    sustain_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type != '(':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                    self.advance()
                    condition, error = self.parseExpr()
                    if error: return None, error
                    if self.current_token.type != ')':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                    self.advance()
                    if self.current_token.type != '{':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '{{'")
                    self.advance()
                    sustain_body, error = self.parseBody()
                    self.advance() # advance past the closing brace
                    body.add_child(SustainNode(condition, sustain_body, sustain_start, self.current_token.pos_end))
                elif self.current_token.type == 'perform':
                    perform_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type != '{':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '{{'")
                    self.advance()
                    perform_body, error = self.parseBody()
                    self.advance() # advance past the closing brace
                    if self.current_token.type != 'sustain':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: sustain")
                    self.advance()
                    if self.current_token.type != '(':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                    self.advance()
                    condition, error = self.parseExpr()
                    if error: return None, error
                    if self.current_token.type != ')':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                    self.advance()
                    if self.current_token.type != ';':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ';'")
                    self.advance()
                    body.add_child(PerformSustainNode(perform_body, condition, perform_start, self.current_token.pos_end))
                else:
                    self.advance()
        return body, None

    def parseCycleCondition(self):
        pos_start = self.current_token.pos_start
        cycle_errors = []
        if self.current_token.type not in ['int', 'float', 'string', 'bool', 'id']:
            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, "Expected: variable declaration or assignment")
        if self.current_token.type in ['int', 'float', 'string', 'bool']:
            init, errors = self.parseDeclaration()
            if errors:
                cycle_errors.append(errors)
        elif self.current_token.type == 'id':
            init, error = self.parseIdCall()
        else:
            raise ParseError(self.current_token.pos_start, self.current_token.pos_end, "Expected: variable declaration or assignment")
        if self.current_token.type == ';':
            self.advance()
            condition, error = self.parseExpr()
            if error: return None, error
            if self.current_token.type == ';':
                self.advance()
                iteration, error = self.parseExpr()
                if error: return None, error
                return CycleConditionNode(init, condition, iteration, pos_start, self.current_token.pos_end), None
        else:
            print(f"Encountered: {self.current_token.type}") 
            raise ParseError(self.current_token.pos_start, self.current_token.pos_end, "Expected: ';'")

    def parseWoogieBody(self):
        body_start = self.current_token.pos_start
        body = BodyNode()
        while self.current_token.type not in ['woogie', 'default', '}']:
            if self.current_token.type in ['int', 'float', 'string', 'bool', 'curse', 'restrict']:
                declaration, errors = self.parseDeclaration()
                if errors: return None, errors
                if declaration:
                    body.add_child(declaration)
            elif self.current_token.type == 'id':
                assignment, error = self.parseIdCall()
                if error: return None, error
                if assignment:
                    body.add_child(assignment)
            elif self.current_token.type == 'invoke':
                invoke_start = self.current_token.pos_start
                self.advance()
                if self.current_token.type != '(':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                self.advance()
                if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(', '[']:
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: int, float, string, identifier, or '('")
                value, error = self.parseInvokeArgument()
                if error: return None, error
                if self.current_token.type != ')':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                self.advance() # move past the closing parenthesis
                if self.current_token.type != ';':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ';'")
                self.advance() # move past the semicolon
                body.add_child(InvokeNode(value, invoke_start, self.current_token.pos_end))
            elif self.current_token.type == 'capture':
                capture_start = self.current_token.pos_start
                self.advance()
                if self.current_token.type != '(':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                self.advance()
                if self.current_token.type != 'id':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected identifier")
                name = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                self.advance()
                if self.current_token.type != ')':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                self.advance()
                body.add_child(CaptureNode(name, capture_start, self.current_token.pos_end))
            elif self.current_token.type == 'dismiss':
                pos_start, pos_end = self.current_token.pos_start, self.current_token.pos_end
                self.advance()
                body.add_child(DismissNode(pos_start, pos_end))
            elif self.current_token.type == 'hop':
                pos_start, pos_end = self.current_token.pos_start, self.current_token.pos_end
                self.advance()
                body.add_child(HopNode(pos_start, pos_end))
            elif self.current_token.type == 'recall': # check later for all possibilities
                pos_start = self.current_token.pos_start
                self.advance()
                value, error = self.parseExpr()
                if error: return None, error
                body.add_child(RecallNode(value, pos_start, self.current_token.pos_end))
            elif self.current_token.type == 'vow':
                vow_start = self.current_token.pos_start
                self.advance()
                if self.current_token.type != '(':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                self.advance()
                condition, error = self.parseExpr()
                if error: return None, error
                if self.current_token.type != ')':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                self.advance()
                if self.current_token.type != '{':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '{{'")
                self.advance()
                body_node, error = self.parseBody()
                if error: return None, error
                self.advance()  # advance past the closing brace '}'
                else_vows = []
                while self.current_token.type == 'else' and self.peek().type == 'vow':
                    self.advance()
                    self.advance()
                    if self.current_token.type != '(':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                    self.advance()
                    else_condition, error = self.parseExpr()
                    if error: return None
                    if self.current_token.type != ')':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                    self.advance()
                    if self.current_token.type != '{':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '{{'")
                    self.advance()
                    else_body_node, error = self.parseBody()
                    if error: return None, error
                    self.advance()  # Advance past the closing '}'
                    else_vows.append(ElseVow(else_condition, else_body_node))
                if self.current_token.type == 'else':
                    else_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type == '{':
                        self.advance()
                        else_body_node, error = self.parseBody()
                        self.advance()  # Advance past the closing '}'
                        body.add_child(VowNode(condition, body_node, else_vows, ElseNode(else_body_node, else_start, self.current_token.pos_end), vow_start, self.current_token.pos_end))
                else:
                    body.add_child(VowNode(condition, body_node, else_vows, None, vow_start, self.current_token.pos_end))
            else:
                self.advance()
        return body, None

    def parseInvokeArgument(self):
        if self.current_token.type == 'string_literal':
            return self.parseString()
        else:
            return self.parseExpr()

    def parseString(self):
        pos_start = self.current_token.pos_start
        left = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
        self.advance()
        while self.current_token.type == '+':
            op = self.current_token
            self.advance()
            if self.current_token.type == 'string_literal':
                right = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                self.advance()
            else:
                right, error = self.parseFactor()
                if error: return None, error
            left = StringConcatNode(left, op, right, pos_start, self.current_token.pos_end)
        return left, None

def semantic_run(tokens):
    symbol_table = SymbolTable()
    visitor = MyASTVisitor(symbol_table)
    parser = Parser(tokens)
    ast, errors = parser.build_ast()
    ast.print_tree()

    # check if there is curse domain node in the ast
    if not any(isinstance(node, CurseDomainNode) for node in ast.children):
        errors.insert(0, DomainError(parser.current_token.pos_start, parser.current_token.pos_end, "Curse domain function is not defined"))

    if ast:
        ast.print_tree()
        visitor.visit(ast)
        visitor.resolve_unresolved()  
    else:
        print("No AST built")
        return "No AST built", None
    
    if visitor.errors:
        errors.extend(visitor.errors)
        if errors:
            errors.sort(key=lambda e: e.pos_start.ln)
        return None, errors
    
    if errors:
        errors.sort(key=lambda e: e.pos_start.ln)
    
    return ast, errors