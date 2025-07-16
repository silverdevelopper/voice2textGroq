# Groq Audio Transcription MCP Server

This project provides a Model Context Protocol (MCP) server that enables audio transcription using Groq's Whisper models. The server can be used with Claude Desktop and other MCP-compatible applications.

## Features

- **Audio Transcription**: Transcribe audio files using Groq's Whisper models
- **Multiple Input Methods**: Support for base64 encoded audio data and direct URL transcription
- **Timestamp Support**: Provides word-level and segment-level timestamps
- **Format Support**: Supports MP3, MP4, M4A, MPEG, MPGA, M4B, WAV, WEBM formats
- **Automatic Language Detection**: Detects the language of the audio automatically

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Groq API key:
```bash
export GROQ_API_KEY="your-groq-api-key-here"
```

Or create a `.env` file:
```
GROQ_API_KEY=your-groq-api-key-here
```

## MCP Server Usage

### Available Tools

1. **transcribe_audio_file**: Transcribe audio from base64 encoded data
2. **transcribe_audio_url**: Transcribe audio from a URL
3. **format_transcription**: Format transcription results into readable text
4. **get_supported_formats**: Get information about supported formats

### Running the MCP Server

```bash
python mcp_server.py
```

### Testing the Server

```bash
python test_mcp_server.py
```

### Example Client Usage

```bash
python mcp_client_example.py
```

## Claude Desktop Integration

To use this MCP server with Claude Desktop, add the following configuration to your Claude Desktop settings:

```json
{
  "mcpServers": {
    "groq-audio-transcription": {
      "command": "python",
      "args": ["/path/to/your/mcp_server.py"],
      "env": {
        "GROQ_API_KEY": "your-groq-api-key-here"
      }
    }
  }
}
```

## API Reference

### transcribe_audio_file

Transcribes audio from base64 encoded data.

**Parameters:**
- `audio_data` (string): Base64 encoded audio file data
- `filename` (string, optional): Original filename for format detection
- `model` (string, optional): Whisper model to use (default: whisper-large-v3-turbo)

**Returns:**
Dictionary containing transcription results with timestamps and metadata.

### transcribe_audio_url

Transcribes audio from a URL.

**Parameters:**
- `audio_url` (string): URL to the audio file
- `model` (string, optional): Whisper model to use (default: whisper-large-v3-turbo)

**Returns:**
Dictionary containing transcription results with timestamps and metadata.

### format_transcription

Formats transcription data into readable text with timestamps.

**Parameters:**
- `transcription_data` (dict): Dictionary containing transcription results

**Returns:**
Formatted transcription text with timestamps.

### get_supported_formats

Returns information about supported audio formats and features.

**Returns:**
Dictionary containing supported formats, features, and available models.

## Example Response Format

```json
{
  "text": "Hello, this is a test audio file.",
  "language": "en",
  "duration": 5.23,
  "segments": [
    {
      "start": 0.0,
      "end": 2.5,
      "text": "Hello, this is a test",
      "formatted_time": "[00:00.00 - 00:02.50]"
    }
  ],
  "metadata": {
    "model": "whisper-large-v3-turbo",
    "filename": "test.wav",
    "total_segments": 1
  }
}
```

## Error Handling

The server provides comprehensive error handling and returns error information in the response when transcription fails.

## Requirements

- Python 3.12+
- Groq API key
- MCP library
- All dependencies listed in requirements.txt

## Contributing

Feel free to submit issues and pull requests to improve the MCP server functionality.