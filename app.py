import os
import json
import gradio as gr
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Groq client
client = None

def transcribe_audio(audio_file):
    """
    Transcribe an uploaded audio file using Groq's Whisper model
    """
    if audio_file is None:
        return "Please upload an audio file first.", None, gr.update(visible=False)
    
    try:
        # Open the audio file in binary mode
        with open(audio_file, "rb") as file:
            # Create a transcription of the audio file
            transcription = client.audio.transcriptions.create(
                file=file,  # Required audio file
                model="whisper-large-v3-turbo",  # Required model to use for transcription
                prompt="Specify context or spelling",  # Optional
                response_format="verbose_json",  # Optional
                timestamp_granularities=["word", "segment"],  # Optional
                language="en",  # Optional
                temperature=0.0  # Optional
            )
        
        # Save transcription to file
        os.makedirs("transcripts", exist_ok=True)
        filename = audio_file.split(".")[0] + ".txt"
        base_name = os.path.splitext(os.path.basename(filename))[0]
        
        # Save JSON data
        with open(f"transcripts/{base_name}.json", "w") as f:
            json.dump(transcription.to_dict(), f, indent=2, default=str)
        
        # Format transcription with timestamps
        formatted_output = []
        
        # Add header information
        formatted_output.append(f"Language: {transcription.language}")
        formatted_output.append(f"Duration: {transcription.duration:.2f} seconds")
        formatted_output.append(f"Total segments: {len(transcription.segments) if hasattr(transcription, 'segments') else 0}")
        formatted_output.append("")
        formatted_output.append("TRANSCRIPTION WITH TIMESTAMPS:")
        formatted_output.append("=" * 40)
        
        # Add segments with timestamps
        if hasattr(transcription, 'segments') and transcription.segments:
            for i, segment in enumerate(transcription.segments):
                start_time = segment["start"]
                end_time = segment["end"]
                text = segment["text"].strip()
                
                # Format timestamp as MM:SS
                start_formatted = f"{int(start_time//60):02d}:{start_time%60:05.2f}"
                end_formatted = f"{int(end_time//60):02d}:{end_time%60:05.2f}"
                
                formatted_output.append(f"[{start_formatted} - {end_formatted}] {text}")
        else:
            # Fallback to full text if no segments
            formatted_output.append(f"[00:00.00] {transcription.text}")
        
        formatted_text = "\n".join(formatted_output)
        
        # Save formatted transcription as TXT
        txt_filename = f"transcripts/{base_name}_formatted.txt"
        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write(formatted_text)
        
        return formatted_text, txt_filename, gr.update(visible=True)
        
    except Exception as e:
        print(e)
        return f"Error transcribing audio: {str(e)}", None, gr.update(visible=False)

def download_transcription(txt_filename):
    """Return the transcription file for download"""
    if txt_filename and os.path.exists(txt_filename):
        return txt_filename
    return None

# Create the Gradio interface
def create_interface(api_key=None):
    global client
    client = Groq(api_key=api_key)
    with gr.Blocks(title="Groq Audio Transcription", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🎵 Groq Audio Transcription")
        gr.Markdown("Upload an audio file to transcribe it using Groq's Whisper model.")
        
        with gr.Row():
            with gr.Column(scale=1):
                audio_input = gr.Audio(
                    label="Upload Audio File",
                    type="filepath",
                    sources=["upload"]
                )
                
                transcribe_btn = gr.Button(
                    "🎤 Transcribe Audio",
                    variant="primary",
                    size="lg"
                )
            
            with gr.Column(scale=2):
                output_text = gr.Textbox(
                    label="Transcription Results",
                    placeholder="Transcription will appear here...",
                    lines=15,
                    max_lines=20
                )
                
                download_btn = gr.Button(
                    "📥 Download Formatted Transcription",
                    visible=False,
                    variant="secondary"
                )
        
        # Add some helpful information
        with gr.Accordion("ℹ️ Information", open=False):
            gr.Markdown("""
            **Supported Audio Formats:**
            - MP3, MP4, M4A, MPEG, MPGA, M4B, WAV, WEBM
            
            **Features:**
            - Automatic language detection
            - Segment-level timestamps
            - High-quality transcription using Whisper Large V3 Turbo
            
            **Output Format:**
            - Timestamped transcription: `[MM:SS.ss - MM:SS.ss] text`
            - Language detection
            - Audio duration
            - Full JSON data saved to transcripts/ folder
            """)
        
        # Store the filename for download
        filename_state = gr.State()
        
        # Connect the button to the function
        transcribe_btn.click(
            fn=transcribe_audio,
            inputs=[audio_input],
            outputs=[output_text, filename_state, download_btn]
        )
        
        # Auto-transcribe when file is uploaded
        audio_input.change(
            fn=transcribe_audio,
            inputs=[audio_input],
            outputs=[output_text, filename_state, download_btn]
        )
        
        # Handle download button click
        download_btn.click(
            fn=download_transcription,
            inputs=[filename_state],
            outputs=[gr.File(label="Download Transcription")]
        )
    
    return demo

if __name__ == "__main__":
    # Create and launch the interface
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    ) 