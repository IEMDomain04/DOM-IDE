from semantic import (
    NumNode, DatatypeNode, StringNode, BoolNode, NullNode, ExponentNode, BinOpNode, 
    RelOpNode, LogOpNode, UnaryOpNode, IdNode, VarDecNode, VarAssignNode, ClanDecNode, 
    ClanLiteralNode, ClanAccessNode, ClanIndexAssignNode, 
    CurseDecNode, CurseDomainNode, ParamNode, BodyNode, CurseCallNode, 
    InvokeNode, CaptureNode, CleaveNode, DismantleNode, LenNode, RecallNode, DismissNode, 
    HopNode, VowNode, ElseVow, ElseNode, BoogieNode, WoogieTrueNode, WoogieNode, 
    DefaultCaseNode, SustainNode, PerformSustainNode, CycleNode, CycleConditionNode
)

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
        self.errors = []
        self.unresolved_cases = []  # List to keep track of unresolved cases

    def visit_DatatypeNode(self, node, parent):
        print(f"Visiting DatatypeNode with type: {node.datatype}")
        self.visit_children(node)
        print(f"Exiting DatatypeNode")

    def visit_StringNode(self, node, parent):
        print(f"Visiting StringNode with value: {node.value}")
        return node.value
        print(f"Exiting StringNode")

    def visit_BoolNode(self, node, parent):
        print(f"Visiting BoolNode with value: {node.value}")
        self.visit_children(node)
        print(f"Exiting BoolNode")

    def visit_NullNode(self, node, parent):
        print(f"Visiting NullNode")
        self.visit_children(node)
        print(f"Exiting NullNode")

    def visit_NumNode(self, node, parent):
        print(f"Visiting NumNode with value: {node.value}")
        ancestor = parent
        while not isinstance(ancestor, InvokeNode):
            if hasattr(ancestor, 'parent'):
                ancestor = ancestor.parent
            else: break

        if isinstance(ancestor, InvokeNode) and not isinstance(parent, ExponentNode):
            self.output.append(str(node.value))
        print(f"Exiting NumNode")

    def visit_ExponentNode(self, node, parent):
        print(f"Visiting ExponentNode")
        ancestor = parent
        while not isinstance(ancestor, InvokeNode):
            if hasattr(ancestor, 'parent'):
                ancestor = ancestor.parent
            else: break
        if isinstance(ancestor, InvokeNode):
            self.output.append("(")
            self.output.append(str(node.left.value))
            self.output.append("**")
            self.output.append(str(node.right.value))
            self.output.append(")")
        self.visit_children(node)
        print(f"Exiting ExponentNode")

    def visit_BinOpNode(self, node, parent):
        print(f"Visiting BinOpNode with operator: {node.op}")
        self.visit_children(node)
        print(f"Exiting BinOpNode")

    def visit_RelOpNode(self, node, parent):
        print(f"Visiting RelOpNode with operator: {node.op}")
        ancestor = parent
        while not isinstance(ancestor, InvokeNode):
            if hasattr(ancestor, 'parent'):
                ancestor = ancestor.parent
            else: break
        if isinstance(ancestor, InvokeNode):
            self.output.append("(")
            self.visit(node.left, node)
            self.output.append(node.op)
            self.visit(node.right, node)
            self.output.append(")")
        else:
            self.visit_children(node)
        print(f"Exiting RelOpNode")

    def visit_LogOpNode(self, node, parent):
        print(f"Visiting LogOpNode with operator: {node.op}")
        ancestor = parent
        while not isinstance(ancestor, InvokeNode):
            if hasattr(ancestor, 'parent'):
                ancestor = ancestor.parent
            else: break
        if isinstance(ancestor, InvokeNode):
            self.output.append("(")
            self.visit(node.left, node)
            self.output.append(node.op)
            self.visit(node.right, node)
            self.output.append(")")
        else: self.visit_children(node)
        print(f"Exiting LogOpNode")

    def visit_UnaryOpNode(self, node, parent):
        print(f"Visiting UnaryOpNode with operator: {node.op.op}")
        if node.pre is True:
            print("HHEYHEYHEY")
            self.output.append(node.op.op)
            self.visit(node.expr, node)
        if node.post is True:
            self.visit(node.expr, node)
            self.output.append(node.op.op)
        print(f"Exiting UnaryOpNode")

    def visit_IdNode(self, node, parent):
        print(f"Visiting IdNode with name: {node.name}")
        print(f"Exiting IdNode")

    def visit_VarDecNode(self, node, parent):
        print(f"Visiting VarDecNode with type: {node.datatype}")
        self.visit_children(node)
        print(f"Exiting VarDecNode")

    def visit_VarAssignNode(self, node, parent):
        print(f"Visiting VarAssignNode with name: {node.name}")
        self.visit_children(node)
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
                if isinstance(self.evaluate_node(list_item), str):
                    value += self.evaluate_node(list_item)
                else: value += str(self.evaluate_node(list_item))
        else: value = self.evaluate_node(node.value)
        if value is None:
            value = node.value
        print(f'\n\n{value}\n\n')
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
            return node.value
        elif isinstance (node, StringNode):
            print("Heyoo")
            return node.value
        elif isinstance(node, BoolNode):
            return node.value
        elif isinstance(node, NullNode):
            return 'Null'
        elif isinstance(node, BinOpNode):
            left_value = self.evaluate_node(node.left)
            right_value = self.evaluate_node(node.right)
            if isinstance(left_value, str):
                right_value = str(right_value)
            if isinstance(right_value, str):
                left_value = str(left_value)
            if left_value is not None and right_value is not None:
                if node.op == '+':
                    return left_value + right_value
                elif node.op == '-':
                    return left_value - right_value
                elif node.op == '*':
                    return left_value * right_value
                elif node.op == '/':
                    return left_value / right_value
                elif node.op == '%':
                    return left_value % right_value
                elif node.op == '==':
                    return left_value == right_value
                elif node.op == '!=':
                    return left_value != right_value
                elif node.op == '<':
                    return left_value < right_value
                elif node.op == '>':
                    return left_value > right_value
                elif node.op == '<=':
                    return left_value <= right_value
                elif node.op == '>=':
                    return left_value >= right_value
                elif node.op == '&&':
                    return left_value and right_value
                elif node.op == '||':
                    return left_value or right_value
        elif isinstance(node, str):
            return node
        return None
        
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
    if runner.errors:
        return None, runner.errors
    
    return runner.output, None