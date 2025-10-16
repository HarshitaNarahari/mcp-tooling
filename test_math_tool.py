import asyncio
from fastmcp.client import Client
from mcp.server.fastmcp import FastMCP

# Import the MCP server instance from your tool file
from math_tool import mcp

async def test():
    async with Client(mcp) as client:
        tools = await client.list_tools()
        print("Available tools:", [t.name for t in tools])

        result = await client.call_tool("calculate", {"expression": "3 * (2 + 4) - 5"})
        print("Result:", result)

if __name__ == "__main__":
    asyncio.run(test())


