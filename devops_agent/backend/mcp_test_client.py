from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
import asyncio


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()
            print("✅ Connected")

            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])

            res = await session.call_tool(
                "get_pods",
                {"namespace": "micro-demo"}
            )
            print("Pods:", res)


if __name__ == "__main__":
    asyncio.run(main())