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

    def tree_to_str(self):
        spaces = ' ' * self.get_level() * 3 
        prefix = spaces + "ᴸ--" if self.parent else spaces
        result = prefix + str(self.data) + '\n'
        if self.children:
            for child in self.children:
                result += child.tree_to_str()
        return result

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
        try:
            self.value = eval(f'{left.value} {op.type} {right.value}')
        except ZeroDivisionError:
            self.value = 0
        except: 
            self.value = None

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
        return f"IdNode_Object"

class VarDecNode(ASTNode): # for variable assignments
    def __init__(self, restrict, datatype, name, value=None, pos_start=None, pos_end=None):
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
        return f"VarDecNode_Object"

class VarAssignNode(ASTNode): # for variable assignments
    def __init__(self, name, value, pos_start=None, pos_end=None):
        super().__init__("Variable Assignment", pos_start, pos_end)
        self.name = name
        self.value = value
        self.add_child(IdNode(name, pos_start, pos_end))
        self.add_child(value)

    def __repr__(self):
        return f"VarAssignNode_Object"

class ClanDecNode(ASTNode): # for arrays
    def __init__(self, restrict, datatype, name, size1=None, size2=None, initial_values=None, pos_start=None, pos_end=None):
        super().__init__("Clan Declaration", pos_start, pos_end)
        self.restrict = restrict
        self.datatype = datatype
        self.name = name
        self.size1 = size1
        self.size2 = size2
        self.initial_values = initial_values or []
        self.add_child(DatatypeNode(datatype, pos_start, pos_end))
        self.add_child(IdNode(name, pos_start, pos_end))
        if size1:
            self.add_child(size1)
        if size2:
            self.add_child(size2)
        if self.initial_values:
            if isinstance(self.initial_values, list):
                self.add_child(ClanLiteralNode(self.initial_values, pos_start, pos_end))
            else:
                self.add_child(self.initial_values)

    def __repr__(self):
        return f"ClanDecNode_Object"

class ClanLiteralNode(ASTNode): # for clan literals
    def __init__(self, values, pos_start=None, pos_end=None):
        super().__init__("Clan Literal", pos_start, pos_end)
        self.values = values
        if isinstance(self.values, list):
            for value in values:
                if isinstance(value, list):
                    self.add_child(ClanLiteralNode(value, pos_start, pos_end))
                else:
                    self.add_child(value)
        else: self.add_child(values)

    def __repr__(self):
        return f"ClanLiteralNode({', '.join(repr(value) for value in self.values)})"
    
class ClanAccessNode(ASTNode): # for array access
    def __init__(self, name, index1, index2, pos_start=None, pos_end=None):
        super().__init__("Clan Access", pos_start, pos_end)
        self.name = name
        self.index1 = index1
        self.index2 = index2
        self.add_child(IdNode(name, pos_start, pos_end))
        self.add_child(index1)
        if index2:
            self.add_child(index2)
    
    def __repr__(self):
        return f"ClanAccessNode_Object"

class ClanIndexAssignNode(ASTNode): # for array index assignments
    def __init__(self, name, index1, index2, value, pos_start=None, pos_end=None):
        super().__init__("Clan Index Assign", pos_start, pos_end)
        self.name = name
        self.index1 = index1
        self.index2 = index2
        self.value = value
        self.add_child(IdNode(name, pos_start, pos_end))
        self.add_child(index1)
        if index2:
            self.add_child(index2)
        if value:
            self.add_child(value)

    def __repr__(self):
        return f"ClanIndexAssignNode_Object"

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
    
    def __repr__(self):
        return f"CurseDecNode_Object: {self.name}"

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
    def __init__(self, arg1, index1, index2, pos_start=None, pos_end=None):
        super().__init__("Cleave Statement", pos_start, pos_end)
        self.arg1 = arg1
        self.index1 = index1
        self.index2 = index2
        self.add_child(arg1)
        self.add_child(index1)
        self.add_child(index2)

class DismantleNode(ASTNode): # for dismantle statements, dismantle(id, delimiter)
    def __init__(self, value, delimiter, pos_start=None, pos_end=None):
        super().__init__("Dismantle Statement", pos_start, pos_end)
        self.value = value
        self.delimiter = delimiter
        self.add_child(value)
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
        return f"VowNode_Object"

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
        binop_parent = parent
        binop_type = self.infer_type(node)

        if left_type == 'null' or right_type == 'null':
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot perform binary operation on Null value"))
            return

        if isinstance(binop_parent, (VarDecNode)):
            if binop_type != binop_parent.datatype:
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 15: Expected '{binop_parent.datatype}', got '{binop_type}'"))
        elif isinstance(binop_parent, (RecallNode)):
            parent_function = binop_parent.parent
            while parent_function and not isinstance(parent_function, CurseDecNode):
                parent_function = parent_function.parent
            if parent_function and parent_function.datatype != binop_type:
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 16: Expected '{parent_function.datatype}', got '{binop_type}'"))
            else: print(f"Unhandled Error: {parent.function.datatype} and {binop_type}")
        elif isinstance(binop_parent, (CycleConditionNode)):
            if binop_type != 'bool':
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"3 Condition must be a boolean expression, got '{binop_type}'"))
        elif isinstance(binop_parent, (VowNode, ElseVow)):
            if binop_type != 'bool':
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"4 Condition must be a boolean expression, got '{binop_type}'"))
        elif isinstance(binop_parent, (WoogieTrueNode)):
            if binop_type != 'bool':
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"5 Condition must be a boolean expression, got '{binop_type}'"))
        elif isinstance(binop_parent, SustainNode):
            if binop_type != 'bool':
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"6 Condition must be a boolean expression, got '{binop_type}'"))
        elif isinstance(binop_parent, PerformSustainNode):
            if binop_type != 'bool':
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"7 Condition must be a boolean expression, got '{binop_type}'"))

        if node.op == '/':
            if isinstance(node.right, NumNode) and node.right.value == 0:
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 1"))
            elif isinstance(node.right, IdNode) and isinstance(node.right.parent, BinOpNode):
                id_symbol = self.symbol_table.get(node.right.name)
                if id_symbol: # If the IdNode is a variable
                    if isinstance(id_symbol, VarDecNode) and isinstance(id_symbol.value, NumNode) and id_symbol.value.value == 0:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 2"))
            elif isinstance(node.right, ClanAccessNode):
                value = None
                clan_symbol = self.symbol_table.get(node.right.name)
                if not clan_symbol: 
                    self.unresolved_cases.append((node, parent))
                    return
                if clan_symbol and isinstance(clan_symbol, ClanDecNode):
                    size1_value = size2_value = index1_value = index2_value = None

                    if node.right.index2 and not clan_symbol.size2:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index out of bounds 3: '{node.right.name}' is a single-dimensional array"))
                        return
                    elif not node.right.index2 and clan_symbol.size2:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index out of bounds 3: '{node.right.name}' is a multi-dimensional array"))
                        return
                    
                    try:
                        size1_value = self.evaluate_node(clan_symbol.size1)
                    except: size1_value = None
                    
                    if clan_symbol.size2:
                        try:
                            size2_value = self.evaluate_node(clan_symbol.size2)
                        except: size2_value = None
                    

                    try:
                        index1_value = self.evaluate_node(node.right.index1)
                    except: index1_value = None
                    
                    if node.right.index2:
                        try: 
                            index2_value = self.evaluate_node(node.right.index2) 
                        except: index2_value = None
                    else: index2_value = None

                    print(f'Left Index: {node.right.index1}, Right Index: {node.right.index2}')
                    if index1_value is not None and size1_value is not None and (index1_value < 0 or index1_value >= self.evaluate_node(clan_symbol.size1)):
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index out of bounds 1: index1 is {index1_value}, but size1 is {self.evaluate_node(clan_symbol.size1)}"))
                    if index2_value is not None and size2_value is not None and (index2_value < 0 or index2_value >= size2_value):
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index out of bounds 2: index2 is {index2_value}, but size2 is {self.evaluate_node(clan_symbol.size2)}"))
                    if index1_value is not None and (index2_value is None or index2_value is not None):
                        if index2_value is None:
                            try: 
                                value = clan_symbol.initial_values.values[index1_value]
                            except IndexError:
                                return
                        else:
                            value = clan_symbol.initial_values[index1_value].values[index2_value] #FIXME: not pointing to the right item in array
                            print(f'Value Hey: {value}')
                        if isinstance(value, NumNode) and value.value == 0:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 3"))
                        elif isinstance(value, IdNode) and isinstance(value.parent, BinOpNode):
                            id_symbol = self.symbol_table.get(value.name)
                            if id_symbol: # If the IdNode is a variable
                                if isinstance(id_symbol, VarDecNode) and isinstance(id_symbol.value, NumNode) and id_symbol.value.value == 0:
                                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 4"))
                        elif isinstance(value, BinOpNode):
                            value = self.evaluate_node(value)
                            if value == 0:
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 5"))

        if left_type != right_type:
            if (left_type == 'string' and right_type in ['int', 'float']) or (right_type == 'string' and left_type in ['int', 'float']):
                if not isinstance(parent, (StringConcatNode, InvokeNode)):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 1.1: Cannot concatenate '{left_type}' and '{right_type}'"))

            elif left_type == 'int' and right_type == 'float':
                if isinstance(parent, BinOpNode):
                    try:
                        evaluation = eval(f"{node.left.value} {node.op} {node.right.value}")
                    except: return
                    if evaluation == 0:
                        if isinstance(parent, BinOpNode) and parent.op == '/' and parent.right == node:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 10"))
                pass
            elif left_type == 'float' and right_type == 'int':
                if isinstance(parent, BinOpNode):
                    try:
                        evaluation = eval(f"{node.left.value} {node.op} {node.right.value}")
                    except: return
                    if evaluation == 0:
                        if isinstance(parent, BinOpNode) and parent.op == '/' and parent.right == node:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 11"))
                pass
            else:
                if isinstance(node.left, IdNode) and not self.symbol_table.get(node.left.name):
                    self.unresolved_cases.append((node, parent))
                    return
                if isinstance(node.right, IdNode) and not self.symbol_table.get(node.right.name):
                    self.unresolved_cases.append((node, parent))
                    return
                if isinstance(node.left, CurseCallNode) and not self.symbol_table.get(node.left.name):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undefined function: '{node.left.name}'"))
                    return
                if isinstance(node.right, CurseCallNode) and not self.symbol_table.get(node.right.name):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undefined function: '{node.right.name}'"))
                    return
                if isinstance(node.left, IdNode) and self.symbol_table.get(node.left.name):
                    left_node = self.symbol_table.get(node.left.name)
                    if isinstance(left_node, VarDecNode):
                        if isinstance(left_node.value, NullNode):
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot perform binary operation on Null value"))
                if isinstance(node.right, IdNode) and self.symbol_table.get(node.right.name):
                    right_node = self.symbol_table.get(node.right.name)
                    if isinstance(right_node, VarDecNode):
                        if isinstance(right_node.value, NullNode):
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot perform binary operation on Null value"))
                
                if node.pos_start: self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot perform operation between '{left_type}' and '{right_type}'"))
                else: self.errors.append(SemanticError(parent.pos_start, parent.pos_end, f"Cannot perform operation between '{left_type}' and '{right_type}'"))
        else:
            if isinstance(parent, BinOpNode):
                if left_type == 'int' and right_type == 'int':
                    print("686")
                    try:
                        evaluation = eval(f"{node.left.value} {node.op} {node.right.value}")
                    except: 
                     return
                    if evaluation == 0:
                        if isinstance(parent, BinOpNode) and parent.op == '/' and parent.right == node:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 12"))
                elif left_type == 'float' and right_type == 'float':
                    try:
                        evaluation = eval(f"{node.left.value} {node.op} {node.right.value}")
                    except: return
                    if evaluation == 0:
                        if isinstance(parent, BinOpNode) and parent.op == '/' and parent.right == node:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 13"))
                elif left_type == 'bool' and right_type == 'bool':
                    try:
                        evaluation = eval(f"{node.left.value} {node.op} {node.right.value}")
                    except: return
                    if evaluation == 0:
                        if isinstance(parent, BinOpNode) and parent.op == '/' and parent.right == node:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 14"))
            if isinstance(node.left, IdNode) and self.symbol_table.get(node.left.name):
                left_node = self.symbol_table.get(node.left.name)
                if isinstance(left_node, VarDecNode):
                    if isinstance(left_node.value, NullNode):
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot perform binary operation on Null value"))
            if isinstance(node.right, IdNode) and self.symbol_table.get(node.right.name):
                right_node = self.symbol_table.get(node.right.name)
                if isinstance(right_node, VarDecNode):
                    if isinstance(right_node.value, NullNode):
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot perform binary operation on Null value"))
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
        if not self.symbol_table.get_local(node.name):
            self.symbol_table.set(node.name, node)  # Store the VarDecNode object itself
        value_type = self.infer_type(node.value)
        var_type = self.symbol_table.get_type(node.name)
        
        if not node.value:
            value_type = 'null'
        else: 
            if isinstance(node.value, CleaveNode):
                pass

        if value_type == 'null':
            pass
        else:
            if var_type != value_type:
                if isinstance(node.value, CurseCallNode):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 3.2: Expected '{var_type}' curse, got '{value_type}'"))
                else: self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 3.2: Expected '{var_type}', got '{value_type}'"))
        self.visit_children(node)
        print(f"Exiting VarDecNode")

    def visit_VarAssignNode(self, node, parent):
        print(f"Visiting VarAssignNode with name: {node.name}")
        if not self.symbol_table.get(node.name):
            self.unresolved_cases.append((node, parent))
        else:
            symbol = self.symbol_table.get(node.name)
            if symbol.restrict:
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot modify restricted variable '{node.name}'"))
                return
            value_type = self.infer_type(node.value)
            var_type = self.symbol_table.get_type(node.name)
            if value_type == 'null':
                pass
            else:
                if var_type != value_type:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 3.1: Expected '{var_type}', got '{value_type}'"))
        self.visit_children(node)
        print(f"Exiting VarAssignNode")

    def visit_ClanDecNode(self, node, parent):
        print(f"Visiting ClanDecNode with name: {node.name}")
        if self.symbol_table.get(node.name):
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Clan '{node.name}' already declared"))
        else:
            self.symbol_table.set(node.name, node)

        # Check if size1 and size2 are strictly integers
        if node.size1:
            size1_type = self.infer_type(node.size1)
            if size1_type == 'unknown':
                self.unresolved_cases.append((node.size1, node))
                return
            if size1_type != 'int':
                self.errors.append(SemanticError(node.size1.pos_start, node.size1.pos_end, f"Type mismatch 23: Expected 'int' for size1, got '{size1_type}'"))
            else:
                size1_value = self.evaluate_node(node.size1)

        if node.size2:
            size2_type = self.infer_type(node.size2)
            if size2_type == 'unknown':
                self.unresolved_cases.append((node.size2, node))
                return
            if size2_type != 'int':
                self.errors.append(SemanticError(node.size2.pos_start, node.size2.pos_end, f"Type mismatch 22: Expected 'int' for size2, got '{size2_type}'"))
            else:
                size2_value = self.evaluate_node(node.size2)

        # Handle single-dimensional array
        if node.size1 and not node.size2:
            size1_value = self.evaluate_node(node.size1)
            if size1_value is not None:
                if not isinstance(node.initial_values, ClanLiteralNode):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, "Cannot initialize multi-dimensional array with single-dimensional size"))
                elif len(node.initial_values.values) > size1_value:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Array out of index 1: size1 is {size1_value}, but got {len(node.initial_values.values)} initial values"))
                else:
                    # Fill missing values
                    while len(node.initial_values.values) < size1_value:
                        if node.datatype == 'int':
                            node.initial_values.values.append(0)
                        elif node.datatype == 'float':
                            node.initial_values.values.append(0.0)
                        elif node.datatype == 'string':
                            node.initial_values.values.append("")
                        elif node.datatype == 'bool':
                            node.initial_values.values.append(False)

        # Handle multi-dimensional array
        if node.size1 and node.size2:
            size1_value = self.evaluate_node(node.size1)
            size2_value = self.evaluate_node(node.size2)
            if size1_value is not None and size2_value is not None:
                if len(node.initial_values) > size1_value:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Array out of index 2: size1 is {size1_value}, but got {len(node.initial_values)} initial values"))
                for inner_node in node.initial_values:
                    if not isinstance(inner_node, ClanLiteralNode):
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, "Expected ClanLiteralNode for multi-dimensional array"))
                        return
                    if len(inner_node.values) > size2_value:
                        self.errors.append(SemanticError(inner_node.pos_start, inner_node.pos_end, f"Array out of index 3: size2 is {size2_value}, but got {len(inner_node.values)} initial values"))
    
                    else:
                        # Fill missing values
                        while len(inner_node.values) < size1_value:
                            if node.datatype == 'int':
                                inner_node.values.append(NumNode(0, None, None))
                            elif node.datatype == 'float':
                                inner_node.values.append(NumNode(0.0, None, None))
                            elif node.datatype == 'string':
                                inner_node.values.append(StringNode("", None, None))
                            elif node.datatype == 'bool':
                                inner_node.values.append(BoolNode(False, None, None))

        # Check initial values for type mismatches
        if isinstance(node.initial_values, ClanLiteralNode):
            for value in node.initial_values.values:
                value_type = self.infer_type(value)
                if isinstance(value, IdNode) and value_type is None:
                    self.unresolved_cases.append((value, node))
                    return
                elif isinstance(value, CurseCallNode) and value_type == 'unknown':
                    self.unresolved_cases.append((value, node))
                    return
                if node.datatype != value_type:
                    if hasattr(value, 'pos_start') and hasattr(value, 'pos_end'):
                        self.errors.append(SemanticError(value.pos_start, value.pos_end, f"Type mismatch in clan values: Expected '{node.datatype}', got '{value_type}'"))
                    else:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch in clan values: Expected '{node.datatype}', got '{value_type}'"))
        else:
            if isinstance(node.initial_values, list):
                for inner_node in node.initial_values:
                    print(f'Inner Node Type: {type(inner_node)}')
                    #if isinstance(inner_node, ClanLiteralNode):
                    for value in inner_node.values:
                        print(f'Value Type: {type(value)}')
                        value_type = self.infer_type(value)
                        if isinstance(value, IdNode) and value_type is None:
                            self.unresolved_cases.append((value, node))
                            return
                        elif isinstance(value, CurseCallNode) and value_type == 'unknown':
                            self.unresolved_cases.append((value, node))
                            return
                        if node.datatype != value_type:
                            if hasattr(value, 'pos_start') and hasattr(value, 'pos_end'):
                                self.errors.append(SemanticError(value.pos_start, value.pos_end, f"Type mismatch in clan values: Expected '{node.datatype}', got '{value_type}'"))
                            else:
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch in clan values: Expected '{node.datatype}', got '{value_type}'"))
            elif isinstance(node.initial_values, ClanLiteralNode):
                for value in node.initial_values.values:
                    value_type = self.infer_type(value)
                    if isinstance(value, IdNode) and value_type is None:
                        self.unresolved_cases.append((value, node))
                        return
                    elif isinstance(value, CurseCallNode) and value_type == 'unknown':
                        self.unresolved_cases.append((value, node))
                        return
                    if node.datatype != value_type:
                        if hasattr(value, 'pos_start') and hasattr(value, 'pos_end'):
                            self.errors.append(SemanticError(value.pos_start, value.pos_end, f"Type mismatch in clan values: Expected '{node.datatype}', got '{value_type}'"))
                        else:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch in clan values: Expected '{node.datatype}', got '{value_type}'"))
        self.visit_children(node)
        print(f"Exiting ClanDecNode")

    def evaluate_node(self, node):
        try:
            if isinstance(node, NumNode):
                return node.value
            elif isinstance(node, BinOpNode):
                left_value = self.evaluate_node(node.left)
                right_value = self.evaluate_node(node.right)
                if left_value is not None and right_value is not None:
                    try:
                     return eval(f'{left_value} {node.op} {right_value}')
                    except: return None
            return None
        except:
            return None

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
        else:
            if isinstance(symbol, ClanDecNode):
                if node.index2 and not symbol.size2:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index out of bounds 3: '{node.name}' is a single-dimensional array"))
                elif not node.index2 and symbol.size2:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index out of bounds 3: '{node.name}' is a multi-dimensional array"))

                size1_value = self.evaluate_node(symbol.size1)
                size2_value = self.evaluate_node(symbol.size2) if symbol.size2 else None

                index1_value = self.evaluate_node(node.index1)
                index2_value = self.evaluate_node(node.index2) if node.index2 else None

                if index1_value is not None and (index1_value < 0 or index1_value >= size1_value):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index out of bounds 4: index1 is {index1_value}, but size1 is {size1_value}"))

                if index2_value is not None and (index2_value < 0 or index2_value >= size2_value):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index out of bounds 5: index2 is {index2_value}, but size2 is {size2_value}"))

        self.visit_children(node)
        print(f"Exiting ClanAccessNode")

    def visit_ClanIndexAssignNode(self, node, parent):
        print(f"Visiting ClanIndexAssignNode with name: {node.name}")
        symbol = self.symbol_table.get(node.name)
        if symbol is None:
            self.unresolved_cases.append((node, parent))
        else:
            if symbol.restrict:
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot modify restricted clan '{node.name}'"))
                return
            symbol_type = self.symbol_table.get_type(node.name)
            if symbol_type is None:
                self.unresolved_cases.append((node, parent))
            else:
                if isinstance(node.value, CurseCallNode):
                    if self.infer_type(node.value) == 'unknown':
                        self.unresolved_cases.append((node.value, node))
                        return
                if node.value:
                    value_type = self.infer_type(node.value)
                    if value_type == 'unknown':
                        self.unresolved_cases.append((node.value, node))
                        return
                    if symbol_type != value_type:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch: Expected '{symbol_type}', got '{value_type}'"))

                print(f'Symbol Table: {self.symbol_table.scopes}')
                # Check for out-of-bounds errors
                if isinstance(symbol, ClanDecNode):
                    if isinstance(symbol.size1, CurseCallNode):
                        size1_value = self.evaluate_node(symbol.size1)
                        if size1_value is None:
                            self.unresolved_cases.append((symbol.size1, symbol))
                            return
                    elif isinstance(symbol.size1, NumNode):
                        size1_value = symbol.size1.value
                    elif isinstance(symbol.size1, IdNode):
                        if self.symbol_table.get_type(symbol.size1.name) == 'int':
                            size1_value = self.symbol_table.get(symbol.size1.name).value
                        else:
                            self.unresolved_cases.append((symbol.size1, symbol))
                            return
                    elif isinstance(symbol.size1, BinOpNode):
                        size1_value = self.evaluate_node(symbol.size1)
                    else:
                        size1_value = self.evaluate_node(symbol.size1)
                    
                    if symbol.size2:
                        if isinstance(symbol.size2, CurseCallNode):
                            size2_value = self.evaluate_node(symbol.size2)
                            if size2_value is None:
                                self.unresolved_cases.append((symbol.size2, symbol))
                                return
                        elif isinstance(symbol.size2, NumNode):
                            size2_value = symbol.size2.value
                        elif isinstance(symbol.size2, IdNode):
                            if self.symbol_table.get_type(symbol.size2.name) == 'int':
                                size2_value = self.symbol_table.get(symbol.size2.name).value
                            else:
                                self.unresolved_cases.append((symbol.size2, symbol))
                                return
                        elif isinstance(symbol.size2, BinOpNode):
                            size2_value = self.evaluate_node(symbol.size2)
                        else:
                            size2_value = self.evaluate_node(symbol.size2)
                    else:
                        size2_value = None

                    index1_value = self.evaluate_node(node.index1)
                    index2_value = self.evaluate_node(node.index2) if node.index2 else None

                    if index1_value is not None and (index1_value < 0 or index1_value >= size1_value):
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index out of bounds 6: index1 is {index1_value}, but size1 is {size1_value}"))

                    if index2_value is not None and (index2_value < 0 or index2_value >= size2_value):
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index out of bounds 7: index2 is {index2_value}, but size2 is {size2_value}"))

        self.visit_children(node)
        print(f"Exiting ClanIndexAssignNode")

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
        
        # Check for recall statement if datatype is not None or 'void'
        if node.datatype and node.datatype != 'void':
            recall_found = False
            children_copy = node.body.children[:]
            for child in children_copy:
                print(f'Child Type: {type(child)}')
                if isinstance(child, RecallNode):
                    recall_found = True
                    break
            if not recall_found:
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Curse '{node.name}' must have a recall statement of type '{node.datatype}'"))
        
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
        if not isinstance(parent, CycleNode):
            self.symbol_table.push()  # Enter new scope for body
        
            for child in list(node.children):
                if isinstance(child, CurseDecNode):
                    self.symbol_table.set(child.name, child)

            self.visit_children(node)
            self.symbol_table.pop()  # Exit body scope
        else:
            self.visit_children(node)
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
                            self.errors.append(SemanticError(arg.pos_start, arg.pos_end, f"Type mismatch 5: Expected '{param_type}', got '{arg_type}'"))
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
        print(f"Visiting CleaveNode: {node.arg1}")
        true_parent = parent
        while true_parent and not isinstance(true_parent, (VarDecNode, VarAssignNode, ClanIndexAssignNode, ClanDecNode, LenNode, InvokeNode)):
            true_parent = true_parent.parent
        arg1 = node.arg1
        arg2 = node.index1
        arg3 = node.index2
        arg1_type = self.infer_type(arg1)
        arg2_type = self.infer_type(arg2)
        arg3_type = self.infer_type(arg3)
        
        print(f"HELLO WORLD, arg1: {type(arg1)}")

        if isinstance(arg1, IdNode) and not self.symbol_table.get(arg1.name):
            self.unresolved_cases.append((node, parent))
        elif isinstance(arg1, StringNode):
            pass
        else:
            if isinstance(true_parent, (VarDecNode, VarAssignNode, ClanIndexAssignNode, InvokeNode)):
                arg1_symbol = self.symbol_table.get(arg1.name)
                print(f'Arg1 Symbol: {arg1_symbol}')
                if arg1_symbol is None:
                    self.unresolved_cases.append((node, parent))
                    return
                else: 
                    if isinstance(arg1_symbol, ClanDecNode):
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot assign clan to a non-clan variable"))
                    
                if not arg1_type == 'string':
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected string for cleave first argument, got '{arg1_type}'"))
                    return
                if isinstance(true_parent, VarDecNode):
                    if true_parent.datatype != 'string':
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected '{true_parent.datatype}', got '{arg1_type}'"))
                elif isinstance(true_parent, (VarAssignNode, ClanIndexAssignNode)):
                    if not self.symbol_table.get(true_parent.name):
                        self.unresolved_cases.append(node, parent)
                    else:
                        if true_parent.datatype != 'string':
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected '{true_parent.datatype}', got '{arg1_type}'"))

            elif isinstance(true_parent, ClanDecNode):
                arg1_symbol = self.symbol_table.get(arg1.name)
                if arg1_symbol is None:
                    self.unresolved_cases.append((node, parent))
                    return
                elif not isinstance(arg1_symbol, ClanDecNode):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected clan in first argument"))
                elif true_parent.datatype != arg1_symbol.datatype:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 17: Expected '{true_parent.datatype}', got '{arg1_symbol.datatype}'"))
            elif isinstance(true_parent, LenNode):
                pass
            else:
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected clan or string (2), got '{arg1_type}'"))

        if isinstance(arg2, IdNode) and not self.symbol_table.get(arg2.name):
            self.unresolved_cases.append((node, parent))
        else: 
            if not arg2_type == 'int':
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected 'int', got '{arg2_type}'"))

        if isinstance(arg3, IdNode) and not self.symbol_table.get(arg3.name):
            self.unresolved_cases.append((node, parent))
        else:
            if not arg3_type == 'int':
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected 'int', got '{arg3_type}'"))

        self.visit_children(node)
        print(f"Exiting CleaveNode")

    def visit_DismantleNode(self, node, parent):
        print(f"Visiting DismantleNode: {node.value}")

        arg1 = node.value
        arg2 = node.delimiter

        arg1_type = self.infer_type(arg1)
        arg2_type = self.infer_type(arg2)

        if isinstance(arg1, IdNode) and not self.symbol_table.get(arg1.name):
            self.unresolved_cases.append((node, parent))
        else:
            if arg1_type != 'string':
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected 'string', got '{arg1_type}'"))

        if isinstance(arg2, IdNode) and not self.symbol_table.get(arg2.name):
            self.unresolved_cases.append((node, parent))
        else:
            if arg2_type != 'string':
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected 'string', got '{arg2_type}'"))

        self.visit_children(node)
        print(f"Exiting DismantleNode")

    def visit_LenNode(self, node, parent):
        print(f"Visiting LenNode: {node.name}")
        len_value = node.name

        if isinstance(len_value, IdNode):
            symbol = self.symbol_table.get(len_value.name)
            if not symbol:
                self.unresolved_cases.append((node, parent))
            else:
                symbol_type = self.symbol_table.get_type(node.name.name)
                if isinstance(symbol, ClanDecNode):
                    pass
                elif isinstance(symbol, VarDecNode):
                    if symbol_type == 'string':
                        pass
                    else: 
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected string, got '{symbol_type}'"))
                elif isinstance(symbol, StringNode):
                    pass
                else:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected string or clan name, got '{symbol_type}'"))
        elif isinstance(len_value, StringNode):
            pass

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
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undefined curse  1 '{node.value.name}'"))
                    else:
                        curse_return_type = curse_node.datatype
                        if curse_return_type is None:
                            curse_return_type = 'void'
                        if grandparent.datatype != curse_return_type:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 6: Expected '{grandparent.datatype}', got '{curse_return_type}'"))
                elif isinstance(node.value, ClanAccessNode):
                    symbol_type = self.symbol_table.get_type(node.value.name)
                    if symbol_type is None:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undefined clan '{node.value.name}'"))
                    else:
                        if grandparent.datatype != symbol_type:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 7: Expected '{grandparent.datatype}', got '{symbol_type}'"))
                elif isinstance(node.value, IdNode):   
                    symbol_type = self.symbol_table.get_type(node.value.name)
                    if symbol_type is None:
                        self.unresolved_cases.append((node, parent))
                    else:
                        if grandparent.datatype != symbol_type:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 8: Expected '{grandparent.datatype}', got '{symbol_type}'"))
                elif isinstance(node.value, BinOpNode):
                    self.unresolved_cases.append((node.value, node))
                else:
                    return_type = self.infer_type(node.value)
                    if return_type != grandparent.datatype:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 9: Expected '{grandparent.datatype}', got '{return_type}'"))
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
        true_parent = parent
        while not isinstance(true_parent, (SustainNode, PerformSustainNode, CycleNode, WoogieNode, WoogieTrueNode)):
            if true_parent.parent:
                true_parent = true_parent.parent
            else: self.errors.append(SemanticError(node.pos_start, node.pos_end, "Dismiss statement not within a loop or boogie"))
        self.visit_children(node)
        print(f"Exiting DismissNode")

    def visit_HopNode(self, node, parent):
        print(f"Visiting HopNode")
        true_parent = parent
        while not isinstance(true_parent, (SustainNode, PerformSustainNode, CycleNode)):
            if true_parent.parent:
                true_parent = true_parent.parent
            else: self.errors.append(SemanticError(node.pos_start, node.pos_end, "Hop statement not within a loop"))
        self.visit_children(node)
        print(f"Exiting HopNode")

    def visit_VowNode(self, node, parent):
        print(f"Visiting VowNode")
        if isinstance(node.condition, BinOpNode):
            if node.condition.op not in ['<', '<=', '>', '>=', '==', '!=', '&&', '||']:
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
        elif isinstance(node.condition, IdNode):
            if not self.symbol_table.get(node.condition.name):
                self.unresolved_cases.append((node, parent))
                return
            condition_type = self.symbol_table.get_type(node.condition.name)
            if condition_type != 'bool':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must return a boolean value"))
        elif isinstance(node.condition, CurseCallNode):
            curse_node = self.symbol_table.get(node.condition.name)
            if curse_node is None:
                self.unresolved_cases.append((node, parent))
                return
            curse_return_type = curse_node.datatype
            if curse_return_type is None:
                curse_return_type = 'void'
            if curse_return_type != 'bool':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
        elif isinstance(node.condition, RelOpNode):
            pass
        elif isinstance(node.condition, LogOpNode):
            pass
        elif isinstance(node.condition, UnaryOpNode):
            if not node.condition.op.op == '!':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
            pass
        else:
            self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
        self.visit_children(node)
        print(f"Exiting VowNode")

    def visit_ElseVow(self, node, parent):
        print(f"Visiting ElseVow")
        if isinstance(node.condition, BinOpNode):
            if node.condition.op not in ['<', '<=', '>', '>=', '==', '!=', '&&', '||']:
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
        elif isinstance(node.condition, IdNode):
            if not self.symbol_table.get(node.condition.name):
                self.unresolved_cases.append((node, parent))
                return
            condition_type = self.symbol_table.get_type(node.condition.name)
            if condition_type != 'bool':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must return a boolean value"))
        elif isinstance(node.condition, CurseCallNode):
            curse_node = self.symbol_table.get(node.condition.name)
            if curse_node is None:
                self.unresolved_cases.append((node, parent))
                return
            curse_return_type = curse_node.datatype
            if curse_return_type is None:
                curse_return_type = 'void'
            if curse_return_type != 'bool':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
        elif isinstance(node.condition, RelOpNode):
            pass
        elif isinstance(node.condition, LogOpNode):
            pass
        elif isinstance(node.condition, UnaryOpNode):
            if not node.condition.op.op == '!':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
            pass
        else:
            self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
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
        if isinstance(node.condition, BinOpNode):
            if node.condition.op not in ['<', '<=', '>', '>=', '==', '!=', '&&', '||']:
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
        elif isinstance(node.condition, IdNode):
            if not self.symbol_table.get(node.condition.name):
                self.unresolved_cases.append((node, parent))
                return
            condition_type = self.symbol_table.get_type(node.condition.name)
            if condition_type != 'bool':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must return a boolean value"))
        elif isinstance(node.condition, CurseCallNode):
            curse_node = self.symbol_table.get(node.condition.name)
            if curse_node is None:
                self.unresolved_cases.append((node, parent))
                return
            curse_return_type = curse_node.datatype
            if curse_return_type is None:
                curse_return_type = 'void'
            if curse_return_type != 'bool':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
        elif isinstance(node.condition, RelOpNode):
            pass
        elif isinstance(node.condition, LogOpNode):
            pass
        elif isinstance(node.condition, UnaryOpNode):
            if not node.condition.op.op == '!':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
            pass
        else:
            self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
        self.visit_children(node)
        print(f"Exiting WoogieTrueNode")

    def visit_WoogieNode(self, node, parent):
        print(f"Visiting WoogieNode")
        if isinstance(node.condition, BinOpNode):
            if node.condition.op in ['<', '<=', '>', '>=', '==', '!=', '&&', '||']:
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Woogie cannot be a boolean expression"))
        elif isinstance(node.condition, IdNode):
            if not self.symbol_table.get(node.condition.name):
                self.unresolved_cases.append((node, parent))
                return
            condition_type = self.symbol_table.get_type(node.condition.name)
            if condition_type == 'bool':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Woogie cannot be a boolean value"))
        elif isinstance(node.condition, CurseCallNode):
            curse_node = self.symbol_table.get(node.condition.name)
            if curse_node is None:
                self.unresolved_cases.append((node, parent))
                return
            curse_return_type = curse_node.datatype
            if curse_return_type is None:
                curse_return_type = 'void'
            if curse_return_type == 'bool':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Woogie cannot be a boolean value"))
            elif curse_return_type == 'void':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Curse must return a valid value"))
        elif isinstance(node.condition, RelOpNode):
            self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Woogie cannot be a boolean expression"))
        elif isinstance(node.condition, LogOpNode):
            self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Woogie cannot be a boolean expression"))
        elif isinstance(node.condition, UnaryOpNode):
            if node.condition.op.op == '!':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Woogie cannot be a boolean expression"))
            pass
        else:
            if isinstance(node.condition, (NumNode, StringNode)):
                pass
            else: 
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Woogie must be a valid value"))
        self.visit_children(node)
        print(f"Exiting WoogieNode")

    def visit_DefaultCaseNode(self, node, parent):
        print(f"Visiting DefaultCaseNode")
        self.visit_children(node)
        print(f"Exiting DefaultCaseNode")

    def visit_SustainNode(self, node, parent):
        print(f"Visiting SustainNode")
        if isinstance(node.condition, BinOpNode):
            if node.condition.op not in ['<', '<=', '>', '>=', '==', '!=', '&&', '||']:
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
        elif isinstance(node.condition, IdNode):
            if not self.symbol_table.get(node.condition.name):
                self.unresolved_cases.append((node, parent))
                return
            condition_type = self.symbol_table.get_type(node.condition.name)
            if condition_type != 'bool':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must return a boolean value"))
        elif isinstance(node.condition, CurseCallNode):
            curse_node = self.symbol_table.get(node.condition.name)
            if curse_node is None:
                self.unresolved_cases.append((node, parent))
                return
            curse_return_type = curse_node.datatype
            if curse_return_type is None:
                curse_return_type = 'void'
            if curse_return_type != 'bool':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
        elif isinstance(node.condition, RelOpNode):
            pass
        elif isinstance(node.condition, LogOpNode):
            pass
        elif isinstance(node.condition, UnaryOpNode):
            if not node.condition.op.op == '!':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
            pass
        else:
            self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
        self.visit_children(node)
        print(f"Exiting SustainNode")

    def visit_PerformSustainNode(self, node, parent):
        print(f"Visiting PerformSustainNode")
        if isinstance(node.condition, BinOpNode):
            if node.condition.op not in ['<', '<=', '>', '>=', '==', '!=', '&&', '||']:
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
        elif isinstance(node.condition, IdNode):
            if not self.symbol_table.get(node.condition.name):
                self.unresolved_cases.append((node, parent))
                return
            condition_type = self.symbol_table.get_type(node.condition.name)
            if condition_type != 'bool':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must return a boolean value"))
        elif isinstance(node.condition, CurseCallNode):
            curse_node = self.symbol_table.get(node.condition.name)
            if curse_node is None:
                self.unresolved_cases.append((node, parent))
                return
            curse_return_type = curse_node.datatype
            if curse_return_type is None:
                curse_return_type = 'void'
            if curse_return_type != 'bool':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
        elif isinstance(node.condition, RelOpNode):
            pass
        elif isinstance(node.condition, LogOpNode):
            pass
        elif isinstance(node.condition, UnaryOpNode):
            if not node.condition.op.op == '!':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
            pass
        else:
            self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
        self.visit_children(node)
        print(f"Exiting PerformSustainNode")

    def visit_CycleNode(self, node, parent):
        print(f"Visiting CycleNode")
        self.symbol_table.push()  # Enter new scope for cycle body
        self.visit_children(node)
        self.symbol_table.pop()  # Exit cycle scope 
        print(f"Exiting CycleNode")

    def visit_CycleConditionNode(self, node, parent):
        print(f"Visiting CycleConditionNode")
        if isinstance(node.init, VarDecNode):
            if not isinstance(node.init.value, NumNode):
                self.errors.append(SemanticError(node.init.pos_start, node.init.pos_end, "Cycle initialization must be an integer"))
        elif isinstance(node.init, VarAssignNode):
            symbol_node = self.symbol_table.get(node.init.name)
            if not symbol_node:
                self.unresolved_cases.append((node.init, node))
                return

            init_type = symbol_node.datatype
            if init_type != 'int':
                self.errors.append(SemanticError(node.init.pos_start, node.init.pos_end, "Cycle initialization must be an integer"))
        else: 
            self.errors.append(SemanticError(node.init.pos_start, node.init.pos_end, "Invalid cycle initialization"))

        if isinstance(node.condition, BinOpNode):
            if node.condition.op not in ['<', '<=', '>', '>=', '==', '!=', '&&', '||']:
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
        elif isinstance(node.condition, IdNode):
            if not self.symbol_table.get(node.condition.name):
                self.unresolved_cases.append((node.condition, node))
                return
            condition_type = self.symbol_table.get_type(node.condition.name)
            if condition_type != 'bool':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must return a boolean value"))
        elif isinstance(node.condition, CurseCallNode):
            curse_node = self.symbol_table.get(node.condition.name)
            if curse_node is None:
                self.unresolved_cases.append((node.condition, node))
                return
            curse_return_type = curse_node.datatype
            if curse_return_type is None:
                curse_return_type = 'void'
            if curse_return_type != 'bool':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
        elif isinstance(node.condition, RelOpNode):
            pass
        elif isinstance(node.condition, LogOpNode):
            pass
        elif isinstance(node.condition, UnaryOpNode):
            if not node.condition.op.op == '!':
                self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
            pass
        else:
            self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))

        self.visit_children(node)
        print(f"Exiting CycleConditionNode")

    def resolve_unresolved(self):
        print("Resolving unresolved references...")
        print(f"Unresolved cases: {self.unresolved_cases}")

        for node, parent in self.unresolved_cases:
            print(f'\tSolving: {type(node)}\n')
            if isinstance(node, VarAssignNode):
                symbol_type = self.symbol_table.get_type(node.name)
                print(f"\n\n\nSymbol_table: {self.symbol_table.scopes}")

                if symbol_type is None:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared variable 1 '{node.name}'"))
                else:
                    symbol = self.symbol_table.get(node.name)
                    if symbol.restrict:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot modify restricted variable '{node.name}'"))
                        continue
                    if isinstance(node.value, CurseCallNode):
                        curse_node = self.symbol_table.get(node.value.name)
                        if curse_node is None:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undefined curse 2 '{node.value.name}'"))
                            break
                        else:
                            curse_return_type = curse_node.datatype
                            if curse_return_type is None:
                                curse_return_type = 'void'
                            if symbol_type != curse_return_type:
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 10: Expected '{symbol_type}' curse, got '{curse_return_type}' curse"))
                    else:
                        value_type = self.infer_type(node.value)
                        if value_type == 'null':
                            pass
                        else:
                            if symbol_type != value_type:
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 11: Expected '{symbol_type}', got '{value_type}'"))
                        

            elif isinstance(node, CurseCallNode):
                curse_node = self.symbol_table.get(node.name)
                print("HEYHEYHEY")
                if isinstance(curse_node, VarDecNode):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"'{node.name}' is not a curse"))
                elif isinstance(parent, VarAssignNode):
                    if isinstance(curse_node, CurseDecNode):
                        if parent.datatype != curse_node.datatype:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 12: Expected '{parent.datatype}' curse, got '{curse_node.datatype}' curse"))  
                elif isinstance(parent, ClanDecNode):
                    print("HEYHEYHEY")
                    if curse_node is None:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undefined curse 3 '{node.name}'"))
                    else:
                        if curse_node.datatype != parent.datatype:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 18: Expected '{parent.datatype}', got '{curse_node.datatype}'"))    
                elif isinstance(parent, BinOpNode):
                    if curse_node is None:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undefined curse 4 '{node.name}'"))
                    else:
                        while parent and not isinstance(parent, (CurseDecNode, VarDecNode, ClanDecNode, ClanIndexAssignNode)): #FIXME: Double check, i think this should be clan access node?
                            parent = parent.parent
                        if curse_node.datatype is None: curse_node_type = 'void'
                        else: curse_node_type = curse_node.datatype
                        if isinstance(parent, (CurseDecNode, VarDecNode, ClanDecNode)):
                            if curse_node_type != parent.datatype:
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 19: Expected '{parent.datatype}' curse, got '{curse_node_type}' curse"))
                        elif isinstance(parent, ClanIndexAssignNode):
                            clan_type = self.symbol_table.get_type(parent.name)
                            if clan_type == None:
                                return # CLAN TYPE NONE, MEANING IT WASNT FOUND IN THE SYMBOL TABLE
                            if curse_node_type != clan_type:
                                print(f'Symbol Table: {self.symbol_table.scopes}')
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 20: Expected '{clan_type}' curse, got '{curse_node_type}' curse"))
                elif isinstance(parent, ClanIndexAssignNode):
                    if curse_node is None:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undefined curse 5 '{node.name}'"))
                    else:
                        parent_type = self.symbol_table.get_type(parent.name)
                        if curse_node.datatype is None: curse_node_type = 'void'
                        else: curse_node_type = curse_node.datatype
                        if curse_node.datatype != parent_type:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 21: Expected '{parent_type}', got '{curse_node_type}'"))
                    if curse_node is None:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undefined curse 6 '{node.name}'"))
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
                                    self.errors.append(SemanticError(arg.pos_start, arg.pos_end, f"Type mismatch 12: Expected '{param_type}' type argument, got '{arg_type}'"))
                            if isinstance(parent, VarAssignNode):
                                parent_datatype = self.symbol_table.get_type(parent.name)
                                if parent_datatype != curse_node.datatype:
                                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 13: Expected '{parent_datatype}' curse, got '{curse_node.datatype}' curse"))
            elif isinstance(node, InvokeNode):
                if isinstance(node.value, IdNode):
                    symbol = self.symbol_table.get(node.value.name)
                    if symbol is None:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared variable 2 '{node.value.name}'"))
            
            elif isinstance(node, IdNode) and isinstance(parent, RecallNode):
                if isinstance(node, IdNode):
                    symbol = self.symbol_table.get(node.name)
                    if symbol is None:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared variable 3 '{node.name}'"))
                    else:
                        parent_function = parent
                        while parent_function and not isinstance(parent_function, CurseDecNode):
                            parent_function = parent_function.parent
                        if parent_function and parent_function.datatype != symbol.datatype:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 14: Expected '{parent_function.datatype}', got '{symbol.datatype}'"))

            elif isinstance(node, IdNode) and isinstance(parent, BinOpNode):
                symbol = self.symbol_table.get(node.name)
                if symbol is None:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared variable 4 '{node.name}'"))
                else:
                    if isinstance(symbol, VarDecNode) and isinstance(symbol.value, NullNode):
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot perform operation on Null value"))
                    if parent.op == '/' and isinstance(symbol.value, NumNode) and symbol.value.value == 0:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 15"))
                    elif parent.op == '/' and isinstance(symbol.value, BinOpNode) and symbol.value.value == 0:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 16"))

            elif isinstance(node, IdNode) and isinstance(parent, ClanDecNode):
                symbol = self.symbol_table.get_type(node.name)
                if symbol is None:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared variable 5 '{node.name}'"))
                else:
                    if symbol != parent.datatype:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 17: Expected '{parent.datatype}', got '{symbol}'"))
            elif isinstance(node, IdNode):
                symbol = self.symbol_table.get(node.name)
                symbol_type = self.symbol_table.get_type(node.name)
                if symbol is None:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared variable 6 '{node.name}'"))
                if isinstance(parent, StringConcatNode):
                    if symbol_type == 'bool':
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot concatenate string with boolean"))
                    elif symbol_type == 'null':
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot concatenate string with null"))
            elif isinstance(node, BinOpNode):
                binop_type = self.infer_type(node)
                left_type = self.infer_type(node.left)
                right_type = self.infer_type(node.right)
                binop_parent = node.parent
                op = node.op 

                if left_type == 'null' or right_type == 'null':
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot perform binary operation on Null value"))
                    continue

                if isinstance(binop_parent, (VarDecNode)):
                    if binop_type != binop_parent.datatype:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 15: Expected '{binop_parent.datatype}', got '{binop_type}'"))
                elif isinstance(binop_parent, (RecallNode)):
                    parent_function = binop_parent.parent
                    while parent_function and not isinstance(parent_function, CurseDecNode):
                        parent_function = parent_function.parent
                    if parent_function and parent_function.datatype != binop_type:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 16: Expected '{parent_function.datatype}', got '{binop_type}'"))
                    else: print(f"Unhandled Error: {parent.function.datatype} and {binop_type}")
                elif isinstance(binop_parent, (CycleConditionNode)):
                    if binop_type != 'bool':
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"3 Condition must be a boolean expression, got '{binop_type}'"))
                elif isinstance(binop_parent, (VowNode, ElseVow)):
                    if binop_type != 'bool':
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"4 Condition must be a boolean expression, got '{binop_type}'"))
                elif isinstance(binop_parent, (WoogieTrueNode)):
                    if binop_type != 'bool':
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"5 Condition must be a boolean expression, got '{binop_type}'"))
                elif isinstance(binop_parent, SustainNode):
                    if binop_type != 'bool':
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"6 Condition must be a boolean expression, got '{binop_type}'"))
                elif isinstance(binop_parent, PerformSustainNode):
                    if binop_type != 'bool':
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"7 Condition must be a boolean expression, got '{binop_type}'"))
                        
                if op == '/':
                    if isinstance(node.right, NumNode) and node.right.value == 0:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 1"))
                    elif isinstance(node.right, IdNode) and isinstance(node.right.parent, BinOpNode):
                        id_symbol = self.symbol_table.get(node.right.name)
                        if id_symbol: # If the IdNode is a variable
                            if isinstance(id_symbol, VarDecNode) and isinstance(id_symbol.value, NumNode) and id_symbol.value.value == 0:
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 2"))
                    elif isinstance(node.right, ClanAccessNode):
                        value = None
                        clan_symbol = self.symbol_table.get(node.right.name)
                        if not clan_symbol: 
                            self.unresolved_cases.append((node.right, node))
                            return
                        if clan_symbol and isinstance(clan_symbol, ClanDecNode):
                            size1_value = size2_value = index1_value = index2_value = None

                            if node.right.index2 and not clan_symbol.size2:
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index out of bounds 3: '{node.right.name}' is a single-dimensional array"))
                                return
                            elif not node.right.index2 and clan_symbol.size2:
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index out of bounds 3: '{node.right.name}' is a multi-dimensional array"))
                                return
                            
                            try:
                                size1_value = self.evaluate_node(clan_symbol.size1)
                            except: size1_value = None
                            
                            if clan_symbol.size2:
                                try:
                                    size2_value = self.evaluate_node(clan_symbol.size2)
                                except: size2_value = None
                            

                            try:
                                index1_value = self.evaluate_node(node.right.index1)
                            except: index1_value = None
                            
                            if node.right.index2:
                                try: 
                                    index2_value = self.evaluate_node(node.right.index2) 
                                except: index2_value = None
                            else: index2_value = None

                            print(f'Left Index: {node.right.index1}, Right Index: {node.right.index2}')
                            if index1_value is not None and size1_value is not None and (index1_value < 0 or index1_value >= self.evaluate_node(clan_symbol.size1)):
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index out of bounds 1: index1 is {index1_value}, but size1 is {self.evaluate_node(clan_symbol.size1)}"))
                            if index2_value is not None and size2_value is not None and (index2_value < 0 or index2_value >= size2_value):
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index out of bounds 2: index2 is {index2_value}, but size2 is {self.evaluate_node(clan_symbol.size2)}"))
                            if index1_value is not None and (index2_value is None or index2_value is not None):
                                if index2_value is None:
                                    try: 
                                        value = clan_symbol.initial_values.values[index1_value]
                                    except IndexError:
                                        return
                                else:
                                    value = clan_symbol.initial_values[index1_value].values[index2_value] #FIXME: not pointing to the right item in array
                                    print(f'Value Hey: {value}')
                                if isinstance(value, NumNode) and value.value == 0:
                                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 3"))
                                elif isinstance(value, IdNode) and isinstance(value.parent, BinOpNode):
                                    id_symbol = self.symbol_table.get(value.name)
                                    if id_symbol: # If the IdNode is a variable
                                        if isinstance(id_symbol, VarDecNode) and isinstance(id_symbol.value, NumNode) and id_symbol.value.value == 0:
                                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 4"))
                                elif isinstance(value, BinOpNode):
                                    value = self.evaluate_node(value)
                                    if value == 0:
                                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 5"))
                
                left_type = self.infer_type(node.left)
                right_type = self.infer_type(node.right)
                if left_type != right_type:
                    if (left_type == 'string' and right_type in ['int', 'float']) or (right_type == 'string' and left_type in ['int', 'float']):
                        if not isinstance(parent, StringConcatNode):
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 1.2: Cannot concatenate '{left_type}' and '{right_type}'"))
                    elif left_type == 'int' and right_type == 'float':
                        if isinstance(parent, BinOpNode):
                            try:
                                evaluation = eval(f"{node.left.value} {node.op} {node.right.value}")
                            except: return
                            if evaluation == 0:
                                if isinstance(parent, BinOpNode) and parent.op == '/' and parent.right == node:
                                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 10"))
                        pass
                    elif left_type == 'float' and right_type == 'int':
                        if isinstance(parent, BinOpNode):
                            try:
                                evaluation = eval(f"{node.left.value} {node.op} {node.right.value}")
                            except: return
                            if evaluation == 0:
                                if isinstance(parent, BinOpNode) and parent.op == '/' and parent.right == node:
                                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Division by zero 11"))
                        pass
                    else:
                        if isinstance(node.left, IdNode) and not self.symbol_table.get(node.left.name):
                            self.errors.append(SemanticError(node.left.pos_start, node.left.pos_end, f"Undeclared variable 4.1 '{node.left.name}'"))
                        if isinstance(node.right, IdNode) and not self.symbol_table.get(node.right.name):
                            self.errors.append(SemanticError(node.right.pos_start, node.right.pos_end, f"Undeclared variable 5 '{node.right.name}'"))
                        if isinstance(node.left, CurseCallNode) and not self.symbol_table.get(node.left.name):
                            self.errors.append(SemanticError(node.left.pos_start, node.left.pos_end, f"Undefined curse 6 '{node.left.name}'"))
                        if isinstance(node.right, CurseCallNode) and not self.symbol_table.get(node.right.name):
                            self.errors.append(SemanticError(node.right.pos_start, node.right.pos_end, f"Undefined curse 7 '{node.right.name}'"))
                        if isinstance(node.left, ClanAccessNode) and not self.symbol_table.get(node.left.name):
                            self.errors.append(SemanticError(node.left.pos_start, node.left.pos_end, f"Undefined clan '{node.left.name}'"))
                        if isinstance(node.right, ClanAccessNode) and not self.symbol_table.get(node.right.name):
                            self.errors.append(SemanticError(node.right.pos_start, node.right.pos_end, f"Undefined clan '{node.right.name}'"))
                        if isinstance(node.left, BinOpNode) and not self.symbol_table.get(node.left.name):
                            self.errors.append(SemanticError(node.left.pos_start, node.left.pos_end, f"Undefined variable '{node.left.name}'"))
                        if isinstance(node.right, BinOpNode) and not self.symbol_table.get(node.right.name):
                            self.errors.append(SemanticError(node.right.pos_start, node.right.pos_end, f"Undefined variable '{node.right.name}'"))
                        if node.pos_start: self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot perform operation between '{left_type}' and '{right_type}'"))
                        else: self.errors.append(SemanticError(parent.pos_start, parent.pos_end, f"Cannot perform operation between '{left_type}' and '{right_type}'"))
                
            elif isinstance(node, VowNode):
                if isinstance(node.condition, BinOpNode):
                    if node.condition.op not in ['<', '<=', '>', '>=', '==', '!=', '&&', '||']:
                        self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
                elif isinstance(node.condition, IdNode):
                    if not self.symbol_table.get(node.condition.name):
                        self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, f"Undeclared variable 7 '{node.condition.name}'"))
                        return
                    condition_type = self.symbol_table.get_type(node.condition.name)
                    if condition_type != 'bool':
                        self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must return a boolean value"))
                elif isinstance(node.condition, CurseCallNode):
                    curse_node = self.symbol_table.get(node.condition.name)
                    if curse_node is None:
                        self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, f"Undefined curse 8 '{node.condition.name}'"))
                        return
                    curse_return_type = curse_node.datatype
                    if curse_return_type is None:
                        curse_return_type = 'void'
                    if curse_return_type != 'bool':
                        self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
                elif isinstance(node.condition, RelOpNode):
                    pass
                elif isinstance(node.condition, LogOpNode):
                    pass
                else:
                    self.errors.append(SemanticError(node.condition.pos_start, node.condition.pos_end, "Condition must be a boolean expression"))
            elif isinstance(node, CycleConditionNode):
                node_init = node.init
                init_type = self.symbol_table.get_type(node_init.name)
                if init_type != 'int':
                    self.errors.append(SemanticError(node.init.pos_start, node.init.pos_end, "Cycle initialization must be an integer"))
            elif isinstance(node, ClanIndexAssignNode):
                symbol = self.symbol_table.get(node.name)
                if symbol is None:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared clan '{node.name}'"))
                else:
                    if symbol.restrict:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot modify restricted clan '{node.name}'"))
                        continue
                    symbol_type = self.symbol_table.get_type(node.name)
                    if symbol_type is None:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared clan '{node.name}'"))
                    else:
                        if isinstance(node.value, CurseCallNode):
                            if self.infer_type(node.value) == 'unknown':
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undefined curse 7 '{node.value.name}'"))
                        if node.value:
                            value_type = self.infer_type(node.value)
                            if value_type == 'unknown':
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undefined variable '{node.value.name}'"))
                            if symbol_type != value_type:
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch: Expected '{symbol_type}', got '{value_type}'"))

                        print(f'Symbol Table: {self.symbol_table.scopes}')
                        # Check for out-of-bounds errors
                        if isinstance(symbol, ClanDecNode):
                            if isinstance(symbol.size1, CurseCallNode):
                                size1_value = self.evaluate_node(symbol.size1)
                            elif isinstance(symbol.size1, NumNode):
                                size1_value = symbol.size1.value
                            elif isinstance(symbol.size1, IdNode):
                                if self.symbol_table.get_type(symbol.size1.name) == 'int':
                                    size1_value = self.symbol_table.get(symbol.size1.name).value
                                else: size1_value = None
                            elif isinstance(symbol.size1, BinOpNode):
                                size1_value = self.evaluate_node(symbol.size1)
                            else:
                                size1_value = self.evaluate_node(symbol.size1)

                            if symbol.size2:
                                if isinstance(symbol.size2, CurseCallNode):
                                    size2_value = self.evaluate_node(symbol.size2)
                                elif isinstance(symbol.size2, NumNode):
                                    size2_value = symbol.size2.value
                                elif isinstance(symbol.size2, IdNode):
                                    if self.symbol_table.get_type(symbol.size2.name) == 'int':
                                        size2_value = self.symbol_table.get(symbol.size2.name).value
                                    else: size2_value = None
                                elif isinstance(symbol.size2, BinOpNode):
                                    size2_value = self.evaluate_node(symbol.size2)     
                                else:
                                    size2_value = self.evaluate_node(symbol.size2)
                            else:
                                size2_value = None

                            index1_value = self.evaluate_node(node.index1)
                            index2_value = self.evaluate_node(node.index2) if node.index2 else None
                            
                            if index1_value is not None and size1_value is not None and (index1_value < 0 or index1_value >= size1_value):
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index out of bounds 8: index1 is {index1_value}, but size1 is {size1_value}"))

                            if index2_value is not None and size2_value is not None and (index2_value < 0 or index2_value >= size2_value):
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index out of bounds 9: index2 is {index2_value}, but size2 is {size2_value}"))
            elif isinstance(node, LenNode):
                len_value = node.name

                if isinstance(len_value, IdNode):
                    symbol = self.symbol_table.get(len_value.name)
                    if not symbol:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared variable 7 '{len_value.name}'"))
                        continue
                    else:
                        symbol_type = self.symbol_table.get_type(node.name.name)
                        if isinstance(symbol, ClanDecNode):
                            pass
                        elif isinstance(symbol, VarDecNode):
                            if symbol_type == 'string':
                                pass
                            else: 
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected string, got '{symbol_type}'"))
                        elif isinstance(symbol, StringNode):
                            pass
                        else:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected string or clan name, got '{symbol_type}'"))
                elif isinstance(len_value, StringNode):
                    pass
            
            elif isinstance(node, CleaveNode):
                true_parent = parent
                while true_parent and not isinstance(true_parent, (VarDecNode, VarAssignNode, ClanIndexAssignNode, ClanDecNode, InvokeNode)):
                    true_parent = true_parent.parent
                arg1 = node.arg1
                arg2 = node.index1
                arg3 = node.index2
                arg1_type = self.infer_type(arg1)
                arg2_type = self.infer_type(arg2)
                arg3_type = self.infer_type(arg3)
        
                if isinstance(arg1, IdNode) and not self.symbol_table.get(arg1.name):
                    self.unresolved_cases.append((node, parent))
                elif isinstance(arg1, StringNode):
                    pass
                else:
                    print(f'Arg1 Symbol: {arg1_symbol}\n True Parent: {true_parent}')
                    if isinstance(true_parent, (VarDecNode, VarAssignNode, ClanIndexAssignNode, InvokeNode)):
                        arg1_symbol = self.symbol_table.get(arg1.name)
                        if arg1_symbol is None:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared variable 8 '{arg1.name}'"))
                            continue
                        else: 
                            if isinstance(arg1_symbol, ClanDecNode):
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot assign clan to a non-clan variable"))
                        if not arg1_type == 'string':
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected string for cleave first argument, got '{arg1_type}'"))
                            continue
                        if isinstance(true_parent, VarDecNode):
                            if true_parent.datatype != 'string':
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected '{true_parent.datatype}', got '{arg1_type}'"))
                        elif isinstance(true_parent, (VarAssignNode, ClanIndexAssignNode)):
                            if not self.symbol_table.get(true_parent.name):
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared variable 9 '{true_parent.name}'"))
                                continue
                            else:
                                if true_parent.datatype != 'string':
                                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected '{true_parent.datatype}', got '{arg1_type}'"))

                    elif isinstance(true_parent, ClanDecNode):
                        arg1_symbol = self.symbol_table.get(arg1.name)
                        if arg1_symbol is None:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared variable 10 '{arg1.name}'"))
                            continue
                        elif not isinstance(arg1_symbol, ClanDecNode):
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected clan in first argument"))
                        elif true_parent.datatype != arg1_symbol.datatype:
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type mismatch 17: Expected '{true_parent.datatype}', got '{arg1_symbol.datatype}'"))
                    else:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected clan or string (1), got '{arg1_type}'"))

                if isinstance(arg2, IdNode) and not self.symbol_table.get(arg2.name):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared variable 11 '{arg2.name}'"))
                    continue
                else: 
                    if not arg2_type == 'int':
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected 'int', got '{arg2_type}'"))

                if isinstance(arg3, IdNode) and not self.symbol_table.get(arg3.name):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Undeclared variable 12 '{arg3.name}'"))
                    continue
                else:
                    if not arg3_type == 'int':
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Expected 'int', got '{arg3_type}'"))


        print(f"Unresolved cases after resolution: {self.unresolved_cases}\n")

    def infer_type(self, node):
        if isinstance(node, NumNode):
            return 'int' if isinstance(node.value, int) else 'float'
        elif isinstance(node, StringNode):
            return 'string'
        elif isinstance(node, BoolNode):
            return 'bool'
        elif isinstance(node, RelOpNode):
            return 'bool'
        elif isinstance(node, LogOpNode):
            return 'bool'
        elif isinstance(node, UnaryOpNode):
            type = self.infer_type(node.expr) 
            return type
        elif isinstance(node, ExponentNode):
            left = node.left
            right = node.right
            if left == 'float' or right == 'float':
                return 'float'
            else: return 'int'
        elif isinstance(node, NullNode):
            return 'null'
        elif isinstance(node, IdNode):
           if self.symbol_table.get_type(node.name):
               return self.symbol_table.get_type(node.name)
           else: return 'unknown'
        elif isinstance(node, BinOpNode):
            if node.op in ['<', '>', '<=', '>=', '==', '!=', '!', '&&', '||']:
                return 'bool'
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
                if curse_node.datatype:
                    return curse_node.datatype
                else: return 'void'
            return 'unknown'
        elif isinstance(node, LenNode):
            return 'int'
        elif isinstance(node, CleaveNode):
            if isinstance(node.arg1, IdNode):
                symbol = self.symbol_table.get(node.arg1.name)
                if isinstance(symbol, ClanDecNode):
                    return symbol.datatype
                elif isinstance(symbol, VarDecNode):
                    return symbol.datatype
                elif isinstance(symbol, CurseDecNode):
                    if symbol.datatype:
                        return symbol.datatype
                    else: return 'void'
                else: return 'unknown'
            elif isinstance(node.arg1, StringNode):
                return 'string'
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
        if self.scopes:
            self.scopes[-1][name] = value
            print(f"Id '{name}' not found in global scope, \nAdding {name} to local scope {self.scopes[-1]}...\nAppend Success... New Symbol Stack: {self.scopes}")
        else: 
            self.scopes.append({})
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
                    if isinstance(error, list):
                        errors.extend(error)
                    else:
                        errors.append(error)
            elif self.current_token is not None and self.current_token.type == 'id':
                assignment, error = self.parseIdCall()
                if assignment:
                    root.add_child(assignment)
                if error:
                    if isinstance(error, list):
                        errors.extend(error)
                    else:
                        errors.append(error)
            else: 
                self.advance()
        return root, errors

    def parseFactor(self):
        tok = self.current_token

        if tok.type in ('int_literal', 'float_literal'):
            self.advance()
            if self.current_token.type in ('++', '--'):
                op = self.current_token
                pos_end = self.current_token.pos_end
                self.advance()
                return UnaryOpNode(op, NumNode(tok.value, tok.pos_start, tok.pos_end), post=True, pos_start=tok.pos_start, pos_end=pos_end), None
            return NumNode(tok.value, tok.pos_start, tok.pos_end), None
        elif tok.type == 'string_literal':
            self.advance()
            return StringNode(tok.value, tok.pos_start, tok.pos_end), None
        elif tok.type == 'cleave': # if cleave returns string 
            self.advance()
            if self.current_token.type != '(':
                return None, SemanticError(tok.pos_start, tok.pos_end, "Expected: '('")
            self.advance()
            argument1, error = self.parseExpr()
            if error: return None, error

            if isinstance(argument1, IdNode):
                arg1_node = self.symbol_table.get(argument1.name)
                if isinstance(arg1_node, ClanDecNode):
                    return None, SemanticError(argument1.pos_start, argument1.pos_end, f"Cannot perform operation on a clan")

            if self.current_token.type != ',':
                return None, SemanticError(tok.pos_start, tok.pos_end, "Expected: ','")
            self.advance()
            argument2, error = self.parseExpr()
            if error: return None, error
            if self.current_token.type != ',':
                return None, SemanticError(tok.pos_start, tok.pos_end, "Expected: ','")
            self.advance()
            argument3, error = self.parseExpr()
            if error: return None, error
            if self.current_token.type != ')':
                return None, SemanticError(tok.pos_start, tok.pos_end, "Expected: ')'")
            cleave_end = self.current_token.pos_end
            self.advance()
            return CleaveNode(argument1, argument2, argument3, tok.pos_start, cleave_end), None
        elif tok.type == 'bool_literal':
            self.advance()
            return BoolNode(tok.value, tok.pos_start, tok.pos_end), None
        elif tok.type == 'null_literal':
            self.advance()
            if not self.current_token.type == ';':
                return None, SemanticError(self.current_token.pos_start, self.current_token.pos_end, "Expected: ';'")
            return NullNode(tok.value, tok.pos_start, tok.pos_end), None
        elif tok.type == 'id' and self.peek().type == '[':
            index1, index2 = None, None
            name = tok.value
            pos_start = tok.pos_start
            self.advance()
            self.advance()
            index1, error = self.parseExpr()
            if error: return None, error
            if self.current_token.type != ']':
                return None, SemanticError(tok.pos_start, tok.pos_end, "Expected: ']'")
            self.advance()
            if self.current_token.type == '[':
                self.advance()
                index2, error = self.parseExpr()
                if error: return None, error
                if self.current_token.type != ']':
                    return None, SemanticError(tok.pos_start, tok.pos_end, "Expected: ']'")
                self.advance()
            return ClanAccessNode(name, index1, index2, pos_start, self.current_token.pos_end), None
        elif tok.type == 'id' and self.peek().type == '(':
            name = tok.value
            pos_start = tok.pos_start
            self.advance()
            self.advance()
            arguments = []
            while self.current_token.type != ')':
                argument, error = self.parseExpr()
                if error: return None, error
                arguments.append(argument)
                if self.current_token.type == ',':
                    while self.current_token.type == ',':
                        self.advance()
                        argument, error = self.parseExpr()
                        if error: return None, error
                        arguments.append(argument)
            if self.current_token.type == ')':
                pos_end = self.current_token.pos_end
                self.advance()
            return CurseCallNode(name, arguments, pos_start, pos_end), None
        elif tok.type == 'id' and self.peek().type in ['+=', '-=', '*=', '/=', '%=']:
            name = tok.value
            pos_start = tok.pos_start
            self.advance()
            if self.current_token.type == '+=':
                op = '+'
            elif self.current_token.type == '-=':
                op = '-'
            elif self.current_token.type == '*=':
                op = '*'
            elif self.current_token.type == '/=':
                op = '/'
            elif self.current_token.type == '%=':
                op = '%'
            self.advance()
            value, error = self.parseExpr()
            if error: return None, error
            left = IdNode(name, pos_start, self.current_token.pos_end)
            right = value
            bin_op_node = BinOpNode(left, Token(op, pos_start=left.pos_start, pos_end=right.pos_end), right)
            return VarAssignNode(name, bin_op_node, pos_start, self.current_token.pos_end), None
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
        elif tok.type in ('-'):
            op = tok
            self.advance()
            factor, error = self.parseFactor()
            if error: return None, error
            return UnaryOpNode(op, factor, pre=True, pos_start=op.pos_start, pos_end=factor.pos_end), None
        elif tok.type == 'len':
            pos_start = tok.pos_start
            self.advance()
            if self.current_token.type != '(':
                return None, SemanticError(tok.pos_start, tok.pos_end, "Expected: '('")
            self.advance()
            if self.current_token.type not in ['id', 'string_literal', 'cleave', 'dismantle']:
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [id, string_literal, 'cleave', 'dismantle']")
            if self.current_token.type == 'dismantle':
                dismantle_start = self.current_token.pos_start
                self.advance()
                if self.current_token.type != '(':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                self.advance()
                clan_name, error = self.parseExpr()
                if error: return None, error
                if self.current_token.type != ',':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ','")
                self.advance()
                delimiter, errors = self.parseExpr()
                if errors: return None, errors
                if self.current_token.type != ')':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                dismantle_end = self.current_token.pos_end
                self.advance()
                len_value = DismantleNode(clan_name, delimiter, dismantle_start, dismantle_end)
            else:
                len_value, error = self.parseExpr()
                if error: return None, error
            if self.current_token.type != ')':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
            len_end = self.current_token.pos_end
            self.advance()
            return LenNode(len_value, pos_start, len_end), None
        else:
            return None, SemanticError(tok.pos_start, tok.pos_end, "Expected one of [int, float, bool, null, identifier, '(', '++', '--', '+', '-', '!']")

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
            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of ['=', '+=', '-=', '*=', '/=', '%=', '++', '--', '(', '[', ';']")
        
        if self.current_token.type in ['=', '+=', '-=', '*=', '/=', '%=']:
            op = self.current_token.type
            self.advance()
            if self.current_token.type not in ['(', '++', '--', '!', 'id', 'cleave', 'len', 'dismantle', 'string_literal', 'int_literal', 'float_literal', 'bool_literal', 'null_literal']:
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of ['(', '++', '--', '!', 'id', 'cleave', 'len', 'dismantle', 'string_literal', 'int_literal', 'float_literal', 'bool_literal', 'null_literal']")
            
            if self.current_token.type == 'id' and self.peek().type == '(':
                value, error = self.parseExpr()
                if error: return None, error
                pos_end = self.current_token.pos_end
                return VarAssignNode(name, value, pos_start, pos_end), None
            elif self.current_token.type == 'id' and self.peek().type == '[':
                index1, index2 = None, None
                clan_id = self.current_token.value
                self.advance()
                self.advance() # self advanced two times to reach the actual index value
                index1, error = self.parseExpr()
                if error: return None, error
                if self.current_token.type != ']':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ']'")
                self.advance()
                if self.current_token.type == '[':
                    self.advance()
                    index2, error = self.parseExpr()
                    if error: return None, error
                    if self.current_token.type != ']':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ']'")
                    self.advance()
                value = ClanAccessNode(clan_id, index1, index2, pos_start, self.current_token.pos_end)
                pos_end = self.current_token.pos_end
                return VarAssignNode(name, value, pos_start, pos_end), None
            elif self.current_token.type == 'cleave':
                cleave_start = self.current_token.pos_start
                self.advance()
                if self.current_token.type != '(':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                self.advance()
                cleave_id = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end) # check node types after advancing
                self.advance() 
                if self.current_token.type != ',':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ','")
                self.advance()
                index1, error = self.parseExpr()
                if error: return None, error
                if self.current_token.type != ',':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ','")
                self.advance()
                index2, error = self.parseExpr()
                if error: return None, error
                if self.current_token.type != ')':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                self.advance()
                pos_end = self.current_token.pos_end
                return VarAssignNode(name, CleaveNode(cleave_id, index1, index2, cleave_start, pos_end), pos_start, pos_end), None
            elif self.current_token.type == 'dismantle':
                dismantle_start = self.current_token.pos_start
                self.advance()
                if self.current_token.type != '(':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                self.advance()
                dismantle_id = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end) #FIXME: check node type for dismantle.. can be string literal too i tink
                self.advance()
                if self.current_token.type != ',':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ','")
                self.advance()
                delimiter = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                self.advance()
                if self.current_token.type != ')':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                self.advance()
                pos_end = self.current_token.pos_end
                return VarAssignNode(name, DismantleNode(dismantle_id, delimiter, dismantle_start, pos_end), pos_start, pos_end), None
            elif self.current_token.type == 'len':
                len_pos_start = self.current_token.pos_start
                self.advance()
                if self.current_token.type not in ['id', 'string_literal', 'cleave', 'dismantle']:
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [id, string_literal, 'cleave', 'dismantle']")
                if self.current_token.type == 'dismantle':
                    dismantle_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type != '(':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                    self.advance()
                    clan_name, error = self.parseExpr()
                    if error: return None, error
                    if self.current_token.type != ',':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ','")
                    self.advance()
                    delimiter, errors = self.parseExpr()
                    if errors: return None, errors
                    if self.current_token.type != ')':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                    dismantle_end = self.current_token.pos_end
                    self.advance()
                    len_value = DismantleNode(clan_name, delimiter, dismantle_start, dismantle_end)
                else:
                    len_value, error = self.parseExpr()
                    if error: return None, error
                if self.current_token.type != ')':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                len_end = self.current_token.pos_end
                self.advance()
                return VarAssignNode(name, LenNode(len_value, len_pos_start, len_end), pos_start, pos_end), None
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
            index1, index2 = None, None
            self.advance()
            index1, error = self.parseExpr()
            if error: return None, error
            if self.current_token.type != ']':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ']'")
            self.advance()
            if self.current_token.type == '[':
                self.advance()
                index2, error = self.parseExpr()
                if error: return None, error
                if self.current_token.type != ']':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ']'")
                self.advance()
            if self.current_token.type != '=':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '='")
            self.advance()
            new_val, error = self.parseExpr()
            if error: return None, error
            return ClanIndexAssignNode(name, index1, index2, new_val, pos_start, self.current_token.pos_end), None
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
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: id or 'curse'")
                
            if self.current_token.type == 'id':
                name = self.current_token.value
                self.advance()

                if self.current_token.type not in ['=', '[', '[...]', ';', ',']:
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of ['=', '[', '[...]', ';', ',', ';']")

                if self.current_token.type == '=':
                    self.advance()
                    if self.current_token.type == 'id' and self.peek().type in ['++', '--']:
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
                                    declarations.append(VarDecNode(None, datatype, name, None, pos_start, self.current_token.pos_end))
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
                                    declarations.append(VarDecNode(None, datatype, name, None, pos_start, self.current_token.pos_end))
                            return declarations, None
                        return VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end), None
                    elif self.current_token.type == 'id' and self.peek().type == '[':
                        index1, index2 = None, None
                        clan_id = self.current_token.value
                        pos_start = self.current_token.pos_start
                        self.advance()
                        self.advance()
                        if self.current_token.type not in ['int_literal', 'float_literal', 'id', '+', '-', '++', '--']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, identifier, '+', '-', '++', '--']")
                        index1, error = self.parseExpr()
                        if error: return None, error
                        if self.current_token.type != ']':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ']'")
                        self.advance()
                        if self.current_token.type == '[':
                            self.advance()
                            index2, error = self.parseExpr()
                            if error: return None, error
                            if self.current_token.type != ']':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ']'")
                            self.advance()
                        value = ClanAccessNode(clan_id, index1, index2, pos_start, self.current_token.pos_end)
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
                                    declarations.append(VarDecNode(None, datatype, name, None, pos_start, self.current_token.pos_end))
                        return VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end), None
                    elif self.current_token.type == 'id' and self.peek().type == '(':
                        value, error = self.parseExpr()
                        if error: return None, error
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
                                    declarations.append(VarDecNode(None, datatype, name, None, pos_start, self.current_token.pos_end))
                            return declarations, None
                        return VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end), None
                    elif self.current_token.type == 'cleave':
                        cleave_start = self.current_token.pos_start
                        self.advance()
                        if self.current_token.type != '(':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                        else:
                            self.advance()
                            if self.current_token.type not in ['string_literal', 'id']:
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [string, identifier]")

                            if self.current_token.type == 'string_literal':
                                cleave_id = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            
                            if self.current_token.type == 'id': 
                                cleave_id = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end) 
                            
                            self.advance()
                            if self.current_token.type != ',':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Missing Parameter")
                            
                            self.advance()
                            if self.current_token.type not in ['int_literal', 'float_literal', 'id', '+', '-', '++', '--']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, identifier, '+', '-', '++', '--']")
                            index1, error = self.parseExpr()
                            if error: return None, error

                            if self.current_token.type != ',':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Missing Parameter")
            
                            self.advance()
                            if self.current_token.type not in ['int_literal', 'float_literal', 'id', '+', '-', '++', '--', 'len']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, identifier , '+', '-', '++', '--', 'len']")
                            index2, error = self.parseExpr()
                            if error: return None, error

                            if self.current_token.type != ')':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                            
                            self.advance()
                            return VarDecNode(None, datatype, name, CleaveNode(cleave_id, index1, index2, cleave_start, self.current_token.pos_end), pos_start, self.current_token.pos_end), None
                    
                    elif self.current_token.type == 'len':
                        len_start = self.current_token.pos_start
                        self.advance()
                        if self.current_token.type != '(':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                        self.advance()
                        if self.current_token.type not in ['id', 'string_literal', 'cleave', 'dismantle']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [id, string_literal, 'cleave', 'dismantle']")
                        if self.current_token.type == 'dismantle':
                            dismantle_start = self.current_token.pos_start
                            self.advance()
                            if self.current_token.type != '(':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                            self.advance()
                            clan_name, error = self.parseExpr()
                            if error: return None, error
                            if self.current_token.type != ',':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ','")
                            self.advance()
                            delimiter, errors = self.parseExpr()
                            if errors: return None, errors
                            if self.current_token.type != ')':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                            dismantle_end = self.current_token.pos_end
                            self.advance()
                            len_value = DismantleNode(clan_name, delimiter, dismantle_start, dismantle_end)
                        else:
                            len_value, error = self.parseExpr()
                            if error: return None, error
                        if self.current_token.type != ')':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                        len_end = self.current_token.pos_end
                        self.advance()
                        return VarDecNode(None, datatype, name, LenNode(len_value, len_start, len_end), pos_start, self.current_token.pos_end), None
                    
                    else:
                        if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'bool_literal', 'null_literal', 'id', '(', '[', '+', '-', '++', '--']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, string, boolean, identifier, '(', '+', '-', '++', '--']")
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
                                    declarations.append(VarDecNode(None, datatype, name, None, pos_start, self.current_token.pos_end))
                                else:
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected '=' or ';'")
                            return declarations, None
                        return VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end), None
                elif self.current_token.type == '[':
                    size1, size2 = None, None
                    self.advance()
                    if self.current_token.type not in ['int_literal', 'id', '(', '+', '-', '++', '--']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, identifier, '(', '+', '-', '++', '--']")
                    size1, error = self.parseExpr()
                    if error: return None, error
                    if self.current_token.type != ']':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ']'")
                    self.advance()

                    if self.current_token.type not in ['=', '[']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '=' or '['")

                    if self.current_token.type == '=': # Parse one dimensional clan declaration
                        initial_values = [] 
                        self.advance()
                        if self.current_token.type not in ['cleave', 'dismantle', '{']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of ['cleave', 'dismantle', '{{']")
                        
                        if self.current_token.type == '{':
                            self.advance()
                            clan_lit_start = self.current_token.pos_start
                            while self.current_token.type != '}':
                                if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(', '+', '-', '++', '--']:
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, string, identifier, '(', '+', '-', '++', '--']")
                                new_val, error = self.parseExpr()
                                if error: return None, error
                                initial_values.append(new_val)
                                if self.current_token.type not in [',', '}']:
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected 3: ',' or '}}'")
                                if self.current_token.type == ',': 
                                    self.advance() 
                            if self.current_token.type != '}':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '}}'")
                            pos_end = self.current_token.pos_end
                            self.advance() # move past the closing brace '}'
                            clan_literal_node = ClanLiteralNode(initial_values, clan_lit_start, pos_end)
                            return ClanDecNode(None, datatype, name, size1, size2, clan_literal_node, pos_start, self.current_token.pos_end), None
                        elif self.current_token.type == 'cleave':
                            cleave_start = self.current_token.pos_start
                            self.advance()
                            if self.current_token.type != '(':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                            self.advance()
                            if self.current_token.type not in ['string_literal', 'id']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [string, identifier]")
                            if self.current_token.type == 'string_literal':
                                argument1 = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            if self.current_token.type == 'id':
                                argument1 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            self.advance()
                            if self.current_token.type != ',':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Missing Parameter")
                            self.advance()
                            if self.current_token.type not in ['int_literal', 'id']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, identifier, '+', '-', '++', '--']")
                            if self.peek().type in ['+', '-', '/', '%', '*', '**']:
                                argument2, error = self.parseExpr()
                                if error: return None, error
                            elif self.current_token.type == 'id':
                                argument2 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                                self.advance()
                            elif self.current_token.type == 'int_literal':
                                argument2 = NumNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                                self.advance()
                            if self.current_token.type != ',':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ','")
                            self.advance()
                            if self.current_token.type not in ['int_literal', 'id']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, identifier, '+', '-', '++', '--']")
                            if self.peek().type in ['+', '-', '/', '%', '*', '**']:
                                argument3, error = self.parseExpr()
                                if error: return None, error
                            elif self.current_token.type == 'id':
                                argument3 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                                self.advance()
                            elif self.current_token.type == 'int_literal':
                                argument3 = NumNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                                self.advance()
                            if self.current_token.type != ')':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                            pos_end = self.current_token.pos_end
                            self.advance()
                            return ClanDecNode(None, datatype, name, size1, size2, CleaveNode(argument1, argument2, argument3, cleave_start, pos_end), pos_start, pos_end), None
                        elif self.current_token.type == 'dismantle':
                            dismantle_start = self.current_token.pos_start
                            self.advance()
                            if self.current_token.type != '(':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                            self.advance()
                            if self.current_token.type not in ['string_literal', 'id']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [string, identifier]")
                            if self.current_token.type == 'string_literal':
                                argument1 = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            if self.current_token.type == 'id':
                                argument1 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            self.advance()
                            if self.current_token.type != ',':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Missing Parameter")
                            self.advance()
                            if self.current_token.type != 'string_literal':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: string type parameter")
                            argument2 = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            self.advance()
                            if self.current_token.type != ')':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                            pos_end = self.current_token.pos_end
                            self.advance()
                            return ClanDecNode(None, datatype, name, size1, size2, DismantleNode(argument1, argument2, dismantle_start, pos_end), pos_start, pos_end), None
                    
                    elif self.current_token.type == '[':
                        new_clan_literal = []
                        clan_literal_node = None
                        self.advance()
                        if self.current_token.type not in ['int_literal', 'id', '(', '+', '-', '++', '--']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, identifier, '(', '+', '-', '++', '--']")
                        size2, error = self.parseExpr()
                        if error: return None, error
                        if self.current_token.type != ']':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ']'")
                        self.advance()
                        initial_values = []
                        if self.current_token.type != '=':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '='")
                        self.advance()
                        if self.current_token.type != '{':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                        while self.current_token.type != '}':
                            self.advance()
                            if self.current_token.type != '{':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ('")
                            clan_lit_start = self.current_token.pos_start
                            self.advance()
                            while self.current_token.type != '}':
                                if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(', '+', '-', '++', '--']:
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, string, identifier, '(', '+', '-', '++', '--']")
                                new_val, error = self.parseExpr()
                                if error: return None, error
                                new_clan_literal.append(new_val)
                                if self.current_token.type not in [',', '}']:
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected 4: ',' or '}}'")
                                if self.current_token.type == ',':
                                    while self.current_token.type == ',': 
                                        self.advance()
                                        if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(', '+', '-', '++', '--']:
                                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, string, identifier, '(', '+', '-', '++', '--']")
                                        new_val, error = self.parseExpr()
                                        if error: return None, error
                                        new_clan_literal.append(new_val)
                            clan_literal_node = ClanLiteralNode(new_clan_literal, clan_lit_start, self.current_token.pos_end)
                            initial_values.append(clan_literal_node)
                            new_clan_literal = []
                            if self.current_token.type != '}':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '}}'")
                            self.advance()
                            if self.current_token.type == ',':
                                while self.current_token.type == ',':
                                    self.advance()
                                    if self.current_token.type != '{':
                                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                                    clan_lit_start = self.current_token.pos_start
                                    self.advance()
                                    while self.current_token.type != '}':
                                        if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(', '+', '-', '++', '--']:
                                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, string, identifier, '(', '+', '-', '++', '--']")
                                        new_val, error = self.parseExpr()
                                        if error: return None, error
                                        new_clan_literal.append(new_val)
                                        if self.current_token.type not in [',', '}']:
                                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected 4: ',' or '}}'")
                                        if self.current_token.type == ',':
                                            while self.current_token.type == ',': 
                                                self.advance()
                                                if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(', '+', '-', '++', '--']:
                                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, string, identifier, '(', '+', '-', '++', '--']")
                                                new_val, error = self.parseExpr()
                                                if error: return None, error
                                                new_clan_literal.append(new_val)
                                    clan_literal_node = ClanLiteralNode(new_clan_literal, clan_lit_start, self.current_token.pos_end)
                                    initial_values.append(clan_literal_node)
                                    self.advance()
                        if self.current_token.type != '}':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '}}'")
                        pos_end = self.current_token.pos_end
                        self.advance()
                        return ClanDecNode(None, datatype, name, size1, size2, initial_values, pos_start, pos_end), None
                elif self.current_token.type == '[...]':
                    self.advance()
                    initial_values = []
                    if self.current_token.type != '=':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '='")
                    self.advance()
                    if self.current_token.type not in ['cleave', 'dismantle', '{']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of ['cleave', 'dismantle', '{{']")
                    if self.current_token.type == '{':
                        self.advance()
                        while self.current_token.type != '}':
                            if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(', '+', '-', '++', '--']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, string, identifier, '(', '+', '-', '++', '--']")
                            new_val, error = self.parseExpr()
                            if error: return None, error
                            initial_values.append(new_val)
                            if self.current_token.type not in [',', '}']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected 6: ',' or '}}'")
                            if self.current_token.type == ',':
                                self.advance()
                        pos_end = self.current_token.pos_end
                        self.advance() # move past the closing brace
                        clan_literal_node = ClanLiteralNode(initial_values, pos_start, pos_end)
                        return ClanDecNode(None, datatype, name, None, None, clan_literal_node, pos_start, pos_end), None
                    
                    elif self.current_token.type == 'cleave':
                        cleave_start = self.current_token.pos_start
                        self.advance()
                        if self.current_token.type != '(':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                        self.advance()
                        if self.current_token.type not in ['string_literal', 'id']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [string, identifier]")
                        if self.current_token.type == 'string_literal':
                            argument1 = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        if self.current_token.type == 'id':
                            argument1 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        self.advance()
                        if self.current_token.type != ',':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Missing Parameter")
                        self.advance()
                        if self.current_token.type not in ['int_literal', 'id']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, identifier, '+', '-', '++', '--']")
                        if self.peek().type in ['+', '-', '/', '%', '*', '**']:
                            argument2, error = self.parseExpr()
                            if error: return None, error
                        elif self.current_token.type == 'id':
                            argument2 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            self.advance()
                        elif self.current_token.type == 'int_literal':
                            argument2 = NumNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            self.advance()
                        if self.current_token.type != ',':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ','")
                        self.advance()
                        if self.current_token.type not in ['int_literal', 'id']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, identifier, '+', '-', '++', '--']")
                        if self.peek().type in ['+', '-', '/', '%', '*', '**']:
                            argument3, error = self.parseExpr()
                            if error: return None, error
                        elif self.current_token.type == 'id':
                            argument3 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            self.advance()
                        elif self.current_token.type == 'int_literal':
                            argument3 = NumNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            self.advance()
                        if self.current_token.type != ')':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                        pos_end = self.current_token.pos_end
                        self.advance()
                        return ClanDecNode(None, datatype, name, None, None, CleaveNode(argument1, argument2, argument3, cleave_start, pos_end), pos_start, pos_end), None
                    
                    elif self.current_token.type == 'dismantle':
                        dismantle_start = self.current_token.pos_start
                        self.advance()
                        if self.current_token.type != '(':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                        self.advance()
                        if self.current_token.type not in ['string_literal', 'id']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [string, identifier]")
                        if self.current_token.type == 'string_literal':
                            argument1 = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        if self.current_token.type == 'id':
                            argument1 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        self.advance()
                        if self.current_token.type != ',':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Missing Parameter")
                        self.advance()
                        if self.current_token.type not in ['string_literal', 'id']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [string, identifier]")
                        if self.current_token.type == 'string_literal':
                            argument2 = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        if self.current_token.type == 'id':
                            argument2 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        self.advance()
                        if self.current_token.type != ')':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                        pos_end = self.current_token.pos_end
                        self.advance()
                        return ClanDecNode(None, datatype, name, None, None, DismantleNode(argument1, argument2, dismantle_start, pos_end), pos_start, pos_end), None
                
                elif self.current_token.type == ',':
                    declarations = [VarDecNode(None, datatype, name, None, pos_start, self.current_token.pos_end)]

                    while self.current_token.type == ',':
                        pos_start = self.current_token.pos_start
                        self.advance()
                        if self.current_token.type != 'id':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: identifier")
                        name = self.current_token.value
                        self.advance()

                        if self.current_token.type not in ['=', '[', ',', ';']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of ['=', '[', ',', ';']")
                        

                        if self.current_token.type == '=':
                            self.advance()
                            value, error = self.parseExpr()
                            if error: return None, error
                            declarations.append(VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end))
                        elif self.current_token.type == '[':
                            self.advance()
                            index1, error = self.parseExpr()
                            if error: return None, error
                            if self.current_token.type != ']':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ']'")
                            self.advance()
                            if self.current_token.tyoe == '[':
                                self.advance()
                                index2, error = self.parseExpr()
                            if error: return None, error
                            if self.current_token.type != ']':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ']'")
                            value = ClanAccessNode(name, index1, index2, pos_start, self.current_token.pos_end)
                            declarations.append(VarDecNode(None, datatype, name, value, pos_start, self.current_token.pos_end))
                            self.advance()
                        elif self.current_token.type == ',':
                            declarations.append(VarDecNode(None, datatype, name, None, pos_start, self.current_token.pos_end))
                        elif self.current_token.type == ';':
                            declarations.append(VarDecNode(None, datatype, name, None, pos_start, self.current_token.pos_end))
                    return declarations, None
                
                elif self.current_token.type == ';':
                    return VarDecNode(None, datatype, name, None, pos_start, self.current_token.pos_end), None
            elif self.current_token.type == 'curse': # curse with return type [int, float, bool, string]
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
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of ['int', 'float', 'string', 'bool']")   
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
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '{{'")
                self.advance()
                body, errors = self.parseBody()
                if errors: return body, errors
                pos_end = self.current_token.pos_end
                self.advance() # move past the closing '}'
                return CurseDecNode(datatype, name, parameters, body, pos_start, pos_end), None
                
        elif self.current_token.type == 'curse': # curse with no return type
            self.advance()
            if self.current_token.type not in ['id', 'domain']:
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: identifier or 'domain'")

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
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected one of ['int', 'float', 'string', 'bool']")
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
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: '{{'")
                else:
                    self.advance()
                    body, errors = self.parseBody()
                    if errors: return body, errors
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
                body, errors = self.parseBody()
                if errors: return body, errors
                self.advance() # move past the closing '}'
                return CurseDomainNode(body, pos_start, pos_end), None
        elif self.current_token.type == 'restrict':
            pos_start = self.current_token.pos_start
            self.advance()
            if self.current_token.type not in ['int', 'float', 'string', 'bool']: 
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected one of ['int', 'float', 'string', 'bool']")
            datatype = self.current_token.type
            self.advance()
            if self.current_token.type != 'id':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected: identifier")
            name = self.current_token.value
            self.advance()
            if self.current_token.type not in ['=', ',', ';', '[', '[...]']:
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected one of ['=', ',', ';', '[', '[...]']")
            
            if self.current_token.type == '=':
                self.advance()
                if self.current_token.type == 'id' and self.peek().type in ['++', '--']:
                    value, error = self.parseIdCall()
                    if error: return None, error
                    if self.peek() == ',':
                        declarations = [VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end)]
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
                                declarations.append(VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end))
                            else:
                                declarations.append(VarDecNode(True, datatype, name, None, pos_start, self.current_token.pos_end))
                        return declarations, None
                    return VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end), None
                elif self.current_token.type == 'id' and self.peek().type in ['+', '-', '/', '%', '*', '**']:
                    value, error = self.parseExpr()
                    if error: return None, error
                    if self.peek() == ',':
                        declarations = [VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end)]
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
                                declarations.append(VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end))
                            else:
                                declarations.append(VarDecNode(True, datatype, name, None, pos_start, self.current_token.pos_end))
                        return declarations, None
                    return VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end), None
                elif self.current_token.type == 'id' and self.peek().type == '[':
                    index1, index2 = None, None
                    clan_id = self.current_token.value
                    pos_start = self.current_token.pos_start
                    self.advance()
                    self.advance()
                    if self.current_token.type not in ['int_literal', 'float_literal', 'id', '+', '-', '++', '--']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, identifier, '+', '-', '++', '--']")
                    index1, error = self.parseExpr()
                    if error: return None, error
                    if self.current_token.type != ']':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ']'")
                    self.advance()
                    if self.current_token.type == '[':
                        self.advance()
                        index2, error = self.parseExpr()
                        if error: return None, error
                        if self.current_token.type != ']':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ']'")
                        self.advance()
                    value = ClanAccessNode(clan_id, index1, index2, pos_start, self.current_token.pos_end)
                    if self.peek() == ',':
                        declarations = [VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end)]
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
                                declarations.append(VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end))
                            else:
                                declarations.append(VarDecNode(True, datatype, name, None, pos_start, self.current_token.pos_end))
                    return VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end), None
                elif self.current_token.type == 'id' and self.peek().type == '(': # curse call?
                    value, error = self.parseExpr()
                    if error: return None, error
                    return VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end), None
                elif self.current_token.type == 'id':
                    value = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                    self.advance()
                    if self.current_token.type == ',':
                        declarations = [VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end)]
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
                                declarations.append(VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end))
                            else:
                                declarations.append(VarDecNode(True, datatype, name, None, pos_start, self.current_token.pos_end))
                        return declarations, None
                    return VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end), None
                elif self.current_token.type == 'cleave':
                    cleave_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type != '(':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                    else:
                        self.advance()
                        if self.current_token.type not in ['string_literal', 'id']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [string, identifier]")

                        if self.current_token.type == 'string_literal':
                            cleave_id = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        
                        if self.current_token.type == 'id': 
                            cleave_id = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end) 
                        
                        self.advance()
                        if self.current_token.type != ',':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Missing Parameter")
                        
                        self.advance()
                        if self.current_token.type not in ['int_literal', 'float_literal', 'id', '+', '-', '++', '--']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, identifier, '+', '-', '++', '--']")
                        index1, error = self.parseExpr()
                        if error: return None, error

                        if self.current_token.type != ',':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Missing Parameter")
        
                        self.advance()
                        if self.current_token.type not in ['int_literal', 'float_literal', 'id', '+', '-', '++', '--', 'len']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, identifier , '+', '-', '++', '--', 'len']")
                        index2, error = self.parseExpr()
                        if error: return None, error

                        if self.current_token.type != ')':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                        
                        self.advance()
                        return VarDecNode(True, datatype, name, CleaveNode(cleave_id, index1, index2, cleave_start, self.current_token.pos_end), pos_start, self.current_token.pos_end), None
                
                elif self.current_token.type == 'len':
                    len_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type != '(':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                    self.advance()
                    if self.current_token.type not in ['id', 'string_literal', 'cleave', 'dismantle']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [id, string_literal, 'cleave', 'dismantle']")
                    if self.current_token.type == 'dismantle':
                        dismantle_start = self.current_token.pos_start
                        self.advance()
                        if self.current_token.type != '(':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                        self.advance()
                        clan_name, error = self.parseExpr()
                        if error: return None, error
                        if self.current_token.type != ',':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ','")
                        self.advance()
                        delimiter, errors = self.parseExpr()
                        if errors: return None, errors
                        if self.current_token.type != ')':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                        dismantle_end = self.current_token.pos_end
                        self.advance()
                        len_value = DismantleNode(clan_name, delimiter, dismantle_start, dismantle_end)
                    else:
                        len_value, error = self.parseExpr()
                        if error: return None, error
                    if self.current_token.type != ')':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                    len_end = self.current_token.pos_end
                    self.advance()
                    return VarDecNode(True, datatype, name, LenNode(len_value, len_start, len_end), pos_start, self.current_token.pos_end), None
                
                else:
                    if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'bool_literal', 'null_literal', 'id', '(', '[', '+', '-', '++', '--']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, string, boolean, identifier, '(', '+', '-', '++', '--']")
                    value, error = self.parseExpr()
                    if error: return None, error
                    if self.current_token.type == ',': # for parsing multi variable declaration
                        declarations = [VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end)]
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
                                declarations.append(VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end))
                            elif self.current_token.type == ';':
                                declarations.append(VarDecNode(True, datatype, name, None, pos_start, self.current_token.pos_end))
                            else:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected '=' or ';'")
                        return declarations, None
                    return VarDecNode(True, datatype, name, value, pos_start, self.current_token.pos_end), None

            elif self.current_token.type == '[': # restricted clan dec
                self.advance()
                if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(', '+', '-', '++', '--']:
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, string, identifier, '(', '+', '-', '++', '--']")
                size1, error = self.parseExpr()
                if error: return None, error
                if self.current_token.type != ']':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ']'")
                self.advance()
                if self.current_token.type not in ['[', '=']:
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of ['[', '=']")
                

                if self.current_token.type == '[': # 2D clan
                    new_clan_literal = []
                    clan_literal_node = None
                    self.advance()
                    if self.current_token.type not in ['int_literal', 'id', '(', '+', '-', '++', '--']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, identifier, '(', '+', '-', '++', '--']")
                    size2, error = self.parseExpr()
                    if error: return None, error
                    if self.current_token.type != ']':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ']'")
                    self.advance()
                    initial_values = []
                    if self.current_token.type != '=':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '='")
                    self.advance()
                    if self.current_token.type != '{':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                    while self.current_token.type != '}':
                        self.advance()
                        if self.current_token.type != '{':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ('")
                        clan_lit_start = self.current_token.pos_start
                        self.advance()
                        while self.current_token.type != '}':
                            if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(', '+', '-', '++', '--']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, string, identifier, '(', '+', '-', '++', '--']")
                            new_val, error = self.parseExpr()
                            if error: return None, error
                            new_clan_literal.append(new_val)
                            if self.current_token.type not in [',', '}']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected 4: ',' or '}}'")
                            if self.current_token.type == ',':
                                while self.current_token.type == ',': 
                                    self.advance()
                                    if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(', '+', '-', '++', '--']:
                                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, string, identifier, '(', '+', '-', '++', '--']")
                                    new_val, error = self.parseExpr()
                                    if error: return None, error
                                    new_clan_literal.append(new_val)
                        clan_literal_node = ClanLiteralNode(new_clan_literal, clan_lit_start, self.current_token.pos_end)
                        initial_values.append(clan_literal_node)
                        new_clan_literal = []
                        if self.current_token.type != '}':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '}}'")
                        self.advance()
                        if self.current_token.type == ',':
                            while self.current_token.type == ',':
                                self.advance()
                                if self.current_token.type != '{':
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                                clan_lit_start = self.current_token.pos_start
                                self.advance()
                                while self.current_token.type != '}':
                                    if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(', '+', '-', '++', '--']:
                                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, string, identifier, '(', '+', '-', '++', '--']")
                                    new_val, error = self.parseExpr()
                                    if error: return None, error
                                    new_clan_literal.append(new_val)
                                    if self.current_token.type not in [',', '}']:
                                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected 4: ',' or '}}'")
                                    if self.current_token.type == ',':
                                        while self.current_token.type == ',': 
                                            self.advance()
                                            if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(', '+', '-', '++', '--']:
                                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, string, identifier, '(', '+', '-', '++', '--']")
                                            new_val, error = self.parseExpr()
                                            if error: return None, error
                                            new_clan_literal.append(new_val)
                                clan_literal_node = ClanLiteralNode(new_clan_literal, clan_lit_start, self.current_token.pos_end)
                                initial_values.append(clan_literal_node)
                                self.advance()
                    if self.current_token.type != '}':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '}}'")
                    pos_end = self.current_token.pos_end
                    self.advance()
                    return ClanDecNode(True, datatype, name, size1, size2, initial_values, pos_start, pos_end), None

                elif self.current_token.type == '=': # 1D clan
                    self.advance()
                    if self.current_token.type not in ['cleave', 'dismantle', '{']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of ['cleave', 'dismantle', '{{']")
                    if self.current_token.type == '{':
                        self.advance()
                        initial_values = []
                        while self.current_token.type != '}':
                            if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(', '+', '-', '++', '--']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, string, identifier, '(', '+', '-', '++', '--']")
                            new_val, error = self.parseExpr()
                            if error: return None, error
                            initial_values.append(new_val)
                            if self.current_token.type not in [',', '}']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ',' or '}}'")
                            if self.current_token.type == ',':
                                self.advance()
                        pos_end = self.current_token.pos_end
                        self.advance()
                        clan_literal_node = ClanLiteralNode(initial_values, pos_start, pos_end)
                        return ClanDecNode(None, datatype, name, size1, None, clan_literal_node, pos_start, pos_end), None
                    
                    elif self.current_token.type == 'cleave':
                        cleave_start = self.current_token.pos_start
                        self.advance()
                        if self.current_token.type != '(':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                        self.advance()
                        if self.current_token.type not in ['string_literal', 'id']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [string, identifier]")
                        if self.current_token.type == 'string_literal':
                            argument1 = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        if self.current_token.type == 'id':
                            argument1 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        self.advance()
                        if self.current_token.type != ',':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Missing Parameter")
                        self.advance()
                        if self.current_token.type not in ['int_literal', 'id']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, identifier, '+', '-', '++', '--']")
                        if self.peek().type in ['+', '-', '/', '%', '*', '**']:
                            argument2, error = self.parseExpr()
                            if error: return None, error
                        elif self.current_token.type == 'id':
                            argument2 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            self.advance()
                        elif self.current_token.type == 'int_literal':
                            argument2 = NumNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            self.advance()
                        if self.current_token.type != ',':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ','")
                        self.advance()
                        if self.current_token.type not in ['int_literal', 'id']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, identifier, '+', '-', '++', '--']")
                        if self.peek().type in ['+', '-', '/', '%', '*', '**']:
                            argument3, error = self.parseExpr()
                            if error: return None, error
                        elif self.current_token.type == 'id':
                            argument3 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            self.advance()
                        elif self.current_token.type == 'int_literal':
                            argument3 = NumNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            self.advance()
                        if self.current_token.type != ')':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                        pos_end = self.current_token.pos_end
                        self.advance()
                        return ClanDecNode(None, datatype, name, size1, None, CleaveNode(argument1, argument2, argument3, cleave_start, pos_end), pos_start, pos_end), None
                    
                    elif self.current_token.type == 'dismantle':
                        dismantle_start = self.current_token.pos_start
                        self.advance()
                        if self.current_token.type != '(':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                        self.advance()
                        if self.current_token.type not in ['string_literal', 'id']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [string, identifier]")
                        if self.current_token.type == 'string_literal':
                            argument1 = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        if self.current_token.type == 'id':
                            argument1 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        self.advance()
                        if self.current_token.type != ',':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Missing Parameter")
                        self.advance()
                        if self.current_token.type not in ['string_literal', 'id']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [string, identifier]")
                        if self.current_token.type == 'string_literal':
                            argument2 = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        if self.current_token.type == 'id':
                            argument2 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        self.advance()
                        if self.current_token.type != ')':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                        pos_end = self.current_token.pos_end
                        self.advance()
                        return ClanDecNode(True, datatype, name, size1, None, DismantleNode(argument1, argument2, dismantle_start, pos_end), pos_start, pos_end), None

            elif self.current_token.type == '[...]': # restricted clan dec
                self.advance()
                initial_values = []
                if self.current_token.type != '=':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '='")
                self.advance()
                if self.current_token.type not in ['cleave', 'dismantle', '{']:
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of ['cleave', 'dismantle', '{{']")
                if self.current_token.type == '{':
                    self.advance()
                    while self.current_token.type != '}':
                        if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', '(', '+', '-', '++', '--']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, string, identifier, '(', '+', '-', '++', '--']")
                        new_val, error = self.parseExpr()
                        if error: return None, error
                        initial_values.append(new_val)
                        if self.current_token.type not in [',', '}']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected 6: ',' or '}}'")
                        if self.current_token.type == ',':
                            self.advance()
                    pos_end = self.current_token.pos_end
                    self.advance() # move past the closing brace
                    clan_literal_node = ClanLiteralNode(initial_values, pos_start, pos_end)
                    return ClanDecNode(None, datatype, name, None, None, clan_literal_node, pos_start, pos_end), None
                
                elif self.current_token.type == 'cleave':
                    cleave_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type != '(':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                    self.advance()
                    if self.current_token.type not in ['string_literal', 'id']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [string, identifier]")
                    if self.current_token.type == 'string_literal':
                        argument1 = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                    if self.current_token.type == 'id':
                        argument1 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                    self.advance()
                    if self.current_token.type != ',':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Missing Parameter")
                    self.advance()
                    if self.current_token.type not in ['int_literal', 'id']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, identifier, '+', '-', '++', '--']")
                    if self.peek().type in ['+', '-', '/', '%', '*', '**']:
                        argument2, error = self.parseExpr()
                        if error: return None, error
                    elif self.current_token.type == 'id':
                        argument2 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        self.advance()
                    elif self.current_token.type == 'int_literal':
                        argument2 = NumNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        self.advance()
                    if self.current_token.type != ',':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ','")
                    self.advance()
                    if self.current_token.type not in ['int_literal', 'id']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, identifier, '+', '-', '++', '--']")
                    if self.peek().type in ['+', '-', '/', '%', '*', '**']:
                        argument3, error = self.parseExpr()
                        if error: return None, error
                    elif self.current_token.type == 'id':
                        argument3 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        self.advance()
                    elif self.current_token.type == 'int_literal':
                        argument3 = NumNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        self.advance()
                    if self.current_token.type != ')':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                    pos_end = self.current_token.pos_end
                    self.advance()
                    return ClanDecNode(None, datatype, name, None, None, CleaveNode(argument1, argument2, argument3, cleave_start, pos_end), pos_start, pos_end), None
                
                elif self.current_token.type == 'dismantle':
                    dismantle_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type != '(':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('")
                    self.advance()
                    if self.current_token.type not in ['string_literal', 'id']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [string, identifier]")
                    if self.current_token.type == 'string_literal':
                        argument1 = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                    if self.current_token.type == 'id':
                        argument1 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                    self.advance()
                    if self.current_token.type != ',':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Missing Parameter")
                    self.advance()
                    if self.current_token.type not in ['string_literal', 'id']:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [string, identifier]")
                    if self.current_token.type == 'string_literal':
                        argument2 = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                    if self.current_token.type == 'id':
                        argument2 = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                    self.advance()
                    if self.current_token.type != ')':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'")
                    pos_end = self.current_token.pos_end
                    self.advance()
                    return ClanDecNode(True, datatype, name, None, None, DismantleNode(argument1, argument2, dismantle_start, pos_end), pos_start, pos_end), None

            elif self.current_token.type == ',':
                pos_start = self.current_token.pos_start
                declarations = [VarDecNode('restrict', datatype, name, None, pos_start, self.current_token.pos_end)]
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
                        declarations.append(VarDecNode(True, datatype, name, None, pos_start, self.current_token.pos_end))
                return declarations, None
            elif self.current_token.type == ';':
                return VarDecNode(True, datatype, name, 0, pos_start, self.current_token.pos_end), None
        else:
            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.value}', Expected one of ['int', 'float', 'string', 'bool', 'curse', 'restrict']")
    
    def parseBody(self):
        body = BodyNode()
        errors = []

        while self.current_token.type != '}':
                if self.current_token.type in ['int', 'float', 'string', 'bool', 'curse', 'restrict']:
                    declarations, error = self.parseDeclaration()
                    if error: 
                        errors.append(error)
                        continue
                    if declarations:
                        if isinstance(declarations, list):
                            for declaration in declarations:
                                body.add_child(declaration)
                        else:
                            body.add_child(declarations)
                elif self.current_token.type == 'id':
                    assignment, error = self.parseIdCall()
                    if error:
                        errors.append(error)
                        continue
                    if assignment:
                        body.add_child(assignment)
                elif self.current_token.type == 'invoke':
                    invoke_pos_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type != '(':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('"))
                        continue
                    self.advance()
                    if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', 'cleave', 'len', '(', '[', '!', '+', '-', '++', '--']:
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, string, identifier, 'cleave', 'len', '(', '+', '-', '++', '--']"))
                        continue
                    value, error = self.parseExpr()
                    if error:
                        errors.append(error)
                        continue
                    if self.current_token.type != ')':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'"))
                        continue
                    self.advance() # move past the parenthesis
                    if self.current_token.type != ';':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ';'"))
                        continue
                    invoke_pos_end = self.current_token.pos_end
                    self.advance() # advance past the semicolon
                    body.add_child(InvokeNode(value, invoke_pos_start, invoke_pos_end))
                elif self.current_token.type == 'capture':
                    capture_pos_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type != '(':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('"))
                        continue
                    self.advance()
                    if self.current_token.type != 'id':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: identifier"))
                    name = IdNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                    self.advance()
                    if self.current_token.type != ')':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'"))
                        continue
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
                    pos_start = self.current_token.pos_start
                    pos_end = self.current_token.pos_end
                    self.advance()
                    if self.current_token.type == ';':
                        self.advance()
                        body.add_child(RecallNode(None, pos_start, pos_end))
                    else:
                        value, error = self.parseExpr()
                        if error:
                            errors.append(error)
                            continue
                        body.add_child(RecallNode(value, pos_start, self.current_token.pos_end))
                elif self.current_token.type == 'vow':
                    pos_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type != '(':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('"))
                        continue
                    self.advance()
                    condition, error = self.parseExpr()
                    if error:
                        errors.append(error)
                        continue
                    if self.current_token.type != ')':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'"))
                        continue
                    self.advance()
                    if self.current_token.type != '{':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '{{'"))
                        continue
                    self.advance()
                    body_node, body_errors = self.parseBody()
                    if body_errors:
                        errors.extend(body_errors)
                        continue
                    if self.current_token.type == '}':
                        self.advance()  # advance past the closing brace '}'
                    else_vows = []
                    while self.current_token.type == 'else' and self.peek().type == 'vow':
                        self.advance()
                        self.advance()
                        if self.current_token.type != '(':
                            errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('"))
                            continue
                        self.advance()
                        else_condition, error = self.parseExpr()
                        if error:
                            errors.append(error)
                            continue
                        if self.current_token.type != ')':
                            errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'"))
                            continue
                        self.advance()
                        if self.current_token.type != '{':
                            errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '{{'"))
                            continue
                        self.advance()
                        else_body_node, else_body_errors = self.parseBody()
                        if else_body_errors:
                            errors.extend(else_body_errors)
                            continue
                        if self.current_token.type == '}':
                            self.advance()  # advance past the closing '}'
                        else_vows.append(ElseVow(else_condition, else_body_node))
                    if self.current_token.type == 'else':
                        self.advance()
                        if self.current_token.type == '{':
                            self.advance()
                            else_pos_start = self.current_token.pos_start
                            else_body_node, else_body_errors = self.parseBody()
                            if else_body_errors:
                                errors.extend(else_body_errors)
                                continue
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
                            errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'"))
                            continue
                        self.advance()
                        if self.current_token.type != '{':
                            errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '{{'"))
                            continue
                        self.advance()
                        cases = []
                        while self.current_token.type != '}':
                            if self.current_token.type == 'woogie':
                                woogie_start = self.current_token.pos_start
                                self.advance()
                                if self.current_token.type in ['int_literal', 'float_literal', 'id']:
                                    case_expr, error = self.parseExpr()
                                    if error:
                                        errors.append(error)
                                        continue
                                elif self.current_token.type == 'string_literal':
                                    case_expr = StringNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                                    self.advance()
                                elif self.current_token.type == '(':
                                    self.advance()
                                    if self.current_token.type == 'id':
                                        case_expr, error = self.parseIdCall()
                                else:
                                    errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, "Expected: int_literal, float_literal, or string_literal"))
                                    continue
                                if self.current_token.type != ':':
                                    errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ':'"))
                                    continue
                                self.advance()
                                case_body, errors = self.parseWoogieBody()
                                if errors: 
                                    errors.append(errors)
                                    continue
                                cases.append(WoogieNode(case_expr, case_body, woogie_start, self.current_token.pos_end))
                            elif self.current_token.type == 'default':
                                default_start = self.current_token.pos_start
                                self.advance()
                                if self.current_token.type != ':':
                                    errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ':'"))
                                    continue
                                self.advance()
                                default_body, errors = self.parseWoogieBody()
                                if errors: 
                                    errors.append(errors)
                                    continue
                                cases.append(DefaultCaseNode(default_body, default_start, self.current_token.pos_end))
                            else: 
                                errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: 'woogie' or 'default'"))
                                continue
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
                                if error:
                                    errors.append(error)
                                    continue
                                if self.current_token.type == ':':
                                    self.advance()
                                    case_body, errors = self.parseWoogieBody()
                                    if errors: 
                                        errors.append(errors)
                                        continue
                                    cases.append(WoogieTrueNode(case_expr, case_body, woogie_start, self.current_token.pos_end))
                            elif self.current_token.type == 'default':
                                default_start = self.current_token.pos_start
                                self.advance()
                                if self.current_token.type == ':':
                                    self.advance()
                                    default_body, errors = self.parseWoogieBody()
                                    if errors: 
                                        errors.append(errors)
                                        continue
                                    cases.append(DefaultCaseNode(default_body, default_start, self.current_token.pos_end))
                        self.advance()
                        body.add_child(BoogieNode(None, cases, boogie_start, self.current_token.pos_end))
                    else: 
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '(' or '{{'"))
                        continue

                elif self.current_token.type == 'cycle':
                    cycle_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type != '(':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('"))
                        continue
                    self.advance()
                    cycle_condition, error = self.parseCycleCondition()
                    if error:
                        errors.append(error)
                        continue
                    if self.current_token.type != ')':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'"))
                        continue
                    self.advance()
                    if self.current_token.type != '{':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '{{'"))
                        continue
                    self.advance()
                    cycle_body, cycle_errors = self.parseBody()
                    if cycle_errors:
                        errors.extend(cycle_errors)
                        continue
                    self.advance() # advance past the closing brace
                    body.add_child(CycleNode(cycle_condition, cycle_body, cycle_start, self.current_token.pos_end)) 
                elif self.current_token.type == 'sustain':
                    sustain_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type != '(':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('"))
                        continue
                    self.advance()
                    condition, error = self.parseExpr()
                    if error:
                        errors.append(error)
                        continue
                    if self.current_token.type != ')':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'"))
                        continue
                    self.advance()
                    if self.current_token.type != '{':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '{{'"))
                        continue
                    self.advance()
                    sustain_body, sustain_errors = self.parseBody()
                    if sustain_errors:
                        errors.extend(sustain_errors)
                        continue
                    self.advance() # advance past the closing brace
                    body.add_child(SustainNode(condition, sustain_body, sustain_start, self.current_token.pos_end))
                elif self.current_token.type == 'perform':
                    perform_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type != '{':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '{{'"))
                        continue
                    self.advance()
                    perform_body, perform_errors = self.parseBody()
                    if perform_errors:
                        errors.extend(perform_errors)
                        continue
                    self.advance() # advance past the closing brace
                    if self.current_token.type != 'sustain':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: sustain"))
                        continue
                    self.advance()
                    if self.current_token.type != '(':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: '('"))
                        continue
                    self.advance()
                    condition, error = self.parseExpr()
                    if error:
                        errors.append(error)
                        continue
                    if self.current_token.type != ')':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ')'"))
                        continue
                    self.advance()
                    if self.current_token.type != ';':
                        errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected: ';'"))
                        continue
                    self.advance()
                    body.add_child(PerformSustainNode(perform_body, condition, perform_start, self.current_token.pos_end))
                else:
                    self.advance()
        return body, errors

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
                if self.current_token.type not in ['int_literal', 'float_literal', 'string_literal', 'id', 'cleave', 'len', '(', '[', '!', '+', '-', '++', '--']:
                    errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Got '{self.current_token.type}', Expected one of [int, float, string, identifier, 'cleave', 'len', '(', '+', '-', '++', '--']"))
                value, error = self.parseExpr()
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
                body_node, body_errors = self.parseBody()
                if body_errors: return None, body_errors
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
                    else_body_node, else_body_errors = self.parseBody()
                    if else_body_errors: return None, else_body_errors
                    if self.current_token.type == '}':
                        self.advance()  # Advance past the closing '}'
                    else_vows.append(ElseVow(else_condition, else_body_node))
                if self.current_token.type == 'else':
                    else_start = self.current_token.pos_start
                    self.advance()
                    if self.current_token.type == '{':
                        self.advance()
                        else_body_node, else_body_errors = self.parseBody()
                        if else_body_errors: return None, else_body_errors
                        else_end = self.current_token.pos_end
                        self.advance()
                        self.advance()  # Advance past the closing '}'
                        body.add_child(VowNode(condition, body_node, else_vows, ElseNode(else_body_node, else_start, self.current_token.pos_end), vow_start, else_end))
                else:
                    body.add_child(VowNode(condition, body_node, else_vows, None, vow_start, self.current_token.pos_end))
            else:
                self.advance()
        return body, None

def semantic_run(tokens):
    symbol_table = SymbolTable()
    visitor = MyASTVisitor(symbol_table)
    parser = Parser(tokens)
    ast, errors = parser.build_ast()
    

    # check if there is curse domain node in the ast
    if not any(isinstance(node, CurseDomainNode) for node in ast.children):
        errors.insert(0, DomainError(parser.current_token.pos_start, parser.current_token.pos_end, "Curse domain function is not defined"))

    if ast:
        visitor.visit(ast)
        visitor.resolve_unresolved()  
        print(symbol_table.scopes)
        tree_str = ast.tree_to_str()
        ast.print_tree()
    else:
        print("No AST built")
        return "No AST built", None, tree_str
    
    if visitor.errors:
        errors.extend(visitor.errors)
        if errors:
            errors.sort(key=lambda e: e.pos_start.ln)
        return None, errors, tree_str
    
    if errors:
        errors.sort(key=lambda e: e.pos_start.ln)

    return ast, errors, tree_str