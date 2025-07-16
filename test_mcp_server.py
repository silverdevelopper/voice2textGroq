#!/usr/bin/env python3

import base64
import json
import os
from mcp_server import get_supported_formats, transcribe_audio_file, format_transcription

def test_with_existing_audio():
    """Test the MCP server with existing audio file"""
    
    # Check if there's an existing audio file
    audio_file = "audio.m4a"
    if not os.path.exists(audio_file):
        print(f"Audio file {audio_file} not found. Please provide an audio file to test.")
        return
    
    # Read and encode the audio file
    with open(audio_file, "rb") as f:
        audio_data = base64.b64encode(f.read()).decode('utf-8')
    
    print("Testing MCP Audio Transcription Server...")
    print("=" * 50)
    
    # Test 1: Get supported formats
    print("1. Testing get_supported_formats...")
    formats = get_supported_formats()
    print(json.dumps(formats, indent=2))
    print()
    
    # Test 2: Transcribe audio file
    print("2. Testing transcribe_audio_file...")
    transcription = transcribe_audio_file(audio_data, audio_file)
    
    if "error" in transcription:
        print(f"Error: {transcription['error']}")
    else:
        print(f"Language: {transcription['language']}")
        print(f"Duration: {transcription['duration']:.2f} seconds")
        print(f"Segments: {len(transcription['segments'])}")
        print(f"Text: {transcription['text'][:200]}..." if len(transcription['text']) > 200 else transcription['text'])
        print()
    
    # Test 3: Format transcription
    print("3. Testing format_transcription...")
    formatted = format_transcription(transcription)
    print(formatted[:500] + "..." if len(formatted) > 500 else formatted)
    
    print("\nMCP Server test completed!")

if __name__ == "__main__":
    test_with_existing_audio()