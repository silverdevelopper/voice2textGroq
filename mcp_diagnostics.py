#!/usr/bin/env python3

import subprocess
import json
import sys
import os

def check_mcp_server_status():
    """Comprehensive MCP server diagnostics"""
    
    print("🔧 MCP Server Diagnostics")
    print("=" * 50)
    
    # Check 1: Environment
    print("1. Environment Check:")
    print(f"   • Python: {sys.version}")
    print(f"   • Working Directory: {os.getcwd()}")
    print(f"   • GROQ_API_KEY: {'✅ Set' if os.getenv('GROQ_API_KEY') else '❌ Not set'}")
    
    # Check 2: Dependencies
    print("\n2. Dependencies Check:")
    try:
        import mcp
        print(f"   • MCP: ✅ Available")
    except ImportError as e:
        print(f"   • MCP: ❌ {e}")
        return False
    
    try:
        import groq
        print(f"   • Groq: ✅ Available")
    except ImportError as e:
        print(f"   • Groq: ❌ {e}")
        return False
    
    # Check 3: Server Module
    print("\n3. Server Module Check:")
    try:
        import mcp_server
        print("   • mcp_server.py: ✅ Imports successfully")
        
        # Check tools
        tools = [
            'get_supported_formats',
            'transcribe_audio_file', 
            'transcribe_audio_url',
            'format_transcription'
        ]
        
        for tool in tools:
            if hasattr(mcp_server, tool):
                print(f"   • {tool}: ✅ Available")
            else:
                print(f"   • {tool}: ❌ Missing")
                
    except Exception as e:
        print(f"   • mcp_server.py: ❌ {e}")
        return False
    
    # Check 4: Server Startup
    print("\n4. Server Startup Test:")
    try:
        process = subprocess.Popen(
            ["uv", "run", "python", "mcp_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True
        )
        
        # Test JSON-RPC communication
        init_msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "diagnostic", "version": "1.0"}
            }
        }
        
        process.stdin.write(json.dumps(init_msg) + "\n")
        process.stdin.flush()
        
        # Read response
        response = process.stdout.readline()
        if response:
            try:
                data = json.loads(response)
                if "result" in data:
                    print("   • Server initialization: ✅ Success")
                    server_info = data["result"].get("serverInfo", {})
                    print(f"   • Server name: {server_info.get('name', 'Unknown')}")
                    print(f"   • Server version: {server_info.get('version', 'Unknown')}")
                else:
                    print("   • Server initialization: ⚠️ Unexpected response")
            except json.JSONDecodeError:
                print("   • Server initialization: ⚠️ Invalid JSON response")
        else:
            print("   • Server initialization: ❌ No response")
        
        # Test tools listing
        tools_msg = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        process.stdin.write(json.dumps(tools_msg) + "\n")
        process.stdin.flush()
        
        response = process.stdout.readline()
        if response:
            try:
                data = json.loads(response)
                if "result" in data and "tools" in data["result"]:
                    tools = data["result"]["tools"]
                    print(f"   • Available tools: ✅ {len(tools)} tools")
                    for tool in tools:
                        print(f"     - {tool['name']}")
                else:
                    print("   • Available tools: ⚠️ No tools listed")
            except json.JSONDecodeError:
                print("   • Available tools: ⚠️ Invalid JSON response")
        
        process.terminate()
        process.wait()
        
    except Exception as e:
        print(f"   • Server startup: ❌ {e}")
        return False
    
    # Check 5: Claude Desktop Config
    print("\n5. Claude Desktop Configuration:")
    config_path = os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json")
    if os.path.exists(config_path):
        print(f"   • Config file: ✅ Found at {config_path}")
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                if "mcpServers" in config:
                    servers = config["mcpServers"]
                    if "groq-audio-transcription" in servers:
                        print("   • Groq transcription server: ✅ Configured")
                    else:
                        print("   • Groq transcription server: ❌ Not configured")
                else:
                    print("   • MCP servers: ❌ No servers configured")
        except Exception as e:
            print(f"   • Config parsing: ❌ {e}")
    else:
        print(f"   • Config file: ❌ Not found")
        print(f"   • Expected location: {config_path}")
    
    print("\n🎉 Diagnostics completed!")
    return True

def show_usage_examples():
    """Show usage examples for the MCP server"""
    print("\n📚 Usage Examples:")
    print("=" * 20)
    
    print("\n1. Test server directly:")
    print("   uv run python simple_ping_mcp.py")
    
    print("\n2. Run server:")
    print("   uv run python mcp_server.py")
    
    print("\n3. Test with audio file:")
    print("   uv run python test_mcp_server.py")
    
    print("\n4. Claude Desktop config location:")
    print("   ~/Library/Application Support/Claude/claude_desktop_config.json")
    
    print("\n5. Example Claude Desktop config:")
    print("""   {
     "mcpServers": {
       "groq-audio-transcription": {
         "command": "uv",
         "args": ["run", "python", "mcp_server.py"],
         "cwd": "/Users/ngumus/Desktop/groq",
         "env": {
           "GROQ_API_KEY": "your-api-key"
         }
       }
     }
   }""")

if __name__ == "__main__":
    success = check_mcp_server_status()
    show_usage_examples()
    sys.exit(0 if success else 1)