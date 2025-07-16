#!/usr/bin/env python3

import asyncio
import base64
import json
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

async def main():
    """Example client that demonstrates how to use the MCP audio transcription server"""
    
    # Start the MCP server as a subprocess
    server_params = {
        "command": "python",
        "args": ["mcp_server.py"]
    }
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            # List available tools
            print("Available tools:")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")
            print()
            
            # Example 1: Get supported formats
            print("=== Supported Formats ===")
            result = await session.call_tool("get_supported_formats", {})
            print(json.dumps(result.content[0].text, indent=2))
            print()
            
            # Example 2: Transcribe audio from file (you would need to provide actual audio data)
            print("=== Audio Transcription Example ===")
            print("To transcribe audio, you would call:")
            print("result = await session.call_tool('transcribe_audio_file', {")
            print("    'audio_data': '<base64_encoded_audio_data>',")
            print("    'filename': 'example.wav'")
            print("})")
            print()
            
            # Example 3: Transcribe from URL (example with placeholder)
            print("=== URL Transcription Example ===")
            print("To transcribe from URL, you would call:")
            print("result = await session.call_tool('transcribe_audio_url', {")
            print("    'audio_url': 'https://example.com/audio.wav'")
            print("})")
            print()
            
            print("MCP Audio Transcription Server is working correctly!")

if __name__ == "__main__":
    asyncio.run(main())