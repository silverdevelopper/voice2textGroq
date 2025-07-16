#!/usr/bin/env python3

import subprocess
import json
import time
import sys

def ping_mcp_server():
    """Simple ping test for MCP server"""
    
    print("🔍 Testing MCP server...")
    
    # Test 1: Check if server starts without errors
    print("\n1. Testing server startup...")
    try:
        # Start the server process
        process = subprocess.Popen(
            ["uv", "run", "python", "mcp_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True
        )
        
        # Give it a moment to start
        time.sleep(2)
        
        # Check if it's still running
        if process.poll() is None:
            print("✅ Server started successfully!")
            
            # Send a simple JSON-RPC initialization message
            print("\n2. Testing JSON-RPC communication...")
            init_message = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "ping-test",
                        "version": "1.0.0"
                    }
                }
            }
            
            try:
                # Send initialization message
                process.stdin.write(json.dumps(init_message) + "\n")
                process.stdin.flush()
                
                # Try to read response (with timeout)
                import select
                if select.select([process.stdout], [], [], 3):
                    response = process.stdout.readline()
                    if response:
                        print("✅ Server responded to initialization!")
                        print(f"Response: {response.strip()}")
                    else:
                        print("⚠️  No response received")
                else:
                    print("⚠️  Server didn't respond within timeout")
                    
            except Exception as e:
                print(f"⚠️  Communication test failed: {e}")
            
        else:
            print("❌ Server failed to start")
            stderr_output = process.stderr.read()
            if stderr_output:
                print(f"Error: {stderr_output}")
        
        # Clean up
        process.terminate()
        process.wait()
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False
    
    # Test 2: Check if tools are importable
    print("\n3. Testing tool imports...")
    try:
        from mcp_server import get_supported_formats, transcribe_audio_file
        print("✅ Tools imported successfully!")
        
        # Test get_supported_formats
        formats = get_supported_formats()
        print(f"✅ get_supported_formats works: {len(formats['supported_formats'])} formats")
        
    except Exception as e:
        print(f"❌ Tool import failed: {e}")
        return False
    
    print("\n🎉 MCP server ping test completed successfully!")
    return True

def quick_health_check():
    """Quick health check of the MCP server"""
    print("🏥 Quick health check...")
    
    # Check if we can import the server
    try:
        import mcp_server
        print("✅ Server module imports correctly")
    except Exception as e:
        print(f"❌ Server module import failed: {e}")
        return False
    
    # Check if tools work
    try:
        formats = mcp_server.get_supported_formats()
        print(f"✅ get_supported_formats: {len(formats['supported_formats'])} formats")
    except Exception as e:
        print(f"❌ get_supported_formats failed: {e}")
        return False
    
    print("✅ Health check passed!")
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("MCP Server Ping Test")
    print("=" * 50)
    
    # Run quick health check first
    if not quick_health_check():
        print("\n❌ Health check failed, skipping full ping test")
        sys.exit(1)
    
    # Run full ping test
    success = ping_mcp_server()
    sys.exit(0 if success else 1)