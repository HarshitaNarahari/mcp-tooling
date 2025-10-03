from mcp.server.fastmcp import FastMCP
import ast
import operator as op

mcp = FastMCP("math_tool")

# --- safe evaluation helper ---
# Supported operators
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

def safe_eval(expr):
    def eval_node(node):
        if isinstance(node, ast.Num):      # number
            return node.n
        elif isinstance(node, ast.BinOp):  # binary operation
            return operators[type(node.op)](eval_node(node.left), eval_node(node.right))
        elif isinstance(node, ast.UnaryOp): # unary (e.g., -3)
            return operators[type(node.op)](eval_node(node.operand))
        else:
            raise ValueError("Unsupported expression")
    tree = ast.parse(expr, mode="eval").body
    return eval_node(tree)

# --- MCP tool ---
@mcp.tool()
def calculate(expression: str) -> dict:
    """Evaluate a basic math expression safely."""
    try:
        result = safe_eval(expression)
        return {"input": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()
