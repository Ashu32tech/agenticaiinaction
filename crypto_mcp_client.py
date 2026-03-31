#!/usr/bin/env python3
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["D:/aiInAction/agenticaiinaction/crypto_mcp_server.py"]
    )

    print("Starting MCP server...")

    async with stdio_client(server_params) as (read, write):
        print("Connected to server")

        async with ClientSession(read, write) as session:
            print("Initializing session...")
            await session.initialize()

            print("Calling tool...")
            result = await session.call_tool(
                "get_cryptocurrency_price",
                {"crypto": "dogecoin"}
            )

            print("Result:", result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())