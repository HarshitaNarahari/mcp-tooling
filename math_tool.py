from mcp.server.fastmcp import FastMCP
import ast
import operator as op

# Create the MCP server
mcp = FastMCP("math_tool")

# Operators we’ll allow (no unsafe stuff)
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

#evaluate math expressions using these cases
def evaluate_expression(expr: str):
    def eval_node(node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            return operators[type(node.op)](eval_node(node.left), eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return operators[type(node.op)](eval_node(node.operand))
        else:
            raise ValueError("That expression uses something we don’t support.")

    try:
        tree = ast.parse(expr, mode="eval").body
        return eval_node(tree)
    except Exception as e:
        raise ValueError(f"Couldn’t evaluate expression: {e}")


# quick math tool
@mcp.tool()
def calculate(expression: str) -> dict:
    try:
        result = evaluate_expression(expression)
        return {"input": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("Starting math MCP tool...")
    mcp.run()
