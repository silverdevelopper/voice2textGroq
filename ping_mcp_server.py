#!/usr/bin/env python3

import asyncio
import json
import subprocess
import sys
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

async def ping_mcp_server():
    """Test/ping the MCP server to verify it's working"""
    
    server_params = ["uv", "run", "python", "mcp_server.py"]
    
    try:
        print("🔍 Connecting to MCP server...")
        async with stdio_client(command="uv", args=["run", "python", "mcp_server.py"]) as (read, write):
            async with ClientSession(read, write) as session:
                print("✅ Successfully connected to MCP server!")
                
                # Initialize the session
                await session.initialize()
                print("✅ Session initialized successfully!")
                
                # Test: List available tools
                print("\n📋 Available tools:")
                try:
                    tools = await session.list_tools()
                    for tool in tools.tools:
                        print(f"  • {tool.name}: {tool.description}")
                except Exception as e:
                    print(f"  ❌ Error listing tools: {e}")
                
                # Test: Get supported formats
                print("\n🧪 Testing get_supported_formats tool...")
                try:
                    result = await session.call_tool("get_supported_formats", {})
                    data = json.loads(result.content[0].text)
                    print(f"  ✅ Supported formats: {', '.join(data['supported_formats'])}")
                    print(f"  ✅ Available models: {', '.join(data['available_models'])}")
                except Exception as e:
                    print(f"  ❌ Error testing tool: {e}")
                
                # Test: Server info
                print("\n📊 Server information:")
                try:
                    server_info = await session.get_server_info()
                    print(f"  • Name: {server_info.name}")
                    print(f"  • Version: {server_info.version}")
                except Exception as e:
                    print(f"  ❌ Error getting server info: {e}")
                
                print("\n🎉 MCP server is working correctly!")
                
    except Exception as e:
        print(f"❌ Failed to connect to MCP server: {e}")
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure the server is in the correct directory")
        print("2. Check that all dependencies are installed (uv sync)")
        print("3. Verify your GROQ_API_KEY is set")
        print("4. Try running: uv run python mcp_server.py")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(ping_mcp_server())
    sys.exit(0 if success else 1)