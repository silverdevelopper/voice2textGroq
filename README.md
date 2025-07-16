# Groq Audio Transcription

A Python application for transcribing audio files using Groq's Whisper model. This project includes both a command-line interface and a web-based UI built with Gradio.

## Features

- 🎵 Audio transcription using Groq's Whisper Large V3 Turbo model
- 🌐 Web-based UI with drag-and-drop file upload
- 📝 Command-line interface for batch processing
- 🕒 Word-level and segment-level timestamps
- 🌍 Automatic language detection
- 💾 JSON output with detailed transcription data
- 📁 Automatic file organization in transcripts folder

## Setup

### Prerequisites

- Python 3.12 or higher
- Groq API key

### Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   uv sync
   ```

3. Create a `.env` file in the project root with your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

## Usage

### Web UI (Recommended)

Run the Gradio web interface:

```bash
uv sync app.py
```

Or use the convenience script:

```bash
uv run run_app.py
```

The web interface will be available at `http://localhost:7860`

**Features of the Web UI:**
- Drag and drop audio file upload
- Real-time transcription
- Formatted results display
- Automatic file saving
- Support for multiple audio formats

### Command Line

For command-line usage, modify the `main.py` file to point to your audio file:

```python
filename = "path/to/your/audio.m4a"  # Update this line
```

Then run:

```bash
python main.py
```

## Supported Audio Formats

- MP3
- MP4
- M4A
- MPEG
- MPGA
- M4B
- WAV
- WEBM

## Output

The application generates:

1. **Console Output**: Formatted transcription results
2. **JSON Files**: Detailed transcription data saved in the `transcripts/` folder
3. **Web UI**: Interactive display with transcription text and metadata

### JSON Output Structure

```json
{
  "text": "Transcribed text content",
  "language": "en",
  "duration": 120.5,
  "segments": 15,
  "words": 250
}
```

## Configuration

### Environment Variables

- `GROQ_API_KEY`: Your Groq API key (required)

### Transcription Options

The app uses the following default settings:
- Model: `whisper-large-v3-turbo`
- Response format: `verbose_json`
- Timestamp granularities: `["word", "segment"]`
- Language: `en` (auto-detected if not specified)
- Temperature: `0.0` (for consistent results)

## Project Structure

```
groq/
├── app.py              # Gradio web UI
├── main.py             # Command-line interface
├── run_app.py          # Convenience script
├── pyproject.toml      # Project dependencies
├── README.md           # This file
├── transcripts/        # Output folder for JSON files
└── .env               # Environment variables (create this)
```

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your `.env` file contains a valid `GROQ_API_KEY`
2. **Audio Format**: Make sure your audio file is in a supported format
3. **File Size**: Large audio files may take longer to process
4. **Network**: Ensure you have a stable internet connection for API calls

### Getting Help

- Check that all dependencies are installed: `uv sync`
- Verify your API key is correct
- Ensure your audio file is not corrupted
- Check the console output for detailed error messages

## License

This project is open source. Feel free to modify and distribute as needed.
