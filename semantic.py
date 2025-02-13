##############
# IMPORTS
##############
from lexer import run as lexer_run
from lexer import string_with_arrows 

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

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Syntax Error', details)

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
        result += ' ' * col_start + '^' * (col_end - col_start)

        # Re-calculate indices
        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0 : idx_end = len(text)

    return result.replace('\t', ' ')

###################
# AST Nodes
###################

class ASTNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

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

    def to_dict(self):
        return {
            'data': self.data,
            'children': [child.to_dict() for child in self.children]
        }
    
class NumNode(ASTNode): # for numbers
    def __init__(self, value):
        super().__init__(f"Number: {value}")
        self.value = value

    def __repr__(self):
        return f"{self.value}"

class BinOpNode(ASTNode): # binary operation
    def __init__(self, left, op, right):
        super().__init__(f"Binary Operation: {op.type}")
        self.left = left
        self.op = op.type
        self.right = right
        self.add_child(left)
        self.add_child(right)

class RelOpNode(ASTNode): # relational operation
    def __init__(self, left, op, right):
        super().__init__(f"Relational Operation: {op.type}")
        self.left = left
        self.op = op.type
        self.right = right
        self.add_child(left)
        self.add_child(right)

class LogOpNode(ASTNode): # logical operation
    def __init__(self, left, op, right):
        super().__init__(f"Logical Operation: {op.type}")
        self.left = left
        self.op = op.type
        self.right = right
        self.add_child(left)
        self.add_child(right)

class UnaryOpNode(ASTNode): # unary operation
    def __init__(self, op, expr, pre=False, post=False):
        super().__init__("Unary Operation")
        self.op = UnaryOperator(op)
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
    def __init__(self, op):
        super().__init__(f"Unary Operator: {op.type}")
        self.op = op.type

class ExponentNode(ASTNode): # exponentiation
    def __init__(self, left, right):
        super().__init__("Exponentiation")
        self.left = left
        self.right = right
        self.add_child(left)
        self.add_child(right)

class BoolNode(ASTNode):
    def __init__(self, value):
        super().__init__(f"Bool: {value}")
        self.value = value

class NullNode(ASTNode):
    def __init__(self, value):
        super().__init__(f"Null")
        self.value = value
        
class RestrictNode(ASTNode): # for restrict keyword
    def __init__(self):
        super().__init__("Restrict")

class DatatypeNode(ASTNode): # for datatype keywords
    def __init__(self, datatype):
        super().__init__(f"Datatype: {datatype}")
        self.datatype = datatype

class IdNode(ASTNode): # for identifier names
    def __init__(self, name):
        super().__init__(f"Identifier: {name}")
        self.name = name

    def __repr__(self):
        return f"{self.name}"

class VarNode(ASTNode): # for variables
    def __init__(self, name):
        super().__init__(f"Variable: {name}")
        self.name = name

    def __repr__(self):
        return f"{self.name}"

class VarDecNode(ASTNode): # for variable assignments
    def __init__(self, restrict, datatype, name, value):
        super().__init__("Variable Declaration")
        self.restrict = restrict
        self.datatype = datatype
        self.name = name
        self.value = value
        if restrict:
            self.add_child(RestrictNode())
        self.add_child(DatatypeNode(datatype))
        self.add_child(IdNode(name))
        if value:
            self.add_child(value)

    def __repr__(self):
        restrict_str = " restrict" if self.restrict else ""
        return f"{self.datatype} {self.name} = {self.value}{restrict_str}"

class VarAssignNode(ASTNode): # for variable assignments
    def __init__(self, name, value):
        super().__init__("Variable Assignment")
        self.name = name
        self.value = value
        self.add_child(IdNode(name))
        self.add_child(value)

    def __repr__(self):
        return f"{self.name} = {self.value}"

class ClanDecNode(ASTNode): # for arrays
    def __init__(self, restrict, datatype, name, size, initial_values=None):
        super().__init__("Clan Declaration")
        self.restrict = restrict
        self.datatype = datatype
        self.name = name
        self.size = size
        self.initial_values = initial_values or []
        self.add_child(DatatypeNode(datatype))
        self.add_child(IdNode(name))
        if size:
            self.add_child(size)
        if initial_values:
            self.add_child(ClanLiteralNode(initial_values))

    def __repr__(self):
        if self.initial_values:
            return f"{self.datatype} {self.name}[{self.size}] = {self.initial_values}"
        else:
            return f"{self.datatype} {self.name}[{self.size}]"

class ClanLiteralNode(ASTNode): # for clan literals
    def __init__(self, values):
        super().__init__(f"Clan Literal: {{{', '.join(str(value) for value in values)}}}")
        self.values = values
        for value in values:
            self.add_child(value)

    def __repr__(self):
        return f"ClanLiteralNode({', '.join(repr(value) for value in self.values)})"
    
class ClanIndexNode(ASTNode): # for array indexing
    def __init__(self, index):
        super().__init__("Clan Index")
        self.index = index
        self.add_child(index)

    def __repr__(self):
        return f"{self.index}"

class ClanSizeNode(ASTNode): # for array size
    def __init__(self, size):
        super().__init__("Clan Size")
        self.size = size
        self.add_child(size)

    def __repr__(self):
        return f"ClanSizeNode({repr(self.size)})"
    
class ClanAccessNode(ASTNode): # for array access
    def __init__(self, name, index):
        super().__init__("Clan Access")
        self.name = name
        self.index = index
        self.add_child(IdNode(name))
        self.add_child(index)

class ClanIndexAssignNode(ASTNode): # for array index assignments
    def __init__(self, name, index, values):
        super().__init__("Clan Index Assign")
        self.name = name
        self.index = index
        self.values = values
        self.add_child(IdNode(name))
        self.add_child(index)
        for value in values:
            self.add_child(value)

    def __repr__(self):
        return f"{self.name}[{self.index}] = {self.values}"
    
class ClanAssignNode(ASTNode): # for assigning the whole array
    def __init__(self, name, values):
        super().__init__("Clan Assign")
        self.name = name
        self.values = values
        self.add_child(IdNode(name))
        self.add_child(ClanLiteralNode(values))

    def __repr__(self):
        return f"{self.name} = {self.values}"

class CurseDecNode(ASTNode): # for functions
    def __init__(self, datatype, name, parameters, body):
        super().__init__("Curse Declaration")
        self.datatype = datatype
        self.name = name
        self.parameters = parameters
        self.body = body
        self.add_child(DatatypeNode(datatype))
        self.add_child(IdNode(name))
        for param in parameters:
            self.add_child(param)
        self.add_child(body)

    def __repr__(self):
        return f"{self.datatype} {self.name}({self.parameters}) {self.body}"

class CurseDomainNode(ASTNode): # for function domain
    def __init__(self, body):
        super().__init__("Main Curse")
        self.body = body
        self.add_child(body)

    def __repr__(self):
        return f"{self.body}"

class ParamNode(ASTNode): # for function parameters
    def __init__(self, datatype, name):
        super().__init__("Parameter")
        self.datatype = datatype
        self.name = name
        self.add_child(DatatypeNode(datatype))
        self.add_child(IdNode(name))

class ArgNode(ASTNode): # for function arguments
    def __init__(self, value):
        super().__init__("Argument")
        self.value = value
        self.add_child(value)

class BodyNode(ASTNode): # for body of functions and vows and boogies and cycles and sustains and perform-sustains
    def __init__(self):
        super().__init__("Body")

class CurseCallNode(ASTNode): # for curse calls
    def __init__(self, name, arguments):
        super().__init__("Curse Call")
        self.name = name
        self.arguments = arguments
        self.add_child(IdNode(name))
        if arguments:
            args_node = ASTNode("Arguments")
            for arg in arguments:
                args_node.add_child(arg)
            self.add_child(args_node)

class StringNode(ASTNode): # for strings
    def __init__(self, value):
        super().__init__(f"String: {value}")
        self.value = value

class StringConcatNode(ASTNode): # for string concatenations
    def __init__(self, left, op, right):
        super().__init__("String Concatenation")
        self.left = left
        self.op = op.type
        self.right = right
        self.add_child(left)
        self.add_child(right)

    def __repr__(self):
        return f"{self.left} {self.op} {self.right}"

class InvokeNode(ASTNode): # for printing invoke("Hello, World!")
    def __init__(self, value):
        super().__init__("Invoke Statement")
        self.value = value
        self.add_child(value)

class CaptureNode(ASTNode): # for user input, capture(id)
    def __init__(self, name):
        super().__init__("Capture Statement")
        self.name = name
        self.add_child(name)

class CleaveNode(ASTNode): # for cleave statements, cleave(id, index1Start, index2End)
    def __init__(self, name, index1, index2):
        super().__init__("Cleave Statement")
        self.name = name
        self.index1 = index1
        self.index2 = index2
        self.add_child(name)
        self.add_child(index1)
        self.add_child(index2)

class DismantleNode(ASTNode): # for dismantle statements, dismantle(id, delimiter)
    def __init__(self, name, delimiter):
        super().__init__("Dismantle Statement")
        self.name = name
        self.delimiter = delimiter
        self.add_child(name)
        self.add_child(delimiter)

class LenNode(ASTNode): # for len statements, len(id)
    def __init__(self, name):
        super().__init__("Len Statement")
        self.name = name
        self.add_child(name)

class RecallNode(ASTNode): # for return statements
    def __init__(self, value):
        super().__init__("Recall Statement")
        self.value = value
        self.add_child(value)

class DismissNode(ASTNode): # for break statements
    def __init__(self):
        super().__init__("Dismiss")

class HopNode(ASTNode): # for continue statements
    def __init__(self):
        super().__init__("Hop")

class VowNode(ASTNode): # if-else (vow-else)
    def __init__(self, condition, body, else_vows=None, else_body=None):
        super().__init__("Vow Statement")
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
    def __init__(self, condition, body):
        super().__init__("Else Vow")
        self.condition = condition
        self.body = body
        self.add_child(condition)
        self.add_child(body)

class ElseNode(ASTNode):
    def __init__(self, body):
        super().__init__("Else")
        self.body = body
        self.add_child(body)

class BoogieNode(ASTNode): # switch-case (boogie)
    def __init__(self, expression, cases):
        super().__init__("Boogie Statement")
        self.expression = expression
        self.cases = cases
        if expression:
            self.add_child(expression)
        for case in cases:
            self.add_child(case)

    def __repr__(self):
        return f"BoogieNode({self.expression}, {self.cases})"

class WoogieTrueNode(ASTNode): # for cases/woogie of boogie true statements (switch true)
    def __init__(self, condition, body):
        super().__init__("Woogie True Statement")
        self.condition = condition
        self.body = body
        self.add_child(condition)
        self.add_child(body)

class WoogieNode(ASTNode): # for cases/woogie of standard boogie statements (switch)
    def __init__(self, condition, body):
        super().__init__("Woogie Statement")
        self.condition = condition
        self.body = body
        self.add_child(condition)
        self.add_child(body)

class DefaultCaseNode(ASTNode): # for default cases
    def __init__(self, body):
        super().__init__("Default Case")
        self.body = body
        self.add_child(body)

class SustainNode(ASTNode): # while loop (sustain)
    def __init__(self, condition, body):
        super().__init__("Sustain Statement")
        self.condition = condition
        self.body = body
        self.add_child(condition)
        self.add_child(body)

    def __repr__(self):
        return f"SustainNode({self.condition}, {self.body})"

class PerformSustainNode(ASTNode): # do-while loop (perform-sustain)
    def __init__(self, body, condition):
        super().__init__("PerformSustain Statement")
        self.body = body
        self.condition = condition
        self.add_child(body)
        self.add_child(condition)

    def __repr__(self):
        return f"PerformSustainNode({self.body}, {self.condition})"

class CycleNode(ASTNode): # for-loop (cycle)
    def __init__(self, cycle_condition, body):
        super().__init__("Cycle Statement")
        self.cycle_condition = cycle_condition
        self.body = body
        self.add_child(cycle_condition)
        self.add_child(body)

    def __repr__(self):
        return f"CycleNode({self.cycle_condition}, {self.body})"

class CycleConditionNode(ASTNode): # for-loop initialization, condition, and iteration
    def __init__(self, init, condition, iteration):
        super().__init__("Cycle Condition")
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
        print(f"Visiting {type(node).__name__}")
        self.visit_node(node, parent)
        for child in node.children:
            self.visit(child, node)

    def visit_node(self, node, parent):
        # This method can be overridden to perform specific actions on each node
        pass

class MyASTVisitor(ASTVisitor):
    def visit_NumNode(self, node, parent):
        print(f"Visiting NumNode with value: {node.value}")
        self.generic_visit(node, parent)

    def visit_StringNode(self, node, parent):
        print(f"Visiting StringNode with value: {node.value}")
        self.generic_visit(node, parent)

    def visit_BoolNode(self, node, parent):
        print(f"Visiting BoolNode with value: {node.value}")
        self.generic_visit(node, parent)

    def visit_NullNode(self, node, parent):
        print(f"Visiting NullNode")
        self.generic_visit(node, parent)

    def visit_ExponentNode(self, node, parent):
        print(f"Visiting ExponentNode")
        self.generic_visit(node, parent)

    def visit_BinOpNode(self, node, parent):
        print(f"Visiting BinOpNode with operator: {node.op}")
        self.generic_visit(node, parent)

    def visit_RelOpNode(self, node, parent):
        print(f"Visiting RelOpNode with operator: {node.op}")
        self.generic_visit(node, parent)

    def visit_LogOpNode(self, node, parent):
        print(f"Visiting LogOpNode with operator: {node.op}")
        self.generic_visit(node, parent)

    def visit_UnaryOpNode(self, node, parent):
        print(f"Visiting UnaryOpNode with operator: {node.op.op}")
        self.generic_visit(node, parent)

    def visit_VarNode(self, node, parent):
        print(f"Visiting VarNode with name: {node.name}")
        self.generic_visit(node, parent)

    def visit_VarDecNode(self, node, parent):
        print(f"Visiting VarDecNode with name: {node.name}")
        self.generic_visit(node, parent)

    def visit_VarAssignNode(self, node, parent):
        print(f"Visiting VarAssignNode with name: {node.name}")
        self.generic_visit(node, parent)

    def visit_ClanDecNode(self, node, parent):
        print(f"Visiting ClanDecNode with name: {node.name}")
        self.generic_visit(node, parent)

    def visit_ClanLiteralNode(self, node, parent):
        print(f"Visiting ClanLiteralNode with values: {node.values}")
        self.generic_visit(node, parent)

    def visit_ClanIndexNode(self, node, parent):
        print(f"Visiting ClanIndexNode with index: {node.index}")
        self.generic_visit(node, parent)

    def visit_ClanSizeNode(self, node, parent):
        print(f"Visiting ClanSizeNode with size: {node.size}")
        self.generic_visit(node, parent)

    def visit_ClanAccessNode(self, node, parent):
        print(f"Visiting ClanAccessNode with name: {node.name}")
        self.generic_visit(node, parent)

    def visit_ClanIndexAssignNode(self, node, parent):
        print(f"Visiting ClanIndexAssignNode with name: {node.name}")
        self.generic_visit(node, parent)

    def visit_ClanAssignNode(self, node, parent):
        print(f"Visiting ClanAssignNode with name: {node.name}")
        self.generic_visit(node, parent)

    def visit_CurseDecNode(self, node, parent):
        print(f"Visiting CurseDecNode with name: {node.name}")
        self.generic_visit(node, parent)

    def visit_CurseDomainNode(self, node, parent):
        print(f"Visiting CurseDomainNode")
        self.generic_visit(node, parent)

    def visit_ParamNode(self, node, parent):
        print(f"Visiting ParamNode with name: {node.name}")
        self.generic_visit(node, parent)

    def visit_ArgNode(self, node, parent):
        print(f"Visiting ArgNode")
        self.generic_visit(node, parent)

    def visit_BodyNode(self, node, parent):
        print(f"Visiting BodyNode")
        self.generic_visit(node, parent)

    def visit_CurseCallNode(self, node, parent):
        print(f"Visiting CurseCallNode with name: {node.name}")
        self.generic_visit(node, parent)

    def visit_StringConcatNode(self, node, parent):
        print(f"Visiting StringConcatNode")
        self.generic_visit(node, parent)

    def visit_InvokeNode(self, node, parent):
        print(f"Visiting InvokeNode")
        self.generic_visit(node, parent)

    def visit_CaptureNode(self, node, parent):
        print(f"Visiting CaptureNode with name: {node.name}")
        self.generic_visit(node, parent)

    def visit_CleaveNode(self, node, parent):
        print(f"Visiting CleaveNode with name: {node.name}")
        self.generic_visit(node, parent)

    def visit_DismantleNode(self, node, parent):
        print(f"Visiting DismantleNode with name: {node.name}")
        self.generic_visit(node, parent)

    def visit_LenNode(self, node, parent):
        print(f"Visiting LenNode with name: {node.name}")
        self.generic_visit(node, parent)

    def visit_RecallNode(self, node, parent):
        print(f"Visiting RecallNode")
        self.generic_visit(node, parent)

    def visit_DismissNode(self, node, parent):
        print(f"Visiting DismissNode")
        self.generic_visit(node, parent)

    def visit_HopNode(self, node, parent):
        print(f"Visiting HopNode")
        self.generic_visit(node, parent)

    def visit_VowNode(self, node, parent):
        print(f"Visiting VowNode")
        self.generic_visit(node, parent)

    def visit_ElseVow(self, node, parent):
        print(f"Visiting ElseVow")
        self.generic_visit(node, parent)

    def visit_ElseNode(self, node, parent):
        print(f"Visiting ElseNode")
        self.generic_visit(node, parent)

    def visit_BoogieNode(self, node, parent):
        print(f"Visiting BoogieNode")
        self.generic_visit(node, parent)

    def visit_WoogieTrueNode(self, node, parent):
        print(f"Visiting WoogieTrueNode")
        self.generic_visit(node, parent)

    def visit_WoogieNode(self, node, parent):
        print(f"Visiting WoogieNode")
        self.generic_visit(node, parent)

    def visit_DefaultCaseNode(self, node, parent):
        print(f"Visiting DefaultCaseNode")
        self.generic_visit(node, parent)

    def visit_SustainNode(self, node, parent):
        print(f"Visiting SustainNode")
        self.generic_visit(node, parent)

    def visit_PerformSustainNode(self, node, parent):
        print(f"Visiting PerformSustainNode")
        self.generic_visit(node, parent)

    def visit_CycleNode(self, node, parent):
        print(f"Visiting CycleNode")
        self.generic_visit(node, parent)

    def visit_CycleConditionNode(self, node, parent):
        print(f"Visiting CycleConditionNode")
        self.generic_visit(node, parent)

###################
# Symbol Table
###################

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def get(self, name):
        value = self.symbols.get(name, None)
        if value is None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

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
        self.reset()
        root = ASTNode("Program")
        while self.current_token is not None and self.current_token.type != 'EOF':
            if self.current_token is not None and self.current_token.type in ['int', 'float', 'string', 'bool', 'curse', 'restrict']:
                declaration = self.parseDeclaration()
                if declaration:
                    root.add_child(declaration)
            elif self.current_token is not None and self.current_token.type == 'id':
                assignment = self.parseIdCall()
                if assignment:
                    root.add_child(assignment)
            else: 
                self.advance()
        return root

    def parseFactor(self):
        tok = self.current_token
        print(f"parseFactor: Current token is {tok.type} with value {tok.value}")

        if tok.type in ('int_literal', 'float_literal'):
            self.advance()
            return NumNode(tok.value)
        elif tok.type == 'string_literal':
            self.advance()
            return StringNode(tok.value)
        elif tok.type == 'bool_literal':
            self.advance()
            return BoolNode(tok.value)
        elif tok.type == 'null_literal':
            self.advance()
            return NullNode(tok.value)
        elif tok.type == 'id':
            self.advance()
            if self.current_token.type in ('++', '--'):
                op = self.current_token
                self.advance()
                return UnaryOpNode(op, VarNode(tok.value), post=True)
            return VarNode(tok.value)
        elif tok.type == '(':
            self.advance()
            expr = self.parseExpr()
            if self.current_token.type == ')':
                self.advance()
                return expr
            else:
                raise InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected ')'")
        elif tok.type in ('+', '-'):
            self.advance()
            factor = self.parseFactor()
            return UnaryOpNode(tok, factor)
        elif tok.type in ('++', '--'):
            op = tok
            self.advance()
            factor = self.parseFactor()
            return UnaryOpNode(op, factor, pre=True)
        elif tok.type == '!':
            op = tok
            self.advance()
            factor = self.parseFactor()
            return UnaryOpNode(op, factor, pre=True)
        else:
            raise InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected int, float, bool, null, identifier, or '('")

    def parseExponent(self):
        left = self.parseFactor()
        while self.current_token.type == '**':
            op = self.current_token
            self.advance()
            right = self.parseFactor()
            left = ExponentNode(left, right)
        return left

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
        left = self.parseFactor()
        while self.current_token.type == '**':
            op = self.current_token
            self.advance()
            right = self.parseFactor()
            left = ExponentNode(left, right)
        return left

    def parseBinOp(self, func, ops, node_class):
        left = func()
        while self.current_token.type in ops:
            op = self.current_token
            self.advance()
            right = func()
            left = node_class(left, op, right)
        return left
    
    def parseIdCall(self):
        if self.current_token.type == 'id':
            name = self.current_token.value
            self.advance()
            if self.current_token.type in ['=', '+=', '-=', '*=', '/=', '%=']:
                op = self.current_token.type
                self.advance()
                if self.current_token.type == '{': # check later for previous node type
                    self.advance()
                    values = []
                    while self.current_token.type != '}':
                        values.append(self.parseExpr())
                        if self.current_token.type == ',':
                            self.advance()
                    self.advance()
                    return ClanAssignNode(name, values)
                elif self.current_token.type == 'id' and self.tokens[self.token_idx + 1].type == '(':
                    value = self.parseIdCall()
                    return VarAssignNode(name, value)
                elif self.current_token.type == 'id' and self.tokens[self.token_idx + 1].type == '[':
                    clan_id = self.current_token.value
                    self.advance()
                    self.advance() # self advanced two times to reach the actual index value
                    index = self.parseExpr()
                    index_node = ClanIndexNode(index)
                    value = ClanAccessNode(clan_id, index_node)
                    return VarAssignNode(name, value)
                elif self.current_token.type == 'cleave':
                    self.advance()
                    if self.current_token.type == '(':
                        self.advance()
                        cleave_id = IdNode(self.current_token.value) # check node types after advancing
                        self.advance() 
                        if self.current_token.type == ',':
                            self.advance()
                            index1 = self.parseExpr()
                            if self.current_token.type == ',':
                                self.advance()
                                index2 = self.parseExpr()
                                if self.current_token.type == ')':
                                    self.advance()
                                    return VarAssignNode(name, CleaveNode(cleave_id, index1, index2))
                elif self.current_token.type == 'dismantle':
                    self.advance()
                    if self.current_token.type == '(':
                        self.advance()
                        dismantle_id = IdNode(self.current_token.value) # check node types after advancing
                        self.advance()
                        if self.current_token.type == ',':
                            self.advance()
                            delimiter = StringNode(self.current_token.value)
                            self.advance()
                            if self.current_token.type == ')':
                                self.advance()
                                return VarAssignNode(name, DismantleNode(dismantle_id, delimiter))
                elif self.current_token.type == 'len':
                    self.advance()
                    if self.current_token.type == '(':
                        self.advance()  
                        len_id = IdNode(self.current_token.value)
                        self.advance()
                        if self.current_token.type == ')': # check if no more than 2 args
                            self.advance()
                            return VarAssignNode(name, LenNode(len_id))
                else:
                    value = self.parseExpr()
                    if op == '=':
                        return VarAssignNode(name, value)
                    else:
                        # Transform shorthand assignment into equivalent expression
                        bin_op = op[0]  # Get the operator part of the shorthand assignment
                        left = VarNode(name)
                        right = value
                        bin_op_node = BinOpNode(left, type('Token', (object,), {'type': bin_op})(), right)
                        return VarAssignNode(name, bin_op_node)
            elif self.current_token.type == '[':
                self.advance()
                index = self.parseExpr()
                index_node = ClanIndexNode(index)
                if self.current_token.type == ']':
                    self.advance()
                    if self.current_token.type == '=':
                        self.advance()
                        if self.current_token.type == '{':
                            self.advance()
                            values = []
                            while self.current_token.type != '}':
                                values.append(self.parseExpr())
                                if self.current_token.type == ',':
                                    self.advance()
                            return ClanIndexAssignNode(name, index_node, values)
            elif self.current_token.type == '(':
                self.advance()
                args = []
                while self.current_token.type != ')':
                    if self.current_token.type == 'string_literal':
                        args.append(StringNode(self.current_token.value))
                        self.advance()
                    elif self.current_token.type == 'id':
                        value = self.parseIdCall()
                        args.append(value)
                    else:
                        args.append(self.parseExpr())
                    if self.current_token.type == ',':
                        self.advance()
                self.advance()
                return CurseCallNode(name, args)
        return None
    

    def parseDeclaration(self):
        if self.current_token.type in ['int', 'float', 'string', 'bool']:
            datatype = self.current_token.type
            self.advance()

            if self.current_token.type == 'id':
                name = self.current_token.value
                self.advance()
                if self.current_token.type == '=':
                    self.advance()
                    if self.current_token.type == 'id' and self.peek().type == '(':
                        value = self.parseIdCall()
                        return VarDecNode(None, datatype, name, value)
                    elif self.current_token.type == 'id' and self.peek().type == '[':
                        clan_id = self.current_token.value
                        self.advance()
                        self.advance()
                        index = self.parseExpr()
                        index_node = ClanIndexNode(index)
                        value = ClanAccessNode(clan_id, index_node)
                        return VarDecNode(None, datatype, name, value)
                    elif self.current_token.type == 'cleave':
                        self.advance()
                        if self.current_token.type == '(':
                            self.advance()
                            cleave_id = IdNode(self.current_token.value) # check node types after advancing
                            self.advance()
                            if self.current_token.type == ',':
                                self.advance()
                                index1 = self.parseExpr()
                                if self.current_token.type == ',':
                                    self.advance()
                                    index2 = self.parseExpr()
                                    if self.current_token.type == ')':
                                        self.advance()
                                        return VarDecNode(None, datatype, name, CleaveNode(cleave_id, index1, index2))
                    elif self.current_token.type == 'dismantle':
                        self.advance()
                        if self.current_token.type == '(':
                            self.advance()
                            dismantle_id = IdNode(self.current_token.value)
                            self.advance()
                            if self.current_token.type == ',':
                                self.advance()
                                delimiter = StringNode(self.current_token.value)
                                self.advance()
                                if self.current_token.type == ')':
                                    self.advance()
                                    return VarDecNode(None, datatype, name, DismantleNode(dismantle_id, delimiter))
                    elif self.current_token.type == 'len':
                        self.advance()
                        if self.current_token.type == '(':
                            self.advance()
                            len_id = IdNode(self.current_token.value)
                            self.advance()
                            if self.current_token.type == ')':
                                self.advance()
                                return VarDecNode(None, datatype, name, LenNode(len_id))
                    else:
                        value = self.parseExpr()
                        return VarDecNode(None, datatype, name, value)
                elif self.current_token.type == '[':
                    self.advance()
                    size = self.parseExpr()
                    clan_size_node = ClanSizeNode(size)
                    if self.current_token.type == ']':
                        self.advance()
                        initial_values = []
                        if self.current_token.type == '=':
                            self.advance()
                            if self.current_token.type == '{':
                                self.advance()
                                while self.current_token.type != '}':
                                    initial_values.append(self.parseExpr())
                                    if self.current_token.type == ',':
                                        self.advance()
                                self.advance()
                        return ClanDecNode(None, datatype, name, clan_size_node, initial_values)
                elif self.current_token.type == '[...]':
                    self.advance()
                    initial_values = []
                    if self.current_token.type == '=':
                        self.advance()
                        if self.current_token.type == '{':
                            self.advance()
                            while self.current_token.type != '}':
                                initial_values.append(self.parseExpr())
                                if self.current_token.type == ',':
                                    self.advance()
                            self.advance()
                    return ClanDecNode(None, datatype, name, None, initial_values)
                else:
                    return VarDecNode(None, datatype, name, None)
        elif self.current_token.type == 'curse':
            self.advance()
            if self.current_token.type == 'id':
                name = self.current_token.value
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    parameters = []
                    while self.current_token.type != ')':
                        param_type = self.current_token.type
                        self.advance()
                        param_name = self.current_token.value
                        self.advance()
                        param_node = ParamNode(param_type, param_name)
                        parameters.append(param_node)
                        if self.current_token.type == ',':
                            self.advance()
                    self.advance()
                    if self.current_token.type == '{':
                        self.advance()
                        body = self.parseBody()
                        return CurseDecNode(None, name, parameters, body)
            elif self.current_token.type == 'domain':
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    if self.current_token.type == ')':
                        self.advance()
                        if self.current_token.type == '{':
                            self.advance()
                            body = self.parseBody()
                            return CurseDomainNode(body)
        elif self.current_token.type == 'restrict':
            self.advance()
            if self.current_token.type in ['int', 'float', 'string', 'bool']:
                datatype = self.current_token.type
                self.advance()
                if self.current_token.type == 'id':
                    name = self.current_token.value
                    self.advance()
                    if self.current_token.type == '=':
                        self.advance()
                        value = self.parseExpr()
                        return VarDecNode('restrict', datatype, name, value)
        return None
    
    def parseBody(self):
        body = BodyNode()
        while self.current_token.type != '}':
            if self.current_token.type in ['int', 'float', 'string', 'bool', 'curse', 'restrict']:
                declaration = self.parseDeclaration()
                if declaration:
                    body.add_child(declaration)
            elif self.current_token.type == 'id':
                assignment = self.parseIdCall()
                if assignment:
                    body.add_child(assignment)
            elif self.current_token.type == 'invoke':
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    value = self.parseInvokeArgument()
                    if self.current_token.type == ')':
                        self.advance()
                        body.add_child(InvokeNode(value))
            elif self.current_token.type == 'capture':
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    if self.current_token.type == 'id':
                        name = IdNode(self.current_token.value)
                        self.advance()
                        if self.current_token.type == ')':
                            self.advance()
                            body.add_child(CaptureNode(name))
            elif self.current_token.type == 'dismiss':
                self.advance()
                body.add_child(DismissNode())
            elif self.current_token.type == 'hop':
                self.advance()
                body.add_child(HopNode())
            elif self.current_token.type == 'recall': # check later for all possibilities
                self.advance()
                value = self.parseExpr()
                body.add_child(RecallNode(value))
            elif self.current_token.type == 'vow':
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    condition = self.parseExpr()
                    if self.current_token.type == ')':
                        self.advance()
                        if self.current_token.type == '{':
                            self.advance()
                            body_node = self.parseBody()
                            self.advance()  # advance past the closing brace '}'
                            else_vows = []
                            while self.current_token.type == 'else' and self.peek().type == 'vow':
                                self.advance()
                                self.advance()
                                if self.current_token.type == '(':
                                    self.advance()
                                    else_condition = self.parseExpr()
                                    if self.current_token.type == ')':
                                        self.advance()
                                        if self.current_token.type == '{':
                                            self.advance()
                                            else_body_node = self.parseBody()
                                            self.advance()  # Advance past the closing '}'
                                            else_vows.append(ElseVow(else_condition, else_body_node))
                            if self.current_token.type == 'else':
                                self.advance()
                                if self.current_token.type == '{':
                                    self.advance()
                                    else_body_node = self.parseBody()
                                    self.advance()  # Advance past the closing '}'
                                    body.add_child(VowNode(condition, body_node, else_vows, ElseNode(else_body_node)))
                            else:
                                body.add_child(VowNode(condition, body_node, else_vows))
            elif self.current_token.type == 'boogie':
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    expression = IdNode(self.current_token.value)
                    self.advance()
                    if self.current_token.type == ')':
                        self.advance()
                        if self.current_token.type == '{':
                            self.advance()
                            cases = []
                            while self.current_token.type != '}':
                                if self.current_token.type == 'woogie':
                                    self.advance()
                                    if self.current_token.type in ['int_literal', 'float_literal', 'id']:
                                        case_expr = self.parseExpr()
                                    elif self.current_token.type == 'string_literal':
                                        case_expr = StringNode(self.current_token.value)
                                        self.advance()
                                    elif self.current_token.type == '(':
                                        self.advance()
                                        if self.current_token.type == 'id':
                                            case_expr = self.parseIdCall()
                                    else:
                                        raise InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, "Expected int_literal, float_literal, or string_literal")
                                    if self.current_token.type == ':':
                                        self.advance()
                                        case_body = self.parseWoogieBody()
                                        cases.append(WoogieNode(case_expr, case_body))
                                elif self.current_token.type == 'default':
                                    self.advance()
                                    if self.current_token.type == ':':
                                        self.advance()
                                        default_body = self.parseWoogieBody()
                                        cases.append(DefaultCaseNode(default_body))
                            self.advance()
                            body.add_child(BoogieNode(expression, cases))
                elif self.current_token.type == '{':
                    self.advance()
                    cases = []
                    while self.current_token.type != '}':
                        if self.current_token.type == 'woogie':
                            self.advance()
                            case_expr = self.parseExpr()
                            if self.current_token.type == ':':
                                self.advance()
                                case_body = self.parseWoogieBody()
                                cases.append(WoogieTrueNode(case_expr, case_body))
                        elif self.current_token.type == 'default':
                            self.advance()
                            if self.current_token.type == ':':
                                self.advance()
                                default_body = self.parseWoogieBody()
                                cases.append(DefaultCaseNode(default_body))
                    self.advance()
                    body.add_child(BoogieNode(None, cases))
            elif self.current_token.type == 'cycle':
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    cycle_condition = self.parseCycleCondition()
                    if self.current_token.type == ')':
                        self.advance()
                        if self.current_token.type == '{':
                            self.advance()
                            cycle_body = self.parseBody()
                            self.advance()
                            body.add_child(CycleNode(cycle_condition, cycle_body)) 
            elif self.current_token.type == 'sustain':
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    condition = self.parseExpr()
                    if self.current_token.type == ')':
                        self.advance()
                        if self.current_token.type == '{':
                            self.advance()
                            sustain_body = self.parseBody()
                            self.advance()
                            body.add_child(SustainNode(condition, sustain_body))
            elif self.current_token.type == 'perform':
                print("Hey i reached 2311")
                self.advance()
                if self.current_token.type == '{':
                    self.advance()
                    perform_body = self.parseBody()
                    self.advance()
                    if self.current_token.type == 'sustain':
                        self.advance()
                        if self.current_token.type == '(':
                            self.advance()
                            condition = self.parseExpr()
                            if self.current_token.type == ')':
                                self.advance()
                                if self.current_token.type == ';':
                                    self.advance()
                                    body.add_child(PerformSustainNode(perform_body, condition))
            else:
                self.advance()
        return body
    
    def parseCycleCondition(self):
        if self.current_token.type in ['int', 'float', 'string', 'bool']:
            init = self.parseDeclaration()
        elif self.current_token.type == 'id':
            init = self.parseIdCall()
        else:
            raise InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, "Expected variable declaration or reassignment")
        if self.current_token.type == ';':
            self.advance()
            condition = self.parseExpr()
            if self.current_token.type == ';':
                self.advance()
                iteration = self.parseExpr()
                return CycleConditionNode(init, condition, iteration)
        else:
            print(f"Encountered: {self.current_token.type}") 
            raise InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, "Expected ';'")

    def parseWoogieBody(self):
        body = BodyNode()
        while self.current_token.type not in ['woogie', 'default', '}']:
            if self.current_token.type in ['int', 'float', 'string', 'bool', 'curse', 'restrict']:
                declaration = self.parseDeclaration()
                if declaration:
                    body.add_child(declaration)
            elif self.current_token.type == 'id':
                assignment = self.parseIdCall()
                if assignment:
                    body.add_child(assignment)
            elif self.current_token.type == 'invoke':
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    value = self.parseInvokeArgument()
                    if self.current_token.type == ')':
                        self.advance()
                        body.add_child(InvokeNode(value))
            elif self.current_token.type == 'capture':
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    if self.current_token.type == 'id':
                        name = IdNode(self.current_token.value)
                        self.advance()
                        if self.current_token.type == ')':
                            self.advance()
                            body.add_child(CaptureNode(name))
            elif self.current_token.type == 'dismiss':
                self.advance()
                body.add_child(DismissNode())
            elif self.current_token.type == 'hop':
                self.advance()
                body.add_child(HopNode())
            elif self.current_token.type == 'recall': # check later for all possibilities
                self.advance()
                value = self.parseExpr()
                body.add_child(RecallNode(value))
            elif self.current_token.type == 'vow':
                self.advance()
                if self.current_token.type == '(':
                    self.advance()
                    condition = self.parseExpr()
                    if self.current_token.type == ')':
                        self.advance()
                        if self.current_token.type == '{':
                            self.advance()
                            body_node = self.parseBody()
                            self.advance()  # advance past the closing brace '}'
                            else_vows = []
                            while self.current_token.type == 'else' and self.peek().type == 'vow':
                                self.advance()
                                self.advance()
                                if self.current_token.type == '(':
                                    self.advance()
                                    else_condition = self.parseExpr()
                                    if self.current_token.type == ')':
                                        self.advance()
                                        if self.current_token.type == '{':
                                            self.advance()
                                            else_body_node = self.parseBody()
                                            self.advance()  # Advance past the closing '}'
                                            else_vows.append(ElseVow(else_condition, else_body_node))
                            if self.current_token.type == 'else':
                                self.advance()
                                if self.current_token.type == '{':
                                    self.advance()
                                    else_body_node = self.parseBody()
                                    self.advance()  # Advance past the closing '}'
                                    body.add_child(VowNode(condition, body_node, else_vows, ElseNode(else_body_node)))
                            else:
                                body.add_child(VowNode(condition, body_node, else_vows))
            else:
                self.advance()
        return body

    def parseInvokeArgument(self):
        if self.current_token.type == 'string_literal':
            return self.parseString()
        else:
            return self.parseExpr()

    def parseString(self):
        left = StringNode(self.current_token.value)
        self.advance()
        while self.current_token.type == '+':
            op = self.current_token
            self.advance()
            if self.current_token.type == 'string_literal':
                right = StringNode(self.current_token.value)
                self.advance()
            else:
                right = self.parseFactor()
            left = StringConcatNode(left, op, right)
        return left


def semantic_run(tokens):
    parser = Parser(tokens)
    ast = parser.build_ast()
    if ast:
        ast.print_tree()
    else:
        print("No AST built")
        return "Failure from Semantic Analyzer", None
    return "Successful from Semantic Analyzer", ast