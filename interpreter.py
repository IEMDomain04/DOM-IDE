from semantic import (
    NumNode, DatatypeNode, StringNode, BoolNode, NullNode, ExponentNode, BinOpNode, 
    RelOpNode, LogOpNode, UnaryOpNode, IdNode, VarDecNode, VarAssignNode, ClanDecNode, 
    ClanLiteralNode, ClanAccessNode, ClanIndexAssignNode, 
    CurseDecNode, CurseDomainNode, ParamNode, BodyNode, CurseCallNode, 
    InvokeNode, CaptureNode, CleaveNode, DismantleNode, LenNode, RecallNode, DismissNode, 
    HopNode, VowNode, ElseVow, ElseNode, BoogieNode, WoogieTrueNode, WoogieNode, 
    DefaultCaseNode, SustainNode, PerformSustainNode, CycleNode, CycleConditionNode
)

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

class RTError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)

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

class DOMInterpreter: 
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

class CodeRunner(DOMInterpreter):
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.output = []
        self.error = None
        self.unresolved_cases = []  # List to keep track of unresolved cases

    def visit_DatatypeNode(self, node, parent):
        print(f"Visiting DatatypeNode with type: {node.datatype}")
        self.visit_children(node)
        print(f"Exiting DatatypeNode")

    def visit_StringNode(self, node, parent):
        print(f"Visiting StringNode with value: {node.value}")
        return node.value

    def visit_BoolNode(self, node, parent):
        print(f"Visiting BoolNode with value: {node.value}")
        self.visit_children(node)
        print(f"Exiting BoolNode")

    def visit_NullNode(self, node, parent):
        print(f"Visiting NullNode")
        self.visit_children(node)
        return None

    def visit_NumNode(self, node, parent):
        print(f"Visiting NumNode with value: {node.value}")
        return node.value
        print(f"Exiting NumNode")

    def visit_ExponentNode(self, node, parent):
        print(f"Exiting ExponentNode")

    def visit_BinOpNode(self, node, parent):
        print(f"Visiting BinOpNode with operator: {node.op}")
        self.visit_children(node)
        print(f"Exiting BinOpNode")

    def visit_RelOpNode(self, node, parent):
        print(f"Visiting RelOpNode with operator: {node.op}")
        print(f"Exiting RelOpNode")

    def visit_LogOpNode(self, node, parent):
        print(f"Visiting LogOpNode with operator: {node.op}")
        print(f"Exiting LogOpNode")

    def visit_UnaryOpNode(self, node, parent):
        print(f"Visiting UnaryOpNode with operator: {node.op.op}")
        if node.pre is True:
            self.output.append(node.op.op)
            self.visit(node.expr, node)
        if node.post is True:
            self.visit(node.expr, node)
            self.output.append(node.op.op)
        print(f"Exiting UnaryOpNode")

    def visit_IdNode(self, node, parent):
        print(f"Visiting IdNode with name: {node.name}")
        # Check if the variable is declared in the symbol table
        symbol = self.symbol_table.get(node.name);
        if self.symbol_table.get(node.name) is None:
            self.error = SemanticError(node.pos_start, node.pos_end, f"Variable '{node.name}' is not declared")
            return None
        if isinstance(symbol, VarDecNode):
            # If the variable is declared, return its value
            print(f"IdNode '{node.name}' found in symbol table")
            return symbol.value
        return None

    def visit_VarDecNode(self, node, parent):
        print(f"Visiting VarDecNode with type: {node.datatype}")
        # true parent
        true_parent = parent
        while true_parent and not isinstance(true_parent, (CurseDomainNode)):
            true_parent = true_parent.parent

        if true_parent is None or not isinstance(true_parent, CurseDomainNode):
            pass
        else:
            var_dec_node = self.symbol_table.get(node.name)
            if not var_dec_node:
                self.symbol_table.set(node.name, node)  # Store the VarDecNode object itself
                var_dec_node = self.symbol_table.get(node.name)
            else: 
                self.error = SemanticError(node.pos_start, node.pos_end, f"Variable '{node.name}' already declared")
            
            value, error = self.evaluate_node(var_dec_node.value)
            if error:
                self.error = error
                return

            if var_dec_node.datatype == 'int' and isinstance(value, float):
                value = int(value)  # Convert float to integer
                print(f"Converted float value to integer for variable '{node.name}'")
            # Update the value in the variable declaration node
            var_dec_node.value = value
            print(f'Value: {var_dec_node.value}')
            print(f"Updated value '{value}' for variable '{node.name}' in symbol table")

        self.visit_children(node)
        print(f"Exiting VarDecNode")

    def visit_VarAssignNode(self, node, parent):
        print(f"Visiting VarAssignNode with name: {node.name}")
        value, error = self.evaluate_node(node.value)
        if error:
            self.error = error
            return
        # Retrieve the variable declaration node from the symbol table
        var_dec_node = self.symbol_table.get(node.name)
        if var_dec_node is None:
            self.error = SemanticError(node.pos_start, node.pos_end, f"Variable '{node.name}' is not declared")
            return
        # Check if the variable is of integer type
        if var_dec_node.datatype == 'int' and isinstance(value, float):
            value = int(value)  # Convert float to integer
            print(f"Converted float value to integer for variable '{node.name}'")
        # Update the value in the variable declaration node
        var_dec_node.value = value
        print(f"Updated value '{value}' for variable '{node.name}' in symbol table")
        print(f"Exiting VarAssignNode")

    def visit_ClanDecNode(self, node, parent):
        print(f"Visiting ClanDecNode with name: {node.name}")
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
        self.visit_children(node)
        print(f"Exiting ClanAccessNode")

    def visit_ClanIndexAssignNode(self, node, parent):
        print(f"Visiting ClanIndexAssignNode with name: {node.name}")
        self.visit_children(node)
        print(f"Exiting ClanIndexAssignNode")

    def visit_CurseDecNode(self, node, parent):
        print(f"Visiting CurseDecNode with name: {node.name}")
        self.visit_children(node)
        print(f"Exiting CurseDecNode")

    def visit_CurseDomainNode(self, node, parent):
        print(f"Visiting CurseDomainNode")
        self.visit_children(node)
        print(f"Exiting CurseDomainNode")

    def visit_ParamNode(self, node, parent):
        print(f"Visiting ParamNode with name: {node.name}")
        self.visit_children(node)
        print(f"Exiting ParamNode")

    def visit_BodyNode(self, node, parent):
        print(f"Visiting BodyNode")
        self.visit_children(node)
        print(f"Exiting BodyNode")

    def visit_CurseCallNode(self, node, parent):
        print(f"Visiting CurseCallNode with name: {node.name}")
        self.visit_children(node)
        print(f"Exiting CurseCallNode")

    def visit_StringConcatNode(self, node, parent):
        print(f"Visiting StringConcatNode")
        self.visit_children(node)
        print(f"Exiting StringConcatNode")

    def visit_InvokeNode(self, node, parent):
        print(f"Visiting InvokeNode")
        value = ''
        if isinstance(node.value, list):
            for list_item in node.value:
                temp, error = self.evaluate_node(list_item)
                if error:
                        self.error = error
                        break
                if isinstance(temp, str):
                    value += temp
                else: 
                    value += str(temp)
        else: 
            value, error = self.evaluate_node(node.value)
            if value is None:
                value = node.value
            if error:
                self.error = error
                return

        if hasattr(value, 'to_string'):
            self.output.append(value.to_string())
        else:
            self.output.append(value)
            
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
        self.visit_children(node)
        print(f"Exiting RecallNode")

    def visit_DismissNode(self, node, parent):
        print(f"Visiting DismissNode")
        self.visit_children(node)
        print(f"Exiting DismissNode")

    def visit_HopNode(self, node, parent):
        print(f"Visiting HopNode")
        self.visit_children(node)
        print(f"Exiting HopNode")

    def visit_VowNode(self, node, parent):
        print(f"Visiting VowNode")
        self.visit_children(node)
        print(f"Exiting VowNode")

    def visit_ElseVow(self, node, parent):
        print(f"Visiting ElseVow")
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
            pass
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
                return curse_node.datatype
            return 'unknown'
        else:
            return 'unknown'
        
    def evaluate_node(self, node):
        if isinstance(node, NumNode):
            return node.value, None
        elif isinstance (node, StringNode):
            return node.value, None
        elif isinstance(node, BoolNode):
            return node.value, None
        elif isinstance(node, NullNode):
            return 'Null', None
        
        elif isinstance(node, IdNode):
            symbol = self.symbol_table.get(node.name)
            if symbol is None:
                return None, SemanticError(node.pos_start, node.pos_end, f"Variable '{node.name}' is not declared")
            if isinstance(symbol, VarDecNode):
                value, error = self.evaluate_node(symbol.value)
                if error:
                    return None, error
            return value, None

        elif isinstance(node, (BinOpNode, RelOpNode, LogOpNode)):
            print("HEYHEYYOUOU")
            left_value, error = self.evaluate_node(node.left)
            if error:
                return None, error
            right_value, error = self.evaluate_node(node.right)
            if error:
                return None, error
            
            if isinstance(left_value, NumNode):
                left_value = left_value.value
            if isinstance(right_value, NumNode):
                right_value = right_value.value
            
            try:
                if left_value is not None and right_value is not None:
                    if node.op == '+':
                        return left_value + right_value, None
                    elif node.op == '-':
                        return left_value - right_value, None
                    elif node.op == '*':
                        return left_value * right_value, None
                    elif node.op == '/':
                        return left_value / right_value, None
                    elif node.op == '%':
                        return left_value % right_value, None
                    elif node.op == '==':
                        return left_value == right_value, None
                    elif node.op == '!=':
                        return left_value != right_value, None
                    elif node.op == '<':
                        return left_value < right_value, None
                    elif node.op == '>':
                        return left_value > right_value, None
                    elif node.op == '<=':
                        return left_value <= right_value, None
                    elif node.op == '>=':
                        return left_value >= right_value, None
                    elif node.op == '&&':
                        return left_value and right_value, None
                    elif node.op == '||':
                        return left_value or right_value, None
            except ZeroDivisionError:
                return None, RTError(node.pos_start, node.pos_end, f'Division by Zero')
            except: 
                return None, RTError(node.pos_start, node.pos_end, f'Invalid operation: {node.op}')
        elif isinstance(node, (str, int, float)):
            return node, None
        return None, None
        
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

        
def interpreter_run(ast, symbol_table):
    runner = CodeRunner(symbol_table)
    runner.visit(ast)
    # runner.resolve_unresolved()
    
    print(f"Interpreter output: {runner.output}")
    if runner.error:
        return None, runner.error
    
    return runner.output, None