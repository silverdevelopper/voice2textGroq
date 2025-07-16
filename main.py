import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
os.makedirs("transcripts", exist_ok=True)


# Initialize the Groq client
client = Groq()

# Specify the path to the audio file
filename = os.path.dirname(__file__) + "/audio.m4a" # Replace with your audio file!

# Open the audio file
with open(filename, "rb") as file:
    # Create a transcription of the audio file
    transcription = client.audio.transcriptions.create(
      file=file, # Required audio file
      model="whisper-large-v3-turbo", # Required model to use for transcription
      prompt="Specify context or spelling",  # Optional
      response_format="verbose_json",  # Optional
      timestamp_granularities = ["word", "segment"], # Optional (must set response_format to "json" to use and can specify "word", "segment" (default), or both)
      language="en",  # Optional
      temperature=0.0  # Optional
    )

with open(f"transcripts/{filename.split('/')[-1].split('.')[0]}.txt", "w") as f:

  segments= transcription.to_dict()["segments"]
  for i, segment in enumerate(transcription.segments):
      start_time = segment["start"]
      end_time = segment["end"]
      start_formatted = f"{int(start_time//60):02d}:{start_time%60:05.2f}"
      end_formatted = f"{int(end_time//60):02d}:{end_time%60:05.2f}"
      f.write(f"{start_formatted} - {end_formatted} {segment['text']}\n")
    