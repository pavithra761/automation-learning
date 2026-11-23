import asyncio

import server


async def main():
    tools = await server.mcp.list_tools()
    for tool in tools:
        print("tool:", tool.name)

    result = await server.mcp.call_tool("celsius_to_fahrenheit", {"celsius": 20})
    print(result.content[0].text)

    result = await server.mcp.call_tool(
        "get_current_temperature", {"latitude": 40.7, "longitude": -74.0}
    )
    print(result.content[0].text)


asyncio.run(main())