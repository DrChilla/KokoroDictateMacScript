import subprocess
from openai import OpenAI
import os
import time
import sys

# Debug helper
def debug(msg):
    sys.stderr.write(f"DEBUG: {msg}\n")
    sys.stderr.flush()

# Initialize OpenAI client
client = OpenAI(
    base_url="http://localhost:8880/v1",
    api_key="not-needed",
    timeout=10.0
)

def get_selected_text():
    try:
        # Store original clipboard content
        original = subprocess.run(['pbpaste'], capture_output=True, text=True, check=True).stdout
        
        # Copy selected text to clipboard
        subprocess.run(['osascript', '-e', 'tell application "System Events" to keystroke "c" using command down'], check=True)
        
        # Wait for clipboard to update
        time.sleep(0.2)
        
        # Get text from clipboard
        result = subprocess.run(['pbpaste'], capture_output=True, text=True, check=True)
        selected_text = result.stdout.strip()
        
        # Restore original clipboard content
        subprocess.run(['pbcopy'], input=original.encode(), check=True)
        
        if selected_text == original:
            debug("No new text was selected (clipboard unchanged)")
            return None
        
        return selected_text
        
    except subprocess.CalledProcessError as e:
        debug(f"Error getting selected text: {e}")
        return None
    except Exception as e:
        debug(f"Unexpected error while getting selected text: {e}")
        return None

def main():
    temp_file = "temp_speech.mp3"
    try:
        # Get selected text
        text = get_selected_text()
        
        if not text:
            debug("Error: No text selected. Please select some text and try again.")
            return
            
        debug(f"Processing text: '{text}'")
        
        # Generate speech from text
        response = client.audio.speech.create(
            model="kokoro",
            voice="af_heart(1)+bf_lily(2)+bf_emma(4)",
            input=text
        )
        
        # Save to temporary file
        response.stream_to_file(temp_file)
        debug(f"Saved to {temp_file}")
        
        # Play the audio using system command
        debug("Playing audio...")
        result = subprocess.run(['afplay', temp_file], check=True)
        debug("Audio playback complete")
        
    except subprocess.CalledProcessError as e:
        debug(f"Error during audio playback: {e}")
    except Exception as e:
        debug(f"Error during processing: {str(e)}")
    finally:
        # Clean up temp file
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception as e:
                debug(f"Error removing temporary file: {e}")

