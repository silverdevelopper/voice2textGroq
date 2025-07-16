#!/usr/bin/env python3

import os
import json
import tempfile
import base64
from typing import Any, Dict, Optional
from mcp.server.fastmcp import FastMCP
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the MCP server
mcp = FastMCP("Groq Audio Transcription Server")

# Initialize the Groq client
client = Groq()

@mcp.tool()
def transcribe_audio_file(audio_data: str, filename: str = "audio.wav", model: str = "whisper-large-v3-turbo") -> Dict[str, Any]:
    """
    Transcribe audio from base64 encoded audio data using Groq's Whisper model
    
    Args:
        audio_data: Base64 encoded audio file data
        filename: Original filename (optional, used for format detection)
        model: Whisper model to use (default: whisper-large-v3-turbo)
    
    Returns:
        Dictionary containing transcription results with timestamps and metadata
    """
    try:
        # Decode base64 audio data
        audio_bytes = base64.b64decode(audio_data)
        
        # Create a temporary file to store the audio
        with tempfile.NamedTemporaryFile(suffix=os.path.splitext(filename)[1], delete=False) as temp_file:
            temp_file.write(audio_bytes)
            temp_file_path = temp_file.name
        
        try:
            # Transcribe the audio file
            with open(temp_file_path, "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=file,
                    model=model,
                    response_format="verbose_json",
                    timestamp_granularities=["word", "segment"],
                    temperature=0.0
                )
            
            # Process the transcription results
            result = {
                "text": transcription.text,
                "language": transcription.language,
                "duration": transcription.duration,
                "segments": [],
                "metadata": {
                    "model": model,
                    "filename": filename,
                    "total_segments": len(transcription.segments) if hasattr(transcription, 'segments') else 0
                }
            }
            
            # Add segments with timestamps if available
            if hasattr(transcription, 'segments') and transcription.segments:
                for segment in transcription.segments:
                    start_time = segment["start"]
                    end_time = segment["end"]
                    text = segment["text"].strip()
                    
                    # Format timestamps as MM:SS.ss
                    start_formatted = f"{int(start_time//60):02d}:{start_time%60:05.2f}"
                    end_formatted = f"{int(end_time//60):02d}:{end_time%60:05.2f}"
                    
                    result["segments"].append({
                        "start": start_time,
                        "end": end_time,
                        "text": text,
                        "formatted_time": f"[{start_formatted} - {end_formatted}]"
                    })
            
            return result
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        return {
            "error": f"Error transcribing audio: {str(e)}",
            "success": False
        }

@mcp.tool()
def transcribe_audio_url(audio_url: str, model: str = "whisper-large-v3-turbo") -> Dict[str, Any]:
    """
    Transcribe audio from a URL using Groq's Whisper model
    
    Args:
        audio_url: URL to the audio file
        model: Whisper model to use (default: whisper-large-v3-turbo)
    
    Returns:
        Dictionary containing transcription results with timestamps and metadata
    """
    try:
        import requests
        
        # Download the audio file
        response = requests.get(audio_url)
        response.raise_for_status()
        
        # Get filename from URL
        filename = os.path.basename(audio_url.split('?')[0]) or "audio.wav"
        
        # Create a temporary file to store the audio
        with tempfile.NamedTemporaryFile(suffix=os.path.splitext(filename)[1], delete=False) as temp_file:
            temp_file.write(response.content)
            temp_file_path = temp_file.name
        
        try:
            # Transcribe the audio file
            with open(temp_file_path, "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=file,
                    model=model,
                    response_format="verbose_json",
                    timestamp_granularities=["word", "segment"],
                    temperature=0.0
                )
            
            # Process the transcription results (same as above)
            result = {
                "text": transcription.text,
                "language": transcription.language,
                "duration": transcription.duration,
                "segments": [],
                "metadata": {
                    "model": model,
                    "source_url": audio_url,
                    "filename": filename,
                    "total_segments": len(transcription.segments) if hasattr(transcription, 'segments') else 0
                }
            }
            
            # Add segments with timestamps if available
            if hasattr(transcription, 'segments') and transcription.segments:
                for segment in transcription.segments:
                    start_time = segment["start"]
                    end_time = segment["end"]
                    text = segment["text"].strip()
                    
                    # Format timestamps as MM:SS.ss
                    start_formatted = f"{int(start_time//60):02d}:{start_time%60:05.2f}"
                    end_formatted = f"{int(end_time//60):02d}:{end_time%60:05.2f}"
                    
                    result["segments"].append({
                        "start": start_time,
                        "end": end_time,
                        "text": text,
                        "formatted_time": f"[{start_formatted} - {end_formatted}]"
                    })
            
            return result
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        return {
            "error": f"Error transcribing audio from URL: {str(e)}",
            "success": False
        }

@mcp.tool()
def format_transcription(transcription_data: Dict[str, Any]) -> str:
    """
    Format transcription data into a readable text format with timestamps
    
    Args:
        transcription_data: Dictionary containing transcription results
        
    Returns:
        Formatted transcription text with timestamps
    """
    try:
        if "error" in transcription_data:
            return f"Error: {transcription_data['error']}"
        
        formatted_output = []
        
        # Add header information
        metadata = transcription_data.get("metadata", {})
        formatted_output.append(f"Language: {transcription_data.get('language', 'Unknown')}")
        formatted_output.append(f"Duration: {transcription_data.get('duration', 0):.2f} seconds")
        formatted_output.append(f"Total segments: {metadata.get('total_segments', 0)}")
        formatted_output.append(f"Model: {metadata.get('model', 'Unknown')}")
        formatted_output.append("")
        formatted_output.append("TRANSCRIPTION WITH TIMESTAMPS:")
        formatted_output.append("=" * 40)
        
        # Add segments with timestamps
        segments = transcription_data.get("segments", [])
        if segments:
            for segment in segments:
                formatted_time = segment.get("formatted_time", "")
                text = segment.get("text", "")
                formatted_output.append(f"{formatted_time} {text}")
        else:
            # Fallback to full text if no segments
            formatted_output.append(f"[00:00.00] {transcription_data.get('text', '')}")
        
        return "\n".join(formatted_output)
        
    except Exception as e:
        return f"Error formatting transcription: {str(e)}"

@mcp.tool()
def get_supported_formats() -> Dict[str, Any]:
    """
    Get information about supported audio formats and features
    
    Returns:
        Dictionary containing supported formats and features
    """
    return {
        "supported_formats": [
            "MP3", "MP4", "M4A", "MPEG", "MPGA", "M4B", "WAV", "WEBM"
        ],
        "features": [
            "Automatic language detection",
            "Segment-level timestamps",
            "Word-level timestamps",
            "High-quality transcription using Whisper models"
        ],
        "available_models": [
            "whisper-large-v3-turbo",
            "whisper-large-v3"
        ],
        "input_methods": [
            "Base64 encoded audio data",
            "Direct URL to audio file"
        ]
    }

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()